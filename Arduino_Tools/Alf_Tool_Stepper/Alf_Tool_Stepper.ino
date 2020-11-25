#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//LED Pins
#define RED      5
#define GREEN    4
#define BLUE     3

//Stepper Pins
#define IN1      8
#define IN2      9
#define IN3      10
#define IN4      11
#define STEPS    2038

#define DATA 50

//serial variablen
char Data[DATA];

//stepper variablen
boolean moveClockwise = true;
int Steps = 0;
boolean Direction = true;
unsigned long last_time;
unsigned long currentMillis ;
int steps_left = 4095;
long time;

//led variablen
unsigned long tstamp  =   0;
bool rgbled_on        =   0;


//Stepper stepper(STEPS, IN1, IN2, IN3, IN4);

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

void stepper(int xw) {
  for (int x = 0; x < xw; x++) {
    switch (Steps) {
      case 0:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;
      case 1:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, HIGH);
        break;
      case 2:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;
      case 3:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        break;
      case 4:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;
      case 5:
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;
      case 6:
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;
      case 7:
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        break;
      default:
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
        break;
    }
    SetDirection();
  }
}
void SetDirection() {
  if (Direction == 1) {Steps++;}
  if (Direction == 2) {Steps--;}
  if (Steps > 7) {Steps = 0;}
  if (Steps < 0) {Steps = 7;}
}


void setup()
{
  Serial.begin(9600);
  setblink(0, 255, 0);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
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
    if (command[0] == 99)
    {
      Serial.print("Stepper/btn1,Links,1,0/btn2,Rechts,2,0/scale1,Speed,0,40/scale2,Steps,0,4000\n");
    }
    else
    {
      steps_left = command[2];
      Serial.print("\nsteps: ");
      Serial.print(command[2]);
      Serial.print("\ndirection: ");
      Serial.print(command[0]);
      Serial.print("\nstepper: ");
      Serial.print(command[1]);
      while (steps_left > 0) {
        currentMillis = micros();
        if (currentMillis - last_time >= 1000) {
          Direction = command[1];
          stepper(command[0]);
          time = time + micros() - last_time;
          last_time = micros();
          steps_left--;
        }
      }
    }

  }
  else
  {
    setblink(255, 0, 0);
  }
}
