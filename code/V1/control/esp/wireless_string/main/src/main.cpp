
#include <Arduino.h>
#include <ESPUDP.h>



//---- STRING CONTROL ESP CONTROLLER ----



// the ESP "virtual strings" send data via WIFI to the raspberry. 
// each ESP has a unique ID.
// the first message it sends to RASP is its ID. 
// the ID must be manually set from the code before uploading. 
// A variation is to have raspberry wait for connections and then assign values to each 
// (OR we could use the last digits of the IP..)


// ______________________________________________________________________________________________ GLOBALS


// the current value of the string reading
uint32_t current_value = 0;

// MSGs
char presentation_msg[] = "hallo";
char RASP_AKNOWLEDGE[IN_SIZE] = "OK";  // added last value for convention, which will also be in the "in_packet"
char RESET_MSG[IN_SIZE] = "RESET";

// ______________________________________________________________________________________________ NETWORKING
//Static IP address configuration

//      IP - DOF MAPPINGS
// IP = 192.168.1.40 -> FORWARD BASE
// IP = 192.168.1.41 -> STRAFE BASE
// IP = 192.168.1.42 -> ANGULAR BASE
// IP = 192.168.1.43 -> SHOULDER SERVO
// IP = 192.168.1.44 -> ELBOW SERVO
// IP = 192.168.1.45 -> CLAW SERVO
// -- BUTTONS
// IP = 192.168.1.20 -> RESET BUTTON
// IP = 192.168.1.30 -> PAUSE BUTTON

const IPAddress staticIP(192, 168, 0, 40);  // this device static IP

const IPAddress defaultDestinationIP(192, 168, 0, 6);  // RASP IP 
const int raspPort = 44444;  // my mac os udp port is: 49242
 
// last three inputs are the LED PINS
EspUdp espUdp(
    staticIP,
    defaultDestinationIP,
    raspPort,
    12, 
    13, 
    15
);

void checkReset() {
    if (espUdp.udp_msg_equals_to(RESET_MSG)) {

      Serial.println("[checkReset] - received RESET message: '" + String(RESET_MSG) + "'.\n... RESETTING ...");
      ESP.restart();
    }
}


// ______________________________________________________________________________________________ENCODER
const uint8 encoderPinA = 4;  // outputA digital GPIO4 - D2
const uint8_t encoderPinB = 5;  // outoutB digital GPIO5 - D1
const uint8_t encoderSW = 14;   // SW (bottone) connesso al pin GPI14 - D5

int encoderCount = 0; // Contatore
int actCLKState; // Lettura attuale del canale CLK (A)
int prevCLKState; // Lettura precedente del canale CLK (A)

#define readA digitalRead(encoderPinA)
#define readB digitalRead(encoderPinB)

ICACHE_RAM_ATTR void CLKChanged() {
  
  int actCLKState = readA;// Leggo il canale A (CLK)

  // Questo if serve per gestire chiamate multiple alla routine di interrupt 
  // causate dal cosiddetto bouncing: ogni volta che si ruota l'albero vengono 
  // in realtà generate diverse variazioni (per ognuna viene scatenato
  // l'interrupt!), dovute al funzionamento meccanico del rotore. Si possono 
  // determinare effetti indesiderati come ad esempio la ripetizione di numeri 
  // ma con questo IF vengono evitati.
  if (prevCLKState != actCLKState) {
    
      encoderCount += (actCLKState == readB ? 1 : -1); 
      
      // SEND TO -EACH- ROBOT
      // Serial.println(encoderCount);
      espUdp.write_int_udp(encoderCount);
      
      prevCLKState = actCLKState;
    }
}

// ICACHE_RAM_ATTR void SWPressed() {
  
//   Serial.println("SW Pressed!");
// }

void setup_encoder(){
  
  pinMode(encoderPinA, INPUT); 
  pinMode(encoderPinB, INPUT);
  pinMode(encoderSW, INPUT_PULLUP);
  
  attachInterrupt(digitalPinToInterrupt(encoderPinA), CLKChanged, CHANGE);
  // attachInterrupt(digitalPinToInterrupt(encoderSW), SWPressed, FALLING);

  prevCLKState = readA;  
}


// ______________________________________________________________________________________________MAIN


void initialize(){

  current_value = 0;
}

void setup() {

  // SERIAL
  Serial.begin(115220);
  delay(200);
  Serial.println("SETUP --- --- --- BEGIN");

  // initialize variables
  initialize();

  // ESP UDP
  espUdp.setup();
  
  // setup encoder
  delay(200);
  setup_encoder();

  // wait for a few seconds before starting
  delay(100);
  Serial.println("SETUP --- --- --- COMPLETE");
}

void loop() {

  // 1. check for UDP essages
  // - check if RESET MSG is received
  noInterrupts();
  if (espUdp.read_udp_non_blocking())
    checkReset();
  interrupts();
  
  // interrupts can work passively here
  delay(500);
}
