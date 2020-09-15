# Alfred
Raspberry houshold robot Prototype 

FH Wiener Neustadt Robotik Project


# Dokumentation

## Alfred von Github herunterladen

Die Daten werden zuerst von Github heruntergeladen.
Da ein Automatisches Setup noch nicht erstellt wurde, müssen danach noch einige Anpassungen auf dem Raspberry Pi gemacht werden.


Terminal auf dem Raspberry Pi öffnen:
```
cd /home/pi/
git clone https://github.com/SDim44/Alfred.git
```
Alfred Updaten:
```
cd /home/pi/Alfred
git pull
```

## Automatisches Setup durchführen

Das Automatische Setup übernimmt alle Schritte unter den folgenden Punkten:
* Benötigte Software
* Raspberry Konfiguration
```
cd /home/pi/Alfred/setup
sudo chmod +x setup.sh
./setup.sh
```
(Während der Installation sind Benutzereingaben erforderlich.)



## Benötigte Software
### Serial Port ansteuern (Python Library):
```
sudo pip install pyserial
```
### Wiringpi – GPIO ansteueren (Python Library):
(auf Raspbian vorinstalliert)

### BME280 Temperatur Sensor (Python Library):
https://canox.net/2017/09/raspberry-pi-der-bme280-sensor/
```
sudo nano /etc/modules
Am Ende der Datei hinzufügen:
i2c-bcm2708
```
```
sudo nano /boot/config.txt
Am Ende der Datei hinzufügen:
dtparam=i2c1=on
dtparam=i2c_arm=on
```

### Pixy Cam 2
https://docs.pixycam.com/wiki/doku.php?id=wiki:v2:building_the_libpixyusb_example_on_linux

libusb installieren:
```
sudo apt-get install git libusb-1.0-0-dev g++ build-essential
```
Pixy2 herunterladen:
```
cd /home/pi && git clone https://github.com/charmedlabs/pixy2
cd pixy2/scripts && ./build_libpixyusb2.sh
./build_get_blocks_cpp_demo.sh
```
Pixy2 testen:
```
cd ../build/get_blocks_cpp_demo/
sudo ./get_blocks_cpp_demo
```
### Jarvis (Sprachsteuerung)
https://github.com/alexylem/jarvis

Jarvis herunterladen und starten:
```
cd /home/pi
git clone https://github.com/alexylem/jarvis.git
cd jarvis
./jarvis.sh
Jarvis
```
Anleitung zur Konfiguration unter:
https://github.com/alexylem/jarvis

Konfigurationshinweise:
Als Spracherkennung wird snowboy verwendet (offline-Erkennung)
Für alle Kommandos und das Schlüsselwort müssen vorab Aufnahmen in Jarvis erstellt werden.
Schlüsselwort: Alfred
Kommandos:
„Foge mir“ Mode 1
„Ladestation“ Mode 2
„stop“ Mode 3


## Optionale Software
### Matchbox-keyboard (Touchscreen/Onscreen Tastatur)
```
sudo apt-get install matchbox-keyboard
```
### Samba Server (Dateifreigabe)
Der Samba Server wurde verwendet um mit dem Windows Explorer auf die Dateien am Raspberry zu zuzugreifen.

Installation:
```
sudo apt-get install samba samba-common smbclient
```
Default config sichern:
```
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf_alt
```
Neue config-Datei erstellen und öffnen: 
```
sudo nano /etc/samba/smb.conf
```
In Datei schreiben:
```
[global]
workgroup = WORKGROUP
security = user
encrypt passwords = yes
client min protocol = SMB2
client max protocol = SMB3
 
[root]
comment = root
path = /
read only = no
```
Samba Dienst neustarten:
```
sudo service smbd stop
sudo service smbd start
```
Samba Benutzer einrichten:
```
sudo smbpasswd -a pi
```
danach noch 2mal dein Passwort für den User „pi“ eingeben.

Jetzt kann der Pfad in der Ordner-Navigationsleiste am Windows Gerät eingegeben werden:
\\Alfred

## Software für Alfred Webinterface 
(in der aktuellen Version noch nicht verfügbar)

### Apache2 (Webserver)
```
sudo apt-get install apache2
```
### PHP
```
sudo apt install php
```
### Website bereitstellen
```
cp /home/pi/Alfred/html /var/www/html
```
Jetzt kann über einen beliebigen Brower aus das Webinterface zugegriffen werden:
http://alfred

## Raspberry Konfiguration
### Bildschirm um 180° drehen:
Für viele Gehäuse des Raspberry Pi 7 Zoll Touchscreen ist es notwendig die anzeige zu drehen damit sie nicht auf dem Kopf steht.

Datei öffnen: 
```
sudo nano /boot/config.txt
```
Am Ende des Dokuments eine Zeile einfügen: 
```
lcd_rotate=2
```
### Bootscreen ändern:
https://scribles.net/customizing-boot-up-screen-on-raspberry-pi/

