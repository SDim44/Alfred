/*

*/

#include <Wire.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>


#define SLAVE_ADDRESS 0x6


// Update these with values suitable for your network.

const char* ssid = "321Meins";
const char* password = "Mizzi123$";
const char* mqtt_server = "testipi";
String mac_address = WiFi.macAddress();

char authen[100] = "homestead/Authentication";
String authen_info = "description,drive_simple on Arduino over ESP01;mac_address," + mac_address + ";baudrate,115200;driver,drive_simple@mqtt";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
int value = 0;


//----------------------------------------------------------------------------------
//Fuctions
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.print("MAC adress: ");
  Serial.println(mac_address);
}

//----------------------------------------------------------------------------------

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  
  // Set Motor 
   
    if ((char)payload[0] == '0')
    {
        Serial.println("STOP");
        sendData(0);
    }
    else if((char)payload[0] == '1')
      {
        Serial.println("FORWARD");
        sendData(1);
      }
      else if((char)payload[0] == '2')
        {
        Serial.println("TURN LEFT");
        sendData(2);
        }
      else if((char)payload[0] == '3')
        {
        Serial.println("TURN RIGHT");
        sendData(3);
        }
       else
       {
      Serial.println("Failed");
      Serial.println((char)payload[0]);
       }  
}

//----------------------------------------------------------------------------------

void reconnect() {

  String actuator = ("homestead/actuator/" + mac_address);
    char actuator_topic[70];
    actuator.toCharArray(actuator_topic,70);

    String logging = ("homestead/log/" + mac_address);
  char log_topic[30];
  logging.toCharArray(log_topic,30);
    
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish(log_topic, "SPYBOT IS ONLINE!");
      // ... and resubscribe
      client.subscribe(actuator_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void receiveData(int byteCount) 
{
  while (Wire.available()) 
  {
    int c = Wire.read();
    Serial.println(c);   
  } 
}

// callback for sending data
void sendData(int x) 
{
  Serial.print("I²C send: ");
  Serial.println(x);
  Wire.beginTransmission(0x4);
  Wire.write(x);
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);
  Serial.println("STARTUP...");
  Serial.println("Slave-Address: ");
  Serial.print(SLAVE_ADDRESS);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  Wire.pins(0, 2);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
}


void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();   


    unsigned long now = millis();
    if (now - lastMsg > 2000) {
      lastMsg = now;
      ++value;
    
    
      String sensor_data= ("NO DATA");
      
      char message[100];
      sensor_data.toCharArray(message,100);  
      char authen_info_char[100];
      authen_info.toCharArray(authen_info_char,100);
    
      String sensor = ("homestead/sensor/" + mac_address);
      char sensor_topic[70];
      sensor.toCharArray(sensor_topic,70);
    
      String logging = ("homestead/log/" + mac_address);
      char log_topic[30];
      logging.toCharArray(log_topic,30);
    
      client.publish(sensor_topic, message);
      client.publish(authen, authen_info_char);
  }
}
