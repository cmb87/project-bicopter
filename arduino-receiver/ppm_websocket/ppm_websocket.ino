#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WebSocketsClient.h>
#include <SocketIoClient.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>
#include <MSP.h>

// =================== CONFIG =================== 
/////////////////////////////////////
////// USER DEFINED VARIABLES //////
///////////////////////////////////
/// WIFI Settings ///
const char* ssid     = "";
const char* password = "";

/// Socket.IO Settings ///
char host[] = "192.168.2.138"; // Socket.IO Server Address
int port = 5000; // Socket.IO Port Address

/// Pin Settings ///
int LEDPin = 2;
int buttonPin = 0;
bool LEDState = false;

// ------------------------------------------------
/////////////////////////////////////
////// ESP32 Socket.IO Client //////
///////////////////////////////////

SocketIoClient webSocket;

// Use WiFiClient class to create TCP connections
WiFiClient client;

// ------------------------------------------------
/////////////////////////////////////
////// PPM //////
///////////////////////////////////
// ESP8266 ESP-01S über CH340G USB-Konverter! 
/* Set these to your desired credentials. */

#define CPU_MHZ 80
#define CHANNEL_NUMBER 8  //set the number of chanels
#define CHANNEL_DEFAULT_VALUE 1500  //set the default servo value
#define FRAME_LENGTH 22500  //set the PPM frame length in microseconds (1ms = 1000µs)
#define PULSE_LENGTH 300  //set the pulse length
#define onState 0  //set polarity of the pulses: 1 is positive, 0 is negative
#define sigPin 4 //set PPM signal output pin on the arduino


volatile unsigned long next;
unsigned int alivecount=0;

int ppm[CHANNEL_NUMBER];

// ------------------------------------------------
void inline ppmISR(void){
  static boolean state = true;

  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    next = next + (PULSE_LENGTH * CPU_MHZ);
    state = false;
    alivecount++;
  } 
  else{  //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;
  
    digitalWrite(sigPin, !onState);
    state = true;

    if(cur_chan_numb >= CHANNEL_NUMBER){
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;// 
      next = next + ((FRAME_LENGTH - calc_rest) * CPU_MHZ);
      calc_rest = 0;
     // digitalWrite(DEBUGPIN, !digitalRead(DEBUGPIN));
    }
    else{
      next = next + ((ppm[cur_chan_numb] - PULSE_LENGTH) * CPU_MHZ);
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }     
  }
  timer0_write(next);
}

// =================== SETUP =================== 
// ------------------------------------------------
void setup() {

  Serial.begin(115200);
  Serial.println("Initializing");
  
  delay(1000);

  pinMode(LEDPin, OUTPUT);
  pinMode(buttonPin, INPUT);

  // Connect to Wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LEDPin, LEDState);
    LEDState = !LEDState;
    delay(500);
  }
  
  // PPM
  pinMode(sigPin,OUTPUT);
  digitalWrite(sigPin, !onState); //set the PPM signal pin to the default state (off)

  noInterrupts();
  timer0_isr_init();
  timer0_attachInterrupt(ppmISR);
  next=ESP.getCycleCount()+1000;
  timer0_write(next);
  for(int i=0; i<CHANNEL_NUMBER; i++){
    ppm[i]= CHANNEL_DEFAULT_VALUE;
  }
  interrupts();

  // Setup 'on' listen events
  webSocket.begin(host, port);
  
  webSocket.on("connect", socket_connected);
  webSocket.on("control", socket_controlHandler);
  webSocket.on("disconnect", socket_disconnected);
  webSocket.on("toggleled", socket_statechange);

}
// =================== MAIN LOOP =================== 
// ------------------------------------------------
void loop() {
  // put your main code here, to run repeatedly:
  webSocket.loop();
}



// =================== FUNCTIONS =================== 
// ----------------
void socket_statechange(const char * payload, size_t length) {
  digitalWrite(LEDPin, LEDState);
  LEDState = !LEDState;
}

// ----------------
void socket_connected(const char * payload, size_t length) {
}
// ----------------
void socket_disconnected(const char * payload, size_t length) {
}
// ----------------
void socket_controlHandler(const char * payload, size_t length) {

//   Serial.print(payload);
  
// https://arduinojson.org/v6/assistant/

  DynamicJsonDocument doc(128);
  deserializeJson(doc, payload);
  
//  MultiWii
// PITCH,YAW,THROTTLE,ROLL,AUX1,AUX2,AUX3,AUX4,8,9,10,11
  ppm[0] = doc[0]; // 1500
  ppm[1] = doc[1]; // 1500
  ppm[2] = doc[2]; // 1599
  ppm[3] = doc[3]; // 1414
  ppm[4] = doc[4]; // 1500
  ppm[5] = doc[5]; // 1400
  ppm[6] = doc[6]; // 1500
  ppm[7] = doc[7]; // 1400

}