Um das Bild, dass beim boot-vorgang angezeigt wird zu ändern, wird das Original Raspbian Bild mit dem Bild aus dem Alfred Ordner ersetzt.
```
sudo cp /home/pi/Alfred/DATA/design/splash.png /usr/share/plymouth/themes/pix/splash.png
```
### Default Audio Device ändern:
Mit diesem Vorgang wird standardmäßig die externe Soundkarte verwendet.

Datei erstellen:
```
sudo nano /etc/asound.conf
```
In Datei schreiben:
```
pcm.!default 
{
    type hw
    card 1
}

ctl.!default 
{
    type hw           
    card 1
}
```


### Init-Script erstellen
http://raspberry.tips/raspberrypi-einsteiger/raspberry-pi-autostart-von-skripten-und-programmen-einrichten

Vorteil eines Init-Scripts ist das ein Programm nicht nur beim booten des RasPi gestartet wird sondern beim runterfahren oder neustarten auch entsprechend behandelt wird.
Dazu eine Datei erstellt werden und der entsprechende Code in die Datei geschrieben werden.
```
sudo nano /etc/init.d/Alfred
```
In die Datei kopieren:
```
#! /bin/sh
### BEGIN INIT INFO
# Provides:          Alfred
# Required-Start:
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts & Stops Alfred
### END INIT INFO
#Switch case fuer den ersten Parameter
case "$1" in
    start)
 #Aktion wenn start uebergeben wird
        echo "Starte Alfred"
        cd /home/pi/Alfred
        ./Alf_Start.sh
     
    stop)
 #Aktion wenn stop uebergeben wird
        echo "Stoppe Alfred"
        cd /home/pi/Alfred
        ./Alf_Stop.sh
 
    restart)
 #Aktion wenn restart uebergeben wird
        echo "Restarte Alfred"
        cd /home/pi/Alfred
        ./Alf_Stop.sh
        sleep 2
        ./Alf_Start.sh
 
    update)
#Aktion wenn update uebergeben wird
        echo "Update Alfred"
        cd /home/pi/Alfred
        ./Alf_Update.sh
 *)
 #Standard Aktion wenn start|stop|restart nicht passen
 echo "(start|stop|restart)"
 
esac
exit 0
```


Jetzt kann Alfred mit folgendem Befehl gestartet, gestoppt und geupdatet werden.
```
Sudo /etc/init.d/Alfred start
Sudo /etc/init.d/Alfred stop 
Sudo /etc/init.d/Alfred update  
```

### Desktop und Startmenü Verknüpfung
https://www.raspberrypi.org/forums/viewtopic.php?t=9817

Um alle Verknüpfungen zu erstellen, werden 3 Dateien angelegt und der entsprechenden Code geschrieben.
#### Alfred starten
Datei am Desktop erstellen:
```
sudo nano /home/pi/Desktop/Alfred_start.desktop
```
Ins Dokument schreiben:
```
[Desktop Entry]
Type=Application
Comment=Start Alfred
Name=Alfred
Exec=sudo /etc/init.d/Alfred start
Icon=/home/pi/Alfred/DATA/design/Alf_Logo_randlos_s_auf_t.png
Terminal=false
Categories=Utility
StartupNotify=true
```
Verknüpfung in das Startmenü kopieren:
```
sudo cp /home/pi/Desktop/Alfred_start.desktop /usr/share/raspi-ui-overrides/applications/Alfred_start.desktop
```

#### Alfred beenden
Datei am Desktop erstellen:
```
sudo nano /home/pi/Desktop/Alfred_stop.desktop
```
Ins Dokument schreiben:
```
[Desktop Entry]
Type=Application
Comment=Stop Alfred
Name=Alfred
Exec=sudo /etc/init.d/Alfred stop
Icon=/home/pi/Alfred/DATA/design/stop.png
Terminal=false
Categories=Utility
StartupNotify=true
```
Verknüpfung in das Startmenü kopieren:
```
sudo cp /home/pi/Desktop/Alfred_stop.desktop /usr/share/raspi-ui-overrides/applications/Alfred_stop.desktop 
```
#### Alfred updaten
Datei am Desktop erstellen:
```
sudo nano /home/pi/Desktop/Alfred_update.desktop
```

Ins Dokument schreiben:
```
[Desktop Entry]
Type=Application
Comment=Update Alfred
Name=Alfred
Exec=sudo /etc/init.d/Alfred update
Icon=/home/pi/Alfred/DATA/design/update.png
Terminal=false
Categories=Utility
StartupNotify=true
```
Verknüpfung in das Startmenü kopieren:
```
sudo cp /home/pi/Desktop/Alfred_update.desktop /usr/share/raspi-ui-overrides/applications/Alfred_update.desktop
```

## Probleme

### Berechtigungen
sudo chmod +x /home/pi/Alfred/Alf_Update.sh
sudo chmod +x /home/pi/Alfred /Alf_Start.sh
sudo chmod +x /home/pi/Alfred /Alf_Stop.sh
sudo chmod +x /home/pi/Alfred /Alf_Main.py

### Python Tkinter GUI über SSH starten
export DISPLAY=:0.0
