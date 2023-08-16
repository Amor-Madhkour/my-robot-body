
from utils.util_methods import parse_serial_message
from configs.esps.esp_types import ESP_CHANNEL_TYPE


# class used to handle the relay of messages from hardware from serial
class inSensor:

    def __init__(self,ip, serial=None):

        #self.serial_value = serial_value
        self.channel_type = None
        self.ip = ip

    def on_esp_msg_rcv(self, string_msg):
        pass
    


class InsensorValueChannel(inSensor):

    def __init__(self, serial, serial_value):
        super(InsensorValueChannel, self).__init__(serial)

        # the channel contains a single esp value.
        self.esp_value = serial_value

        self.channel_type = ESP_CHANNEL_TYPE.SINGLE_VALUE

    def on_esp_msg_rcv(self, string_msg):
        # called when a UDP msg is received from ESP.
        # esp UDP messages for 'single-value' are in the form 'value'

        # 1. transmit message to the esp_value
        # print(f"[SingleValueEspChannel][on_esp_msg_rcv] - ip: {self.ip} - message: '{string_msg}'")

        self.esp_value.on_msg_received(string_msg)


class InsensorMultiValueChannel(inSensor):

    def __init__(self, serial):
        super(InsensorMultiValueChannel, self).__init__(serial)

        # the channel contains a number of "esp values" that are the values
        # that come from the ESP and need to be sent to Arduino after a processing
        # it's an esp_value_key:esp_value dict.
        self.esp_values = dict()

        self.channel_type = ESP_CHANNEL_TYPE.MULTI_VALUE

    def add_esp_value(self, serial_value):
        # this overrides any ESP_VALUE with the same key
        self.esp_values[serial_value.serial_value_type.key] = serial_value

    def remove_esp_value(self, serial_value_key):
        del self.esp_values[serial_value_key]

    def on_esp_msg_rcv(self, string_msg):
        # called when a UDP msg is received from ESP.
        # esp UDP messages for 'multi-value' are in the form 'key:val:_key_val_..'

        # 1. get individual messages
        # 2. for each individual key-value msg,
        #    call the "on_msg_rcv" of the EspValue with the corresponding KEY

        all_key_val_msgs = string_msg
        # print(f"[MultiValueEspChannel][on_esp_msg_rcv] - ip: {self.ip} - messages: '{all_key_val_msgs}'")

        for msg in all_key_val_msgs:
            self.serial_values[msg.key].on_msg_received(msg.value)
