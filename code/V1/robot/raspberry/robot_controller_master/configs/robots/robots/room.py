
from configs.robots.robot import Robot
from configs.robots.dof import DofName
from utils.constants import serial_default_port


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


room = Robot(room_name, room_ip, room_dofs)
