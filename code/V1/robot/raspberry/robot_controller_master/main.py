
import os
import time

from classes.control import Control
from classes.sensing import Sensing
from configs.robots.dof import DofName
from configs.robots.robots import siid,room


# ______________________________________________________________________________________________GLOBALS

# directory of the file. It's the same dicrectory of the RESTART.SH file
abs_path = os.path.dirname(os.path.abspath(__file__))
restart_file_name = "restart.sh"
path_to_restart = "./" + restart_file_name  # abs_path + "/restart.sh"
time_difference_ms = 5 # 5 ms
# Convert time difference to seconds (0.005 seconds)
time_difference_sec = time_difference_ms / 1000

# ______________________________________________________________________________________________ VALUES

# STRING IPS
test_ip_1 = "192.168.0.40"

test_ip_2 = "192.168.0.42"

# ______________________________________________________________________________________________ CREATE VIRTUAL ObJECTS

# INITIALIZE CONTROLS

# -- this variable contains the ROBOT config. Just comment out the robot you are coding for
#    and all the setup will be already implemented in it
robot = room.room
# robot = blackwing.blackwing

# -- this is the MAIN CLASS, the one handling all the logic
#control = Control(robot, path_to_restart)
sensing = Sensing(robot, path_to_restart)
control = Control(robot, path_to_restart)

def add_esp_channels():

    global control
    from configs.esps.esp_types import ESP_VALUE_TYPE_KEYS
    from configs.robots.dof import DofName
    control.on_new_config_rcv(test_ip_1, ESP_VALUE_TYPE_KEYS.ANGLE_X.value, DofName.PETALS.value.key, True)
    control.on_new_config_rcv(test_ip_1, ESP_VALUE_TYPE_KEYS.ANGLE_Y.value, DofName.EYE_X.value.key, True)
    #control.on_new_config_rcv(test_ip_1, ESP_VALUE_TYPE_KEYS.ANGLE_Z.value, DofName.LED.value.key, True)
    #control.on_new_config_rcv(test_ip_2, ESP_VALUE_TYPE_KEYS.ANGLE_X.value, DofName.PETALS.value.key, True)
    #control.on_new_config_rcv(test_ip_2, ESP_VALUE_TYPE_KEYS.ANGLE_Y.value, DofName.EYE_X.value.key, True)
    #control.on_new_config_rcv(test_ip_2, ESP_VALUE_TYPE_KEYS.ANGLE_Z.value, DofName.LED.value.key, True)

# ______________________________________________________________________________________________ MAIN


def setup():
    print("[SETUP] --------------------------------------------- BEGIN")

    # ADD REMOTE ESP CONTROLLERS TO STRING CONTROL OBJECT
    add_esp_channels()

    # SETUP STRING CONTROL OBJECT
    #control.setup()
    #sensing.setup()
   # print(sensing.send_sensor_signals())

    print("[SETUP] --------------------------------------------- COMPLETE\n")


def main_body():
    # main setup
    setup()

    # main loop
    print("[MAIN LOOP] --------------------------------------------- STARTING MAIN LOOP\n")
    while True:
       
        start_time = time.time()
        #every  5ms switch between control and sensing
        while  (time.time() - start_time) <= time_difference_sec:
            # execute CONTROLLERS loop
            control.loop()

       # while  (time.time() - start_time) <= (2 * time_difference_sec) and (time.time() - start_time) > time_difference_sec:
             # execute SENSING loop
         #   sensing.loop()


def main():

    main_body()

    print("end")

    #control.cleanup()


if __name__ == "__main__":
    main()
