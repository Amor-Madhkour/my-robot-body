# My (Robot) Body

General purpose system for digital remote control of social robots. 
The three main components are: 

- REMOTE CONTROLLERS: ESP32 modules with a number of sensors onboard streaming their control values to the robot
- ROBOT: A. a Raspberry Pi controller receiving data from the ESP32 controllers, and deploying them to the arduino board for actuations; B. and Arduino Mega board for direct control of the peripheries (motors, wheels, leds, and sensors). 
- SENSORY FEEDBACK: an Oculus Quest 2 Unity app to interpret the signals coming from the robot's sensors. 
