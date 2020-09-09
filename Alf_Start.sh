#!/bin/bash

sudo chmod +x /home/pi/Alfred
sudo chmod +x /home/pi/Alfred/Alf_Start.sh
sudo chmod +x /home/pi/Alfred/Alf_Stop.sh
sudo chmod +x /home/pi/Alfred/Alf_Main.py
echo Berechtigungen wurden gesetzt

echo "99.gif" > emotion.conf
sleep 2
lxterminal --title="Alfred GUI" --working-directory="/home/pi/Alfred" --command bash -c "python2.7 Alf_GUI.py; bash" &
lxterminal --title="Alfred Speech" --working-directory="/home/pi/Alfred" --command bash -c "python2.7 Alf_Speech.py; bash" &
lxterminal --title="Alfred Main" --working-directory="/home/pi/Alfred" --command bash -c "sudo python2.7 Alf_Main.py; bash"