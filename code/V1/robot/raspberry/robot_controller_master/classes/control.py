
import time
from subprocess import call
from classes.serial_channel import SerialChannel
from classes.networking_channel import NetworkingChannel
from classes.esp_channel import SingleValueEspChannel, MultiValueEspChannel
from classes.out_sensor import PassThroughChannel, AggregateChannel
from classes.esp_value import EspValue
from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS
from utils.util_methods import parse_serial_message
from utils.util_methods import get_single_msg_for_serial
from utils.util_methods import bytes_to_unicode_str
from utils.constants import net_reset_msg, net_quit_msg, MSG_DELIMITER
from configs.esps.esp_types import esp_value_types, ESP_CHANNEL_TYPE


DEFAULT_SERIAL_ELAPSED = 0.005
id1="Outsensor1"
id2="Outsensor2"
id3="Outsensor3"

def quit_program():
    print("[CONTROL]-----------QUIT")
    quit()


class Control:
    def __init__(self,
                 robot,
                 path_to_restart):

        # -- VARIABLES
        # the ROBOT, which contains the configuration (name, ip, dofs, serial ports)
        self.ROBOT = robot
        #
        # path to the RESTART.SH file used to restart the program
        self.path_to_restart = path_to_restart

        # -- NETWORKING (with ESP)
        #
        self.NETWORKING_CHANNEL = NetworkingChannel(self.ROBOT.ip)

        self.priority_responses = {
            net_reset_msg: self.restart_program,
            net_quit_msg: quit_program
        }

        # -- SERIAL (with Arduino)
        # there is ONE SERIAL CHANNEL for every Arduino on the Robot.
        # it's a STRING-SERIALCHANNEL dict, where the STRING is the SERIAL PORT of that channel
        self.SERIAL_CHANNELS = dict()

        for serial_port in set(self.ROBOT.dof_name_to_serial_port_dict.values()):
            if serial_port not in self.SERIAL_CHANNELS:
                self.SERIAL_CHANNELS[serial_port] = SerialChannel(serial_port)
               # print(f"[CONTROLS][on_new_config_rcv] '{self.SERIAL_CHANNELS}'")

        self.last_serial_time = time.time()
        
        self.INSENSOR_CHANNELS = dict()
        self.setup_init_inSensor_config()
        # -- ESP CHANNEL
        self.ESP_CHANNELS = dict()
        self.setup_init_outSensor_config()
        print("Hola")

    # ------------------------------------------------------------------------------------------ APP CONFIG
    def on_new_config_rcv(self, ip, esp_value_key, dof_key, set):
        # received from APP to set a NEW config: it means that the ESP_VALUE coming from ESP with

        if not set:
            # REMOVE CONFIG
            # if SET IS FALSE, it means the ESP_VALUE is to be set DEACTIVATED
            #    (meaning: the corresponding ESP_VALUE class must be removed, if present)
            #    0. check if IP is present in the list. If not, DO NOTHING (it means that config is ABSENT)
            #    2. check if the 'esp value' has an esp type 'single' or 'multi'.
            #       - if 'single', remove the entire ESP_CHANNEL from list;
            #       - if 'multi', remove the ESP_VALUE from the corresponding ESP_CHANNEL.
            #         if Esp_channel becomes empty, remove it

            # 0.
            if ip not in self.ESP_CHANNELS:
                return

            if self.ESP_CHANNELS[ip].channel_type == ESP_CHANNEL_TYPE.SINGLE_VALUE:
                del self.ESP_CHANNELS[ip]
            else:
                self.ESP_CHANNELS[ip].remove_esp_value(esp_value_key)
                if len(self.ESP_CHANNELS[ip].esp_values) <= 0:
                    del self.ESP_CHANNELS[ip]

        else:
            # ADD CONFIG
            # if SET IS TRUE, it means the ESP_VALUE is to be set ACTIVE
            #   (meaning: the corresponding ESP_VALUE class must exist)
            #    ip = 'ip' and key = 'esp_value_    key' is to be associated with DOF = 'dof'.
            #    0. get the DOFNAME enum element from the STRING KEY
            #    1. generate a new ESP_VALUE according to the KEY.
            #    2. check if the 'esp value' has an esp type 'single' or 'multi', and then call the corresponding method

            # 0.
            dof = None
            for temp_dof in self.ROBOT.dof_name_to_serial_port_dict:
                if temp_dof.value.key == dof_key:
                    dof = temp_dof
                    break
            if dof is None:
                print(f"[CONTROLS][on_new_config_rcv] - ip: '{ip}' - esp_value_key: '{esp_value_key}' - dof: '{dof}': "
                      f"INVALID DOF - DOF NOT PRESENT IN ROBOT CONFIG")

            # 1.
            temp_esp_value = EspValue(esp_value_types[esp_value_key], dof)

            # 2.
            if temp_esp_value.esp_value_type.channel_type == ESP_CHANNEL_TYPE.SINGLE_VALUE:
                self.add_esp_value_single(ip, temp_esp_value)
            elif temp_esp_value.esp_value_type.channel_type == ESP_CHANNEL_TYPE.MULTI_VALUE:
                self.add_esp_value_multi(ip, temp_esp_value)
            else:
                print(f"[CONTROLS][on_new_config_rcv] - ip: '{ip}' - esp_value_key: '{esp_value_key}' - dof: '{dof}': "
                      f"INVALID CHANNEL TYPE")

    def add_esp_value_single(self, ip, new_esp_value):
        # called when receiving a message from THE APP.
        # called to ADD a new ESP-DOF link, with a SINGLE-VALUE ESP with IP='ip'.
        # 1. generate a new Single-Value esp channel with that IP and add it to the DICT of channels,
        #    using the IP as KEY. If there was a previous one with same IP, it's simply overridden
        temp_esp_channel = SingleValueEspChannel(ip, new_esp_value)
        self.ESP_CHANNELS[ip] = temp_esp_channel

    def add_esp_value_multi(self, ip, new_esp_value):
        # called when receiving a message from THE APP.
        # called to ADD a new ESP-DOF link, with a SINGLE-VALUE ESP with IP='ip'.
        # 1. check if there already is an ESP_CHANNEL with that IP in the dict.
        #    - if there is NOT: create a new one
        # 2. add the new ESP_VALUE to the ESP_CHANNEL with that IP using the ESP_CHANNEL method.
        #    that method will override an existing ESP_VALUE of the same type if present
        if ip not in self.ESP_CHANNELS:
            temp_esp_channel = MultiValueEspChannel(ip)
            self.ESP_CHANNELS[ip] = temp_esp_channel

        self.ESP_CHANNELS[ip].add_esp_value(new_esp_value)
        print(f"[CONTROL][SETUP] ---------------------------------------------- BEGIN")

    # ------------------------------------------------------------------------------------------ SETUP
    # def add_esp_channel(self, new_esp_channel):
    #     for ip, esp_channel in self.ESP_CHANNELS.items():
    #         if new_esp_channel.ip == esp_channel.IP:
    #             del self.ESP_CHANNELS[ip]
    #     self.ESP_CHANNELS[new_esp_channel.ip] = new_esp_channel

    def setup(self):
        print(f"[CONTROL][SETUP] ---------------------------------------------- BEGIN")
        # 1:
        self.NETWORKING_CHANNEL.setup_udp(self.priority_responses)
        # 2:
        for serial_channel in self.SERIAL_CHANNELS.values():
            serial_channel.setup_serial()

        print(f"[CONTROL][SETUP] ---------------------------------------------- COMPLETE\n")

    # ------------------------------------------------------------------------------------------ LOOP
    def get_esp_signals(self):
        # try to get an UDP message
        # read_udp_blocking() has been set to NON-BLOCKING during initialization.
        # if there is no message to read, the method will return FALSE.

        # UDP: wait for a new message, and get the sender IP.
        #      the senders are the ESP. Check if the sender is a VALID ESP (one among the 'self.ESP_CHANNELS')
        #      if it is, call the corresponding 'onMsgRcv' method to process the data accordingly
        if self.NETWORKING_CHANNEL.read_udp_non_blocking():

            string_msg = bytes_to_unicode_str(self.NETWORKING_CHANNEL.udp_data[0])

            # check if the MSG is valid (None if 'decode' failed) and non-empty
            if string_msg is not None and string_msg:
                sender_ip = self.NETWORKING_CHANNEL.udp_data[1][0]
                print(f"[CONTROL][get_esp_signals] - msg: '{string_msg}' - sender: '{sender_ip}'")

                # check if the message came from a VALID ESP CHANNEL
                if sender_ip in self.ESP_CHANNELS:
                    self.ESP_CHANNELS[sender_ip].on_esp_msg_rcv(string_msg)

    def write_serial(self):
        # the SOURCE for the values to SEND via serial is ANY ESP amongst the ESP_CHANNELS
        # currently registered in the DICT

        #  METHOD:
        #  - for EACH ARDUINO (meaning: for each SERIAL CHANNEL):
        #     - collect all the messages -> process them -> send them via the corresponding SERIAL PORT

        for serial_port, serial_channel in self.SERIAL_CHANNELS.items():

            # print(f"[Control][write_serial] - serial port: '{serial_port}'")
            # initialize empty message
            msg = ""

            # check all values of the ESP CHANNELS.
            #    - use values only for the ESP CHANNELS that are associated to a DOF that is controlled by the
            #      Arduino on this 'serial_port'
            for _, esp_channel in self.ESP_CHANNELS.items():
                for esp_value in esp_channel.esp_values.values():
                    if self.ROBOT.is_serial_port_correct(esp_value.dof_name, serial_port):
                        msg = get_single_msg_for_serial(msg, esp_value.get_msg)

            # if empty message, don't send any message via serial
            if len(msg) > 0:

                # remove the msg delimiter at the end of the MSG
                if msg[-1] == MSG_DELIMITER:
                    msg = msg[:-1]

                serial_channel.write_serial(msg)
         

    def read_serial(self):
        # read all there is to read, if any
        # update serial time only if something was read
        for serial_channel in self.SERIAL_CHANNELS.values():
            while True:
                line = serial_channel.read_serial_non_blocking()
                if line is not None:
                    # print(line)
                    pass
                else:
                    break

    def serial_communication(self):
        # Raspberry and Arduino need to negotiate the HALF-DUPLEX serial channel.
        # to do this, they each send a single full message to the other, one at a time:
        # RASPBERRY is the "master": he's the first that can SEND; then, to send again, it must first have
        # received; a timeout is set in place, so that it can send again
        # even if a message hasn't been received for some time

        # can perform a SERIAL ACTION only every 'self.last_serial_time' seconds (~10ms usually)
        if time.time() - self.last_serial_time < DEFAULT_SERIAL_ELAPSED:
            # print(".. NO SERIAL COMM ..")
            self.write_serial()
            return

        # SEND, if it can
        # print(" --- WRITE: ")
        self.read_serial()
        self.last_serial_time = time.time()

    def loop(self):
        # 1: try to get UPD messages until there are no more
        #    \-> if MSG is received from a valid GLOVE IP, call the corresponding 'onMsgReceived'.
        #        this is done in the 'get_esp_signals' method, to update its setpoint
        # 2: SERIAL COMMUNICATION with Arduino.
        #    - send new data to arduino with a single message

        # 1
        # print(f"------GET ESP SIGNALS")
        self.get_esp_signals()
        # print()

        # 2
        # print(f"------SERIAL COMM")
        self.serial_communication()
        # print("\n")

    # ------------------------------------------------------------------------------------------ UTILS
    # -- ESP PRIORITY MESSAGES
    #
    def restart_program(self):
        print("[CONTROL]-----------RESTARTING")
        self.cleanup()
        time.sleep(1)
        rc = call(self.path_to_restart)

    #
    def cleanup(self):
        for serial_channel in self.SERIAL_CHANNELS.values():
            serial_channel.cleanup()
        self.NETWORKING_CHANNEL.cleanup()

    def setup_init_inSensor_config(self):
        # received from APP to set a NEW config: it means that the ESP_VALUE coming from ESP with
        # ADD CONFIG
        for temp_dof in self.ROBOT.dof_name_to_serial_port_dict:
            for esp_value_key in self.ROBOT.serial_mapping_dict:
                if temp_dof.value.key == esp_value_key.value.key:
                    temp_esp_value=self.ROBOT.serial_mapping_dict[esp_value_key]
                    temp_raw_value = EspValue(esp_value_types[temp_esp_value], temp_dof)
                    self.INSENSOR_CHANNELS[temp_esp_value] = temp_raw_value


        
    def setup_init_outSensor_config(self):
        msg_to_send = ""
        self.on_new_config(id1, ESP_VALUE_TYPE_KEYS.ANGLE_X.value,"M")
        self.on_new_config(id2, ESP_VALUE_TYPE_KEYS.ANGLE_Y.value,"M")
        self.on_new_config(id1, ESP_VALUE_TYPE_KEYS.GYRO_Y.value,"M")
        self.on_new_config(id1, ESP_VALUE_TYPE_KEYS.GYRO_X.value,"M")
        self.on_new_config(id2, ESP_VALUE_TYPE_KEYS.GYRO_Z.value,"M")
        self.on_new_config(id3, ESP_VALUE_TYPE_KEYS.GYRO_X.value,"S")

        '''for temp in self.ESP_CHANNELS.values():
            if temp.channel_type == ESP_CHANNEL_TYPE.AGGREGATIONE_VALUE:
                temp1= temp.insensor_values.values()
                for rv in temp1:
                    print(rv.current_value)
            else:
                temp1= temp.esp_value.current_value
                print(temp1)
        '''
        msg_to_send=self.send_sensor_signals()
        print(msg_to_send)
        
    
    def on_new_config(self, id, esp_value_key, type):
        if(type=="S"):
            self.add_inSensor_value_single(id, self.INSENSOR_CHANNELS[esp_value_key])
        elif type=="M":
            self.add_inSensor_value_multi(id, self.INSENSOR_CHANNELS[esp_value_key])               
    
    def add_inSensor_value_single(self, id, serial_value):
   
        temp_insensor_channel = PassThroughChannel(id, serial_value)
        self.ESP_CHANNELS[id] = temp_insensor_channel

    def add_inSensor_value_multi(self, id, new_esp_value):
        
        if id not in self.ESP_CHANNELS:
            temp_insensor_channel = AggregateChannel(id)
            self.ESP_CHANNELS[id] = temp_insensor_channel

        self.ESP_CHANNELS[id].add_esp_value(new_esp_value)


    def send_sensor_signals(self):  

        msg_to_send = ''
        for temp in self.ESP_CHANNELS.values():
            msg_to_send += f"{temp.serial}:{temp.esp_value}{MSG_DELIMITER}{MSG_DELIMITER}"
                        
        # Rimuovi l'ultimo trattino basso (_)
            msg_to_send = msg_to_send[:-1]
        return msg_to_send