
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>


//---- RESET BUTTON ESP8266 CONTROLLER ----



// ______________________________________________________________________________________________STATIC IP
//Static IP address configuration

//      IP - DOF MAPPINGS
// -- STRING CONTROLS
// IP = 192.168.1.40 -> FORWARD BASE
// IP = 192.168.1.41 -> STRAFE BASE
// IP = 192.168.1.42 -> ANGULAR BASE
// IP = 192.168.1.43 -> SHOULDER SERVO
// IP = 192.168.1.44 -> ELBOW SERVO
// IP = 192.168.1.45 -> CLAW SERVO
// -- BUTTONS
// IP = 192.168.1.20 -> RESET BUTTON
// IP = 192.168.1.30 -> PAUSE BUTTON

IPAddress staticIP(192, 168, 1, 20); // ESP static ip
IPAddress gateway(192, 168, 1, 1);   // IP Address of your WiFi Router (Gateway)
IPAddress subnet(255, 255, 255, 0);  // Subnet mask
IPAddress primaryDNS(192, 168, 1, 1);  // DNS 1
IPAddress secondaryDNS(8, 8, 8, 8);  // DNS 2

// RASP IP
#define RASP_IP "192.168.1.6"  //"192.168.1.3"
#define RASP_PORT 44444  // my mac os udp port is: 49242

// declare the list of all IPs that the RESET message should be sent to:
// IPs of all the strings, and the IP of the RASP
char *reset_ips[] = { 
    RASP_IP, 
    "192.168.1.40",  
    "192.168.1.41",  
    "192.168.1.42",  
    "192.168.1.43",  
    "192.168.1.44",  
    "192.168.1.45"
};

int num_IPs = sizeof(reset_ips)/sizeof(reset_ips[0]);


// ______________________________________________________________________________________________LEDS

const byte ledPinOn = 12;    // digital GPI12 - D6 - LED ON when ESP ON
const byte ledPinWiFi = 13;  // digital GPI13 - D7 - LED ON when ESP connected to WIFI 
const byte ledPinReset = 15; // digital GPI15 - D8 - LED BLINKS when RESET (i.e. when button pressed)

byte leds[] = {ledPinOn, ledPinWiFi, ledPinReset};

int num_leds = sizeof(leds)/sizeof(leds[0]);


void blink_led(byte led_pin, int delay_t, int num_times = 1) {
  
  for (int i = 0; i < num_times; i++) {
    digitalWrite(led_pin, HIGH);
    delay(delay_t);
    digitalWrite(led_pin, LOW);
    delay(delay_t);
  }
}

void blink_leds(int delay_t, int num_times = 1) {

  for (int i = 0; i < num_times; i++) {
  
    for (int j = 0; j < num_leds; j++)
      digitalWrite(leds[j], HIGH);

    delay(delay_t);
  
    for (int j = 0; j < num_leds; j++)
      digitalWrite(leds[j], LOW);
      
    delay(delay_t);
     
  }
}

void setup_leds() {

  Serial.println("[SETUP LEDS] - start");


  for (int j = 0; j < num_leds; j++)
    pinMode(leds[j], OUTPUT);
  
  blink_leds(100, 6);

  digitalWrite(ledPinOn, HIGH);
  digitalWrite(ledPinWiFi, LOW);
  digitalWrite(ledPinReset, LOW);

  Serial.println("[SETUP LEDS] - complete\n");
}


// ______________________________________________________________________________________________WIFI

// connect to wifi with static IP

#define WIFI_SSID "Triskarone"
#define WIFI_PSW "triskarone"
#define MY_UDP_PORT 4210
#define IN_SIZE 255
#define OUT_SIZE 255

char RASP_AKNOWLEDGE[IN_SIZE] = "OK";  // added last value for convention, which will also be in the "in_packet"
char RESET_MSG[IN_SIZE] = "RESET";

WiFiUDP UDP;

char in_packet[IN_SIZE];
char out_packet[OUT_SIZE];

void write_char_udp(char msg[], char ip[] = RASP_IP, int port = RASP_PORT){
    UDP.beginPacket(ip, port);
    UDP.write(msg);
    UDP.endPacket();
}

void write_string_udp(String msg, char ip[] = RASP_IP, int port = RASP_PORT){
    UDP.beginPacket(ip, port);
    UDP.print(msg);
    UDP.endPacket();
}

void write_int_udp(int value, char ip[] = RASP_IP, int port = RASP_PORT){
    itoa(value, out_packet, 10);
  
    write_char_udp(out_packet, ip, port);
}

bool read_udp_non_blocking(){
  
  int packetSize = UDP.parsePacket();

  bool received = false;
  
  if (packetSize) {
    Serial.print("Received packet! Size: ");
    Serial.println(packetSize); 
    int len = UDP.read(in_packet, IN_SIZE);  // the value is written in the BUFFER specificed as the first argument ("in_packet" in our case)
    if (len > 0)
    {
      in_packet[len] = '\0';
      received = true;
    }
    Serial.print("Packet received: ");
    Serial.print(in_packet);
    Serial.print(" - with size: ");
    Serial.print(len);
    Serial.print(" - current size: ");
    Serial.println(sizeof(in_packet));
    Serial.print(" - ACKNOWLEDGE: ");
    Serial.print(RASP_AKNOWLEDGE);
    Serial.print(" - with size: ");
    Serial.println(sizeof(RASP_AKNOWLEDGE));
  }

  return received;
}


void connect_to_wifi(){

  Serial.println("[CONNECT TO WIFI] - begin");

  // Prevent connecting to wifi based on previous configuration
  WiFi.disconnect();  

  // setup with STATIC IP
  bool wifi_configured = false;
  while (!wifi_configured)
  {
    if (!WiFi.config(staticIP, gateway, subnet, primaryDNS, secondaryDNS)) {
      Serial.println("[CONNECT TO WIFI] - failed to configure STATIC IP");
      // blink fast to signal failed STATIC IP setup
      blink_led(ledPinWiFi, 50, 5);
      delay(1000);
    } else {
      wifi_configured = true;
      Serial.println("[CONNECT TO WIFI] - configured STATIC IP");
    }
  }

  // set the ESP8266 to be a WiFi-client
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PSW);

  // Attempting connection to WiFi
  Serial.println("Trying to connect ...");
  while (WiFi.status() != WL_CONNECTED) {
    
    // blink the WIFI led while awaiting for connection once (per loop)
    // NB the "blink_led" method contains the delay
    blink_led(ledPinWiFi, 250);
    
    Serial.print(".");
  }

  // turn WIFI led OFF.
  // so, if LED stays off after blinking, it's because the UDP connection crashed the ESP
  digitalWrite(ledPinWiFi, LOW);

  // notify being connected to WiFi;
  Serial.print("Connected to Local Network - ESP IP: ");
  Serial.println(WiFi.localIP());

  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);

  // Begin listening to UDP port
  UDP.begin(MY_UDP_PORT);
  Serial.print("UDP on:");
  Serial.println(MY_UDP_PORT);

  // turn WIFI led ON: WIFI connection successful
  digitalWrite(ledPinWiFi, HIGH);
  Serial.println("[CONNECT TO WIFI] - complete\n");
}


// ______________________________________________________________________________________________BUTTON

// button pin
const byte btn_pin = 14;  // D5 pin - GPIO 16

// button states
byte prev_button_state;
byte current_button_state;

// reset method. Called on button released
// sends "RESET" msg to all reveiver IPs: strings and rasp
void reset(){

  Serial.println("[RESET] - sending RESET MSG to IPs: ");
  for (int i = 0; i < num_IPs; i++)
  {
    int port;

    if (reset_ips[i] == RASP_IP)
      port = RASP_PORT;
    else
      port = MY_UDP_PORT;  // all esps use the same port

    write_char_udp(RESET_MSG, reset_ips[i], port);

    Serial.print("  -- [RESET MSG] - sent to IP: " + String(reset_ips[i]) + " - and port: " + String(port));
  }
  // blink red led
  blink_led(ledPinReset, 40, 20);

  Serial.println("[RESET] - complete");
}

// setup button
void setup_btn() {
  Serial.println("[SETUP BUTTON] - begin");

  pinMode(btn_pin, INPUT);

  Serial.println("[SETUP BUTTON] - complete\n");
}

// check button method. Called in the loop function
void check_button_released(){

  current_button_state = digitalRead(btn_pin);
  if (current_button_state != prev_button_state && current_button_state == LOW)
    reset();

  prev_button_state = current_button_state;
}


// ______________________________________________________________________________________________MAIN


void initialize(){
  Serial.println("[INIZIALIZE VARIABLES] - begin");
  
  prev_button_state = LOW;
  current_button_state = LOW;
  
  Serial.println("[INIZIALIZE VARIABLES] - complete\n");
}

void setup(){

  // setup serial
  Serial.begin(115200);
  delay(200);
  Serial.println("[SETUP] - begin\n");

  // initialize variables
  initialize();

  // setup leds
  setup_leds();

  // initialize internet connection
  connect_to_wifi();

  // setup button
  setup_btn();

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.println("[SETUP] - complete\n");
}

void loop(){

  check_button_released();

}