
import serial
import time
from utils.constants import \
    serial_default_delay_after_setup, DELIMITER


class EspUdpChannel:

    def __init__(self,
                 esp_ip):
        self.esp_ip = esp_ip


    def setup_esp_udp(self):

        print(f"[ESPUDPCHANNEL][IP '{self.esp_ip}'][SETUP ESPUDP] - START setting up ESPUDP")

        print(f"[ESPUDPCHANNEL][IP '{self.esp_ip}'][SETUP ESPUDP] - "
              "attempting UDP connection at PORT: ", self.esp_ip)

    

    def cleanup(self):
        self.ser.close()
