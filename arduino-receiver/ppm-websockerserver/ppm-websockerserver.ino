// https://github.com/steveio/arduino/blob/master/ESP8266RotaryEncoderServo/ESP8266RotaryEncoderServo.ino


#include <WebSocketsServer.h>
#include <ESP8266WiFi.h>
#include "config.h"

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
const char* ssid2 = WIFI_SSID2;
const char* password2 = WIFI_PASSWORD2;

const char* deviceName = DEVICE_NAME;

WebSocketsServer webSocket = WebSocketsServer(WEBSOCKETPORT);

bool connected = false;
uint8_t cam_num;

// ==============================================
// ==============================================
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
#define sigPin SIGPN //set PPM signal output pin on the arduino

volatile unsigned long next;
unsigned int alivecount = 0;

int ppm[CHANNEL_NUMBER];


/// Pin Settings ///
int LEDPin = 2;
int buttonPin = 0;
bool LEDState = false;
int lastUpdate = 0;
int lastTransmission = 0;
// ==============================================
// Data Package settings

// data message
typedef struct data_t
{
  int pitch;
  int yaw;
  int throttle;
  int roll;
  int aux1;
  int aux2;
  int aux3;
  int aux4;
};

// message packaging / envelope
typedef union packet_t {
  struct data_t data;
  uint8_t packet[sizeof(struct data_t)];
};

#define PACKET_SIZE sizeof(struct data_t)

union packet_t receiveMsg;

// buffer
uint8_t byteArray[PACKET_SIZE];



// ==============================================
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();


  // scan....
  int n = WiFi.scanNetworks();
  for (int i = 0; i < n; ++i) {
    if (WiFi.SSID(i)== ssid ) {
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid,password); //trying to connect the modem
      Serial.print("Connecting to ");
      Serial.println(ssid);
      break;
    }
    if (WiFi.SSID(i)== ssid2) {
      WiFi.mode(WIFI_STA);
      WiFi.begin(ssid2,password2); //trying to connect the modem
      Serial.print("Connecting to ");
      Serial.println(ssid2);
     break;
    }
  }


  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LEDPin, LEDState);
    LEDState = !LEDState;
    delay(500);
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}
// ==============================================
// https://github.com/Links2004/arduinoWebSockets/issues/192

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {

  switch (type) {
    case WStype_DISCONNECTED:
      Serial.printf("[%u] Disconnected!\n", num);
      break;
    case WStype_CONNECTED:
      Serial.printf("[%u] Client Connected!\n", num);
      cam_num = num;
      connected = true;
      break;
    case WStype_TEXT:
      Serial.printf("[%u] get Text: %s\n", num, payload);
      break;

    case WStype_BIN:
      readByteArray(payload);
//      Serial.print(ppm[0]);
//      Serial.print(" ");
//      Serial.print(ppm[1]);
//      Serial.print(" ");
//      Serial.print(ppm[2]);
//      Serial.print(" ");
//      Serial.print(ppm[3]);
//      Serial.print(" ");
//      Serial.print(ppm[4]);
//      Serial.print(" ");
//      Serial.print(ppm[5]);
//      Serial.print(" ");
//      Serial.print(ppm[6]);
//      Serial.print(" ");
//      Serial.print(ppm[7]);
//      Serial.println();
      break;

      //        case WStype_ERROR:
      //        case WStype_FRAGMENT_TEXT_START:
      //        case WStype_FRAGMENT_BIN_START:
      //        case WStype_FRAGMENT:
      //        case WStype_FRAGMENT_FIN:


  }
}

// ==============================================
// read bytes from buffer
void readByteArray(uint8_t * byteArray)
{
  for (int i = 0; i < PACKET_SIZE; i++)
  {
    receiveMsg.packet[i] = byteArray[i];
  }

  // Update ppm signals
  ppm[0] = receiveMsg.data.pitch;
  ppm[1] = receiveMsg.data.yaw;
  ppm[2] = receiveMsg.data.throttle;
  ppm[3] = receiveMsg.data.roll;
  ppm[4] = receiveMsg.data.aux1;
  ppm[5] = receiveMsg.data.aux2;
  ppm[6] = receiveMsg.data.aux3;
  ppm[7] = receiveMsg.data.aux4;

  if (receiveMsg.data.aux1 > 1500) digitalWrite(LEDPin, true);
  if (receiveMsg.data.aux1 < 1500) digitalWrite(LEDPin, false);

  lastUpdate = millis();

}
// ==============================================

void setup() {

  Serial.begin(115200);

  pinMode(LEDPin, OUTPUT);
  pinMode(buttonPin, INPUT);
  pinMode(sigPin, OUTPUT);

  // Connect to wifi
  setup_wifi();
  setup_PPM();

  // Start Websocket Server
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
  Serial.println("WebsocketServer Online :)");
}
// ==============================================
void loop() {
  // let the websockets client check for incoming messages
  webSocket.loop();

  // If a too long timeout occurs, reset websocket!
  if ((millis() - lastUpdate) >= 2000 ) {
    //Serial.print("Timeout! Resetting commands");
    lastUpdate = millis();
    default_values();
  }

  // Transmit RSSI
  if(connected == true && (millis() - lastTransmission) >= 2000){
    long rssi = WiFi.RSSI();
    String rssi_str = String(rssi);
    webSocket.broadcastTXT(rssi_str);
  } 
  
}

// ==============================================
// PPM Fun
// ==============================================


// ==============================================
void default_values() {
  // Default values
  ppm[0] = 1500;
  ppm[1] = 1500;
  ppm[2] = 1000;
  ppm[3] = 1500;
  ppm[4] = 1000;
  ppm[5] = 1000;
  ppm[6] = 1000;
  ppm[7] = 1000;
}
// ==============================================
void inline ppmISR(void) {
  static boolean state = true;

  if (state) {  //start pulse
    digitalWrite(sigPin, onState);
    next = next + (PULSE_LENGTH * CPU_MHZ);
    state = false;
    alivecount++;
  }
  else { //end pulse and calculate when to start the next pulse
    static byte cur_chan_numb;
    static unsigned int calc_rest;

    digitalWrite(sigPin, !onState);
    state = true;

    if (cur_chan_numb >= CHANNEL_NUMBER) {
      cur_chan_numb = 0;
      calc_rest = calc_rest + PULSE_LENGTH;//
      next = next + ((FRAME_LENGTH - calc_rest) * CPU_MHZ);
      calc_rest = 0;
      // digitalWrite(DEBUGPIN, !digitalRead(DEBUGPIN));
    }
    else {
      next = next + ((ppm[cur_chan_numb] - PULSE_LENGTH) * CPU_MHZ);
      calc_rest = calc_rest + ppm[cur_chan_numb];
      cur_chan_numb++;
    }
  }
  timer0_write(next);
}
// ==============================================

void setup_PPM() {
  // PPM
  digitalWrite(sigPin, !onState); //set the PPM signal pin to the default state (off)

  noInterrupts();
  timer0_isr_init();
  timer0_attachInterrupt(ppmISR);
  next = ESP.getCycleCount() + 1000;
  timer0_write(next);
  for (int i = 0; i < CHANNEL_NUMBER; i++) {
    ppm[i] = CHANNEL_DEFAULT_VALUE;
  }
  interrupts();

}
