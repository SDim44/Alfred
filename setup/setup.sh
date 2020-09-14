#!/bin/bash

echo ----------------------------------------------
echo ---------Alfred wird installiert--------------
echo ----------------------------------------------

echo -> install pyserial
sudo pip install pyserial


echo ----------------------------------------------
echo -> configure /etc/modules
grep -q -F 'i2c-bcm2708' /etc/modules ||  echo 'i2c-bcm2708' | sudo tee -a /etc/modules


echo ----------------------------------------------
echo -> configure /boot/config.txt

grep -q -F '# Alfred Settings:' /boot/config.txt ||  echo '#Alfred Settings:' | sudo tee -a /boot/config.txt
grep -q -F 'dtparam=i2c1=on' /boot/config.txt ||  echo 'dtparam=i2c1=on' | sudo tee -a /boot/config.txt
grep -q -F 'dtparam=i2c_arm=on' /boot/config.txt ||  echo 'dtparam=i2c_arm=on' | sudo tee -a /boot/config.txt
grep -q -F 'lcd_rotate=2' /boot/config.txt ||  echo 'lcd_rotate=2' | sudo tee -a /boot/config.txt


echo ----------------------------------------------
echo -> install jarvis
cd /home/pi & git clone https://github.com/alexylem/jarvis.git 
cd /home/pi/jarvis & ./jarvis.sh


echo ----------------------------------------------
echo -> install Matchbox Keyboard
sudo apt-get install matchbox-keyboard


echo ----------------------------------------------
echo -> Change Bootscreen
sudo cp /home/pi/Alfred/DATA/design/splash.png /usr/share/plymouth/themes/pix/splash.png


echo ----------------------------------------------
echo -> Create Init-Script
sudo cp /home/pi/Alfred/setup/Alfred /etc/init.d/Alfred


echo ----------------------------------------------
echo -> Create Shortcuts
sudo cp /home/pi/Alfred/setup/Alfred_start.desktop /home/pi/Desktop/Alfred_start.desktop
sudo cp /home/pi/Alfred/setup/Alfred_start.desktop /usr/share/raspi-ui-overrides/applications/Alfred_start.desktop

sudo cp /home/pi/Alfred/setup/Alfred_stop.desktop /home/pi/Desktop/Alfred_stop.desktop
sudo cp /home/pi/Alfred/setup/Alfred_stop.desktop /usr/share/raspi-ui-overrides/applications/Alfred_stop.desktop

sudo cp /home/pi/Alfred/setup/Alfred_update.desktop /home/pi/Desktop/Alfred_update.desktop
sudo cp /home/pi/Alfred/setup/Alfred_update.desktop /usr/share/raspi-ui-overrides/applications/Alfred_update.desktop


echo ----------------------------------------------
echo -> Set Permissions
sudo chmod +rwxr /etc/init.d/Alfred
sudo chmod +x /home/pi/Alfred/Alf_Update.sh
sudo chmod +x /home/pi/Alfred/Alf_Start.sh
sudo chmod +x /home/pi/Alfred/Alf_Stop.sh
sudo chmod +x /home/pi/Alfred/Alf_Main.py


echo ----------------------------------------------
echo ---------Installation Abgeschlossen-----------
echo ----------------------------------------------

