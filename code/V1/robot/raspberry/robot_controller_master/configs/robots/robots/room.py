
from configs.robots.robot import Robot
from configs.robots.dof import DofName
from utils.constants import serial_default_port
from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS


room_name = 'room'

room_ip = '192.168.0.5'

room_arduino_port = serial_default_port
room_esp1_ip = '192.168.0.5'
room_esp2_ip = '192.168.0.6'
room_esp3_ip = '192.168.0.7'


room_dofs = {
    DofName.FORWARD: room_esp1_ip,
    DofName.STRAFE: room_esp2_ip,
    DofName.ANGULAR: room_esp1_ip,
    DofName.PETALS: room_esp2_ip,
    DofName.EYE_X: room_esp2_ip,
    DofName.EYE_Y: room_esp1_ip,
    DofName.LED: room_esp3_ip,
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
