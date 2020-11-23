#include <Servo.h>

//LED Pins
#define RED      5
#define GREEN    4
#define BLUE     3

unsigned long tstamp = 0;
bool rgbled_on = 0;
Servo servo_pin_2; //Servo Pin


int i;

void setColor(int redValue, int greenValue, int blueValue)
{
  analogWrite(RED, redValue);
  analogWrite(GREEN, greenValue);
  analogWrite(BLUE, blueValue);
}

void setblink(int redValue, int greenValue, int blueValue)
{

  int blink_delay = 3000;
  if (millis() > (tstamp + blink_delay))
  {
    rgbled_on = !rgbled_on;
    tstamp = millis();
  }
  if (rgbled_on == 1)
  {
    setColor(255, 0, 0);
  }
  else
  {
    setColor(0, 0, 0);
  }
}


void setup()
{

  Serial.begin(9600);
  servo_pin_2.attach(2, 530, 2600);
  servo_pin_2.write( 0 );
  setblink(0, 255, 0);
}


void loop() {
  //Seriell Daten empfangen und auswerten
  if (Serial.available() > 0)
  {
    char data;
    String buf = Serial.readStringUntil('\n');
    int n = buf.length();
    char string[n + 1];
    strcpy(string, buf.c_str());
    char delimiter[] = ",";
    char *ptr;
    int command[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    // initialisieren und ersten Abschnitt erstellen
    ptr = strtok(string, delimiter);
    int j = 0;
    while (ptr != NULL)
    {
      command[j] = atoi(ptr);
      ptr = strtok(NULL, delimiter);
      j++;
    }

    //Serielle Befehle ausführen
    setColor(0, 255, 0);

    if (command[0] == 99)
    {
      Serial.print("Greifer/btn1,Auf,1,0/btn2,Zu,0,0/scale1,Grad,0,40\n");
    }
    else if (command[0] == 0)
    {
      servo_pin_2.write( 0 );
    }
    else if (command[0] == 1)
    {
      servo_pin_2.write( command[1] );
    }

    command[0] = 0;
  }
  else
  {
    setblink(255, 0, 0);
  }



}
