
import os

from classes.control import Control
from classes.sensing import Sensing
from configs.robots.dof import DofName
from configs.robots.robots import siid

# ______________________________________________________________________________________________GLOBALS

# directory of the file. It's the same dicrectory of the RESTART.SH file
abs_path = os.path.dirname(os.path.abspath(__file__))
restart_file_name = "restart.sh"
path_to_restart = "./" + restart_file_name  # abs_path + "/restart.sh"


# ______________________________________________________________________________________________ VALUES

# STRING IPS
test_ip_1 = "192.168.0.40"

test_ip_2 = "192.168.0.42"

# ______________________________________________________________________________________________ CREATE VIRTUAL ObJECTS

# INITIALIZE CONTROLS

# -- this variable contains the ROBOT config. Just comment out the robot you are coding for
#    and all the setup will be already implemented in it
robot = siid.siid
# robot = blackwing.blackwing

# -- this is the MAIN CLASS, the one handling all the logic
control = Control(robot, path_to_restart)
sensing= Sensing(robot, path_to_restart)


def add_esp_channels():

    global control
    from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS
    from configs.robots.dof import DofName
    control.on_new_config_rcv(test_ip_1, ESP_VALUE_TYPE_KEYS.ANGLE_X.value, DofName.PETALS.value.key, True)
    control.on_new_config_rcv(test_ip_1, ESP_VALUE_TYPE_KEYS.ANGLE_Y.value, DofName.EYE_X.value.key, True)
    control.on_new_config_rcv(test_ip_1, ESP_VALUE_TYPE_KEYS.ANGLE_Z.value, DofName.LED.value.key, True)
    control.on_new_config_rcv(test_ip_2, ESP_VALUE_TYPE_KEYS.ANGLE_X.value, DofName.PETALS.value.key, True)
    control.on_new_config_rcv(test_ip_2, ESP_VALUE_TYPE_KEYS.ANGLE_Y.value, DofName.EYE_X.value.key, True)
    control.on_new_config_rcv(test_ip_2, ESP_VALUE_TYPE_KEYS.ANGLE_Z.value, DofName.LED.value.key, True)

# ______________________________________________________________________________________________ MAIN


def setup():
    print("[SETUP] --------------------------------------------- BEGIN")

    # ADD REMOTE ESP CONTROLLERS TO STRING CONTROL OBJECT
    add_esp_channels()

    # SETUP STRING CONTROL OBJECT
    control.setup()

    print("[SETUP] --------------------------------------------- COMPLETE\n")


def main_body():
    # main setup
    setup()

    # main loop
    print("[MAIN LOOP] --------------------------------------------- STARTING MAIN LOOP\n")
    while True:
        # execute CONTROLLERS loop
        control.loop()


def main():

    main_body()

    print("end")

    control.cleanup()


if __name__ == "__main__":
    main()
