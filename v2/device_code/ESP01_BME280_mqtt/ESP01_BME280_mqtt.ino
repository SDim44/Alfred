/***************************************************************************
  Dimnik Stefan - 13.11.2020

  ESP01 mit BME280 -> Data per MQTT

  ***************************************************************************/
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)


String mac_address = WiFi.macAddress();

//----------------------------------------------------------------------------------
//Device Information

String authen_info = "description,ESP01 mit BME280;mac_address," + mac_address + ";baudrate,9600;driver,bme280@mqtt";


//----------------------------------------------------------------------------------
//BME Sensor
Adafruit_BME280 bme; // I2C
unsigned long delayTime;

//----------------------------------------------------------------------------------
//Wifi/MQTT Connection
const char* SSID = "321Meins";
const char* PSK = "Mizzi123$";
const char* MQTT_BROKER = "testipi";

char authen[30] = "homestead/Authentication";


WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
int value = 0;


//----------------------------------------------------------------------------------
//Fuctions

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(SSID);

  WiFi.begin(SSID, PSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//----------------------------------------------------------------------------------

void reconnect() {
  while (!client.connected()) {
    Serial.print("Reconnecting...");
    if (!client.connect("ESP8266Client")) {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}

//----------------------------------------------------------------------------------

void setup()
{
  Serial.begin(9600);
  Serial.println(F("BME280 test"));
  Wire.pins(0, 2);
  Wire.begin();

  bool status;

  // default settings
  status = bme.begin(0x76, &Wire);
  if (!status) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  }

  Serial.println("-- Default Test --");
  delayTime = 1000;

  Serial.println();

  delay(100); // let sensor boot up


//----------------------------------------------------------------------------------
setup_wifi();
client.setServer(MQTT_BROKER, 1883);
}


//----------------------------------------------------------------------------------
void loop() {
  //printValues();
  //delay(delayTime);

  //----------------------------------------------------------------------------------
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float tem = bme.readTemperature();
  float pre = (bme.readPressure() / 100.0F);
  float hpa = (bme.readAltitude(SEALEVELPRESSURE_HPA));
  float hum = (bme.readHumidity());

  String msg= ("Temperature," + String(tem) + ";Pressure," + String(pre) + ";Approx-Altitude," + String(hpa) + ";Humidity," + String(hum));
  char message[100];
  msg.toCharArray(message,100);  
  char authen_info_char[100];
  authen_info.toCharArray(authen_info_char,100);

  String sensor = ("homestead/sensor/" + mac_address);
  String logging = ("homestead/log/" + mac_address);
  char sensor_topic[70];
  sensor.toCharArray(sensor_topic,70);
  char log_topic[30];
  logging.toCharArray(log_topic,30);

  Serial.println(sensor);
  Serial.println(sensor_topic);
  Serial.println(authen_info_char);
  Serial.println(message);
  client.publish(sensor_topic, message);
  client.publish(authen, authen_info_char);
  
  
  delay(5000);
}
