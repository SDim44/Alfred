#include <Servo.h>
#include <Wire.h>


#define SLAVE_ADDRESS 0x5
unsigned long tstamp = 0;
bool rgbled_on = 0;
Servo servo_pin_2; //Servo Pin

int i;
int RED = 4;
int GREEN = 5;
int BLUE = 6;


void setup()
{
  Serial.begin(9600);
  Serial.println("STARTUP...");
  Serial.println("Slave-Address: ");
  Serial.print(SLAVE_ADDRESS);
  
  Wire.begin(SLAVE_ADDRESS);
  Wire.begin(SLAVE_ADDRESS);
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  //  Wire.onRequest(sendData);

  servo_pin_2.attach(2, 530, 2600);
  servo_pin_2.write( 0 );

}

void loop() {

  delay(100);

}

void receiveData(int byteCount) 
{
  while (Wire.available()) 
  {
    int c = Wire.read();
    Serial.println(c);
    if (c != 9999)
    {
      servo_pin_2.write( c );
      sendData("1");
    }
    else
    {
      sendData("0");
    }
    
  } 
}

// callback for sending data
void sendData(char x) 
{
  Wire.write(x);
}
