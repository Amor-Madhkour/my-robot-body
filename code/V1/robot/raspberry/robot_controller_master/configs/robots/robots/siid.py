
from configs.robots.robot import Robot
from configs.robots.dof import DofName
from utils.constants import serial_default_port,serial_default_port2 ,serial_default_port3
from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS
serial_default_port3 

siid_name = 'siid'

siid_ip = '192.168.0.3'

siid_arduino_port1 = serial_default_port
siid_arduino_port2 = serial_default_port2
siid_arduino_port3 = serial_default_port3

siid_dofs = {
    DofName.FORWARD: siid_arduino_port1,
    DofName.STRAFE: siid_arduino_port2,
    DofName.ANGULAR: siid_arduino_port3,
    DofName.PETALS: siid_arduino_port1,
    DofName.EYE_X: siid_arduino_port2,
    DofName.EYE_Y: siid_arduino_port3,
    DofName.LED: siid_arduino_port1,
}

#siid_serial_mappings = {}




siid_serial_mappings = {
    DofName.FORWARD: ESP_VALUE_TYPE_KEYS.ANGLE_X.value,
    DofName.STRAFE:ESP_VALUE_TYPE_KEYS.ANGLE_Y.value,
    DofName.ANGULAR: ESP_VALUE_TYPE_KEYS.ANGLE_Z.value,
    DofName.PETALS: ESP_VALUE_TYPE_KEYS.GYRO_X.value,
    DofName.EYE_X: ESP_VALUE_TYPE_KEYS.GYRO_Y.value,
    DofName.EYE_Y: ESP_VALUE_TYPE_KEYS.GYRO_Z.value,
    DofName.LED: ESP_VALUE_TYPE_KEYS.SONAR.value,
}

siid = Robot(siid_name, siid_ip, siid_dofs, siid_serial_mappings)
