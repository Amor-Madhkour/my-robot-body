
from enum import Enum


class sensor_Dof:
    def __init__(self, key, min_val, max_val, ):
        # the IP address of the device(esp/Oculus) that will receive the value of this DOF
        ip_addresses = ["", ""]
        # the key of the DOF is the same as the key of the ESP_VALUE that will be sent to the ESP
        self.key = key


