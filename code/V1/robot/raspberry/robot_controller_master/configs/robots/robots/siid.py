
from configs.robots.robot import Robot
from configs.robots.dof import DofName
from utils.constants import serial_default_port,serial_default_port2 ,serial_default_port3
from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS
serial_default_port3 

siid_name = 'siid'

siid_ip = '192.168.0.3'

siid_arduino_port1 = serial_default_port


siid_dofs = {
    DofName.FORWARD: siid_arduino_port1,
    DofName.STRAFE: siid_arduino_port1,
    DofName.ANGULAR: siid_arduino_port1,
    DofName.PETALS: siid_arduino_port1,
    DofName.EYE_X: siid_arduino_port1,
    DofName.EYE_Y: siid_arduino_port1,
    DofName.LED: siid_arduino_port1,
}

#siid_serial_mappings = {}



siid = Robot(siid_name, siid_ip, siid_dofs)
