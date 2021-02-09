#define MOTORANZAHL 6 // Gesamtzahl der Servos
#include "Servo.h"
#include <Wire.h>
#define SLAVE_ADDRESS 0x8

Servo Motor[MOTORANZAHL]; // erstelle ein Objekt für
// jeden Motor

byte Motorpin[MOTORANZAHL] = {3, 4, 5, 10, 11, 12};
byte Motorposition[MOTORANZAHL];
byte aktuellerMotor = 0, Position = 0, EingabeWinkel = 0;


void setup() {
  Serial.begin(115200);

  // initialize i2c as slave
  Serial.println("Slave-Address: ");
  Serial.print(SLAVE_ADDRESS);
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



// callback for received data
void receiveData(int byteCount)
{
  while (Wire.available())
  {
    byte Eingabe = Wire.read();
    Serial.println(c);

    if (aktuellerMotor == 10) // noch kein Motor gewählt
    {
      if (Eingabe >= '0' && Eingabe < MOTORANZAHL + '0')
        //(1)
      { // Ist die Eingabe eine gültige
        // Motor-Nr?
        aktuellerMotor = Eingabe - '0';
        continue; // (2)
      }
      if (Eingabe == 'i') // Statusinfo ausgeben
      {
        Serial.println("### aktuelle Positionswerte ###");
        for (byte i = 0; i < MOTORANZAHL; i++)
          Serial.println("Motor " + String(i) + ": " +
                         String(Motor[i].read()));
        continue;
      }
    }

    if (aktuellerMotor < 10) // Motor wurde bereits
      // angewählt
    {
      if (Eingabe >= '0' && Eingabe <= '9') // Eingabe ist
        // eine Ziffer
      {
        EingabeWinkel = EingabeWinkel * 10 + (Eingabe - '0');
        continue;
      }

      if (Eingabe == '+') // Erhöhung des Winkels
      {
        if (EingabeWinkel == 0)
          EingabeWinkel = 1;
        Position = Motor[aktuellerMotor].read(); // aktuellen
        // Winkel
        // auslesen
        if (180 - Position >= EingabeWinkel)
          Position += EingabeWinkel;
        else
          Position = 180;
        Motor[aktuellerMotor].write(Position);
        Serial.println("Motor " + String(aktuellerMotor)
                       + " wurde auf Position " +
                       String(Position)
                       + " gestellt.");
        EingabeWinkel = 0; aktuellerMotor = 10;
        continue;
      }
      if (Eingabe == '-') // Verringerung des
        // Winkels
      {
        if (EingabeWinkel == 0)
          EingabeWinkel = 1;
        Position = Motor[aktuellerMotor].read();
        if (Position >= EingabeWinkel)
          Position -= EingabeWinkel;
        else
          Position = 0;
        Motor[aktuellerMotor].write(Position);
        Serial.println("Motor " + String(aktuellerMotor)
                       + " wurde auf Position " +
                       String(Position)
                       + " gestellt.");
        EingabeWinkel = 0; aktuellerMotor = 10;
        continue;
      }

      if (EingabeWinkel <= 180) // absoluter Eingabewinkel
      {
        Motor[aktuellerMotor].write(EingabeWinkel);
        Serial.println("Motor " + String(aktuellerMotor)
                       + " wurde auf Position " +
                       String(EingabeWinkel)
                       + " gestellt.");
        EingabeWinkel = 0; aktuellerMotor = 10;
        continue;
      }

      Serial.println("Ungueltige Eingabe!");
      EingabeWinkel = 0; aktuellerMotor = 10;
    }
  }

  void loop()
  {


  }
