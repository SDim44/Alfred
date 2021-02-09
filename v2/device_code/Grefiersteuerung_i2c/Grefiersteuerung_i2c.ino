#include <Servo.h>
#include <Wire.h>

#define MOTORANZAHL 6
#define SLAVE_ADDRESS 0x8
Servo Motor[MOTORANZAHL];// Gesamtzahl der Servos

byte Motorpin[MOTORANZAHL] = {3, 4, 5, 10, 11, 12};
byte Motorposition[MOTORANZAHL];
byte aktuellerMotor = 0, Position = 0, EingabeWinkel = 0;

int axis;
int angle;


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

   for (byte i = 0; i < MOTORANZAHL; i++)
  {
    pinMode(Motorpin[i], OUTPUT);
    Motor[i].attach(Motorpin[i]); // Motorobjekte mit den
    // entsprechenden
  } // Anschlusspins
  // initialisieren.

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
      axis = (c/100) -1;
      angle = c - (axis*100);

      if(axis >= 0 and axis <=5)
      {
        if(angle >= 0 and angle <=180)
        {
        Motor[axis].write(angle);
        Motorposition[axis] = angle;
        }
      }
      
      sendData(Motorposition);
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
