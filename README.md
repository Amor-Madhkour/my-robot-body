# My (Robot) Body


General purpose system for digital remote control of social robots. 
The three main components are: 

- REMOTE CONTROLLERS: ESP32 modules with a number of sensors onboard streaming their control values to the robot
- ROBOT: A. a Raspberry Pi controller receiving data from the ESP32 controllers, and deploying them to the arduino board for actuations; B. and Arduino Mega board for direct control of the peripheries (motors, wheels, leds, and sensors). 
- SENSORY FEEDBACK: an Oculus Quest 2 Unity app to interpret the signals coming from the robot's sensors. 

The directory is structured as follows: 

## CODE
contains all the code of the project. 
The structure is the following: 
-> main function in the project (e.g. "control" or "robot")
  -> target platform (e.g. esp32 or arduino or raspberry)
    -> name of the specific project (e.g. "robot_controller_master" or "esp_channel")   



### EXPERIMENTS
contains a reference to all the experiments performed using this framework.
Within each experiment folder you can find documents on the setup and results such as
- questionnaires 
- answers
- plots/tables of elaborations of the results
