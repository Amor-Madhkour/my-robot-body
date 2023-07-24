
from configs.robots.robot import Robot
from configs.robots.dof import DofName
from utils.constants import serial_default_port
from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS


room_name = 'room'

room_ip = '192.168.0.5'

room_arduino_port = serial_default_port

room_dofs = {
    DofName.FORWARD: room_arduino_port,
    DofName.STRAFE: room_arduino_port,
    DofName.ANGULAR: room_arduino_port,
    DofName.PETALS: room_arduino_port,
    DofName.EYE_X: room_arduino_port,
    DofName.EYE_Y: room_arduino_port,
    DofName.LED: room_arduino_port,
}



room_mapping = {
    DofName.FORWARD: ESP_VALUE_TYPE_KEYS.ANGLE_X.value,
    DofName.STRAFE:ESP_VALUE_TYPE_KEYS.ANGLE_Y.value,
    DofName.ANGULAR: ESP_VALUE_TYPE_KEYS.ANGLE_Z.value,
    DofName.PETALS: ESP_VALUE_TYPE_KEYS.GYRO_X.value,
    DofName.EYE_X: ESP_VALUE_TYPE_KEYS.GYRO_Y.value,
    DofName.EYE_Y: ESP_VALUE_TYPE_KEYS.GYRO_Z.value,
    DofName.LED: ESP_VALUE_TYPE_KEYS.SONAR.value,
}


room = Robot(room_name, room_ip, room_dofs, room_mapping)
