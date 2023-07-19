
from utils.util_methods import get_key_value_string


# wrapper for a SINGLE VALUE coming from and ESP.
# Each type of value has its own processing for when the value is received,
# which will convert the value from the one received from unity/arduino to the one to be sent to Unity/Arduino
class onGoingValue:
##############################################################################################################CLasse che forse è da togliere
    def __init__(self, esp_value_type, sensor_Dof):

        self.esp_value_type = esp_value_type
        # this is the value that is updated when new setpoint is received from UNITY
        # and that is sent to ARDUINO.
        self.current_value = 0
        # every time the current value is sent via serial, the sent value is stored.
        # values are sent via serial if the difference wrt the previously sent value is above the TOLERANCE.
        self.last_sent_value = 0

        self.slope = None

    def on_msg_received(self, string_msg):

        # convert message to FLOAT and save it as 'current_value'
        # if operation can't be completed, notify with PRINT and RETURN
        try:
            self.current_value = self.on_msg_received_preprocessing(float(string_msg))
            # print(f"[ESP VALUE][on_msg_received] - dof: '{self.dof}' - msg: '{string_msg}' - cur val: '{self.current_value}'")
        except Exception as e:
            # print(f"[ESP VALUE][on_msg_received] - dof: '{self.dof}' - "
            #       f"received MSG: '{string_msg}' "
            #       f"but its can't be converted to float: gotten the following ERROR: '{e}'")
            return

    def get_msg_preprocessing(self):
        pass

    def get_msg(self):
        if self.dof is None:
            print("[ESP VALUE][get_msg] - DOF IS NULL -> SKIPPING ESP VALUE")
            return

        # RETURN:
        # key-value message to send to ARDUINO
        # if the last send value is too similar to the current one, return EMPTY STRING

        # perform a subclass-dependant preprocessing of the data
        self.get_msg_preprocessing()

        # print(f"      -  [ESP VALUE][get_msg] - dof: '{self.dof.key}' - "
        #       f"current value: {self.current_value} - last sent: '{self.last_sent_value}' - "
        #       f"abs diff: '{abs(self.current_value - self.last_sent_value)}' - tolerance: '{self.dof.tolerance}' ")

        # check if difference with previous setpoint is higher than tolerance
        # if not, do nothing
        if abs(self.current_value - self.last_sent_value) <= self.dof.tolerance:
            # print(f"[EspValue][get_msg] - value type: '{self.esp_value_type}' - dof: '{self.dof_name.name}' - "
            #       f"cur val: '{self.current_value}' - last sent val: '{self.last_sent_value}' - "
            #       f"tolerance: '{self.dof.tolerance}' - NOT ENOUGH DIFF :: NOT SENDING\n")
            return ""

        # if yes, return key-value message to send to setpoint and update previous setpoint
        self.last_sent_value = self.current_value
        #
        # print(f" |-- sending current value: {self.current_value}")

        return get_key_value_string(self.dof.key, self.current_value)

    # -- UTILS
    def print_info(self):
        print(f"[ESP VALUE][PRINT INFO] - dof: '{self.dof}'")

    def reset(self):
        self.last_sent_value = self.current_value
