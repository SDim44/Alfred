/*
  I2C Pinouts

  SDA -> A4
  SCL -> A5
*/

//Import the library required
#include <Wire.h>

//Slave Address for the Communication
#define SLAVE_ADDRESS 0x4
  

//Motor Pins
const int A1A = 5;//define pin D5 for A1A;
const int A1B = 6;//define pin D6 for A1B;

const int B1A = 9;//define pin D9 for B1A;
const int B1B = 10;//define pin D10 for B1B;


//Ultrasonic
float duration, ultrasonic_distance;

int trigPin = 2;//define pin D2 for Trigger
int echoPin = 4;//define pin D4 for Echo


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

// callback for received data
void receiveData(int byteCount) 
{
  while (Wire.available()) 
  {
    int c = Wire.read();
    Serial.println(c);
    Serial.println(ultrasonic_distance);

    if(ultrasonic_distance > 10)
    {
      if (c == 0)
      {
          Serial.println("STOP");
          digitalWrite(A1A,LOW); 
          digitalWrite(A1B,LOW);
          digitalWrite(B1A,LOW);
          digitalWrite(B1B,LOW);
          sendData("1");
      }
      else if(c == 1)
        {
          Serial.println("FORWARD");
          digitalWrite(A1A,HIGH); 
          digitalWrite(A1B,LOW);
          digitalWrite(B1A,HIGH);
          digitalWrite(B1B,LOW);
          sendData("1");
        }
        else if (c == 2)
          {
          Serial.println("TURN LEFT");
          digitalWrite(A1A,LOW); 
          digitalWrite(A1B,LOW);
          digitalWrite(B1A,HIGH);
          digitalWrite(B1B,LOW);
          sendData("1");
          }
        else if (c == 3)
          {
          Serial.println("TURN RIGHT");
          digitalWrite(A1A,HIGH); 
          digitalWrite(A1B,LOW);
          digitalWrite(B1A,LOW);
          digitalWrite(B1B,LOW);
          sendData("1");
          }
         else
         {
        Serial.println("Failed");
        Serial.println(c);
        sendData("0");
         }  
   }  
  }
}

// callback for sending data
void sendData(char x)
{
  Wire.write(x);
}


//Code Initialization
void setup() 
{
  Serial.begin(9600);
  Serial.println("STARTUP...");
  
  // initialize i2c as slave
  Serial.println("Slave-Address: ");
  Serial.print(SLAVE_ADDRESS);
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  //  Wire.onRequest(sendData);


  pinMode(trigPin, OUTPUT); // define trigger pin as output

  
  //Motor Pins
  pinMode(B1A,OUTPUT);// define pin as output
  pinMode(B1B,OUTPUT);
  
  pinMode(A1A,OUTPUT);
  pinMode(A1B,OUTPUT);

  digitalWrite(A1A,LOW);
  digitalWrite(A1B,LOW); 
  digitalWrite(B1A,LOW);
  digitalWrite(B1B,LOW);
}

void loop() {
  delay(100);

  ultrasonic_distance = ultrasonic();
  //Serial.print("Distance: : ");
  //Serial.print(ultrasonic_distance, 1); 
  //Serial.println(" cm");
} // end loop


//End of the program
