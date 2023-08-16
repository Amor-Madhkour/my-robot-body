
import serial
import time
from utils.constants import \
    serial_default_baud, serial_default_timeout, serial_default_delay_after_setup, DELIMITER


class EspUdpChannel:

    def __init__(self,
                 esp_ip,
                delay_after_setup=serial_default_delay_after_setup):
        self.esp_ip = esp_ip
        self.delay_after_setup = delay_after_setup

        # declare SER to None; it will be initialized in "setup_serial"
        self.ser = None

    def setup_esp_udp(self):

        print(f"[ESPUDPCHANNEL][IP '{self.esp_ip}'][SETUP ESPUDP] - START setting up ESPUDP")

        print(f"[ESPUDPCHANNEL][IP '{self.esp_ip}'][SETUP ESPUDP] - "
              "attempting UDP connection at PORT: ", self.esp_ip)

        

    def cleanup(self):
        self.ser.close()
