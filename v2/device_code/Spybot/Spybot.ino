/*
  I2C Pinouts

  SDA -> A2
  SCL -> A1
*/

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>

Adafruit_MPU6050 mpu;


// Update these with values suitable for your network.

const char* ssid = "321Meins";
const char* password = "Mizzi123$";
const char* mqtt_server = "testipi";
String mac_address = WiFi.macAddress();

char authen[100] = "homestead/Authentication";
String authen_info = "description,MPU6050 and drive_simple on ESP8266;mac_address," + mac_address + ";baudrate,115200;driver,mpu5060@mqtt,drive_simple@mqtt,ultrasonic@mqtt";

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

//----------------------------------------------------------------------------------
//Motor Pins
const int A1A = 14;//define pin D5 for A1A;
const int A1B = 12;//define pin D6 for A1B;

const int B1A = 13;//define pin D7 for B1A;
const int B1B = 0;//define pin D3 for B1B;

//----------------------------------------------------------------------------------
//Motor Pins
int trigPin = 16;//define pin D0 for Trigger
int echoPin = 2;//define pin D4 for Echo

//---------------------------------------------------------------------------------
//Ultrasonic
float duration, ultrasonic_distance;

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
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//----------------------------------------------------------------------------------
float ultrasonic()
{
  //get ultrasonic distance
    digitalWrite(echoPin, LOW);   // set the echo pin LOW
    digitalWrite(trigPin, LOW);   // set the trigger pin LOW
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);  // set the trigger pin HIGH for 10μs
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);  // measure the echo time (μs)
    ultrasonic_distance = (duration/2.0)*0.0343;   // convert echo time to distance (cm)
    return ultrasonic_distance;
}


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
        digitalWrite(A1A,LOW); 
        digitalWrite(A1B,LOW);
        digitalWrite(B1A,LOW);
        digitalWrite(B1B,LOW);
    }
    else if((char)payload[0] == '1')
      {
        if(ultrasonic_distance > 100) 
        {
        Serial.println("FORWARD");
        digitalWrite(A1A,HIGH); 
        digitalWrite(A1B,LOW);
        digitalWrite(B1A,HIGH);
        digitalWrite(B1B,LOW);
        }
      }
      else if((char)payload[0] == '2')
        {
        Serial.println("TURN LEFT");
        digitalWrite(A1A,LOW); 
        digitalWrite(A1B,LOW);
        digitalWrite(B1A,HIGH);
        digitalWrite(B1B,LOW);
        }
      else if((char)payload[0] == '3')
        {
        Serial.println("TURN RIGHT");
        digitalWrite(A1A,HIGH); 
        digitalWrite(A1B,LOW);
        digitalWrite(B1A,LOW);
        digitalWrite(B1B,LOW);
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

void setup() {

  pinMode(trigPin, OUTPUT); // define trigger pin as output

  pinMode(A1A, OUTPUT);
  pinMode(A1B, OUTPUT);
  pinMode(B1A, OUTPUT);
  pinMode(B1B, OUTPUT);
  
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  Serial.println("STARTUP...");
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  digitalWrite(A1A,LOW); 
  digitalWrite(A1B,LOW);
  digitalWrite(B1A,LOW);
  digitalWrite(B1B,LOW);

//-----------------------------------------------------
// MPU
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);  
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
    //snprintf (msg, MSG_BUFFER_SIZE, "hello world #%ld", value);

    ultrasonic_distance = ultrasonic();
    Serial.print("Motor stopped!  Distance: : ");
    Serial.println(ultrasonic_distance, 1); Serial.println(" cm");

    
    
    /* Get new sensor events with the readings */
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
  
  
    String sensor_data= ("Acceleration:" + String(a.acceleration.x) + "," + String(a.acceleration.y) + "," + String(a.acceleration.z) + ";Rotation:" + String(g.gyro.x) + "," + String(g.gyro.y) + "," + String(g.gyro.z) + ";Temperature:" + String(temp.temperature) + ";Ultrasonic:" + String(ultrasonic_distance));
    
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
