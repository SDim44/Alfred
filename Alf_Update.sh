#!/bin/bash

# Update herunterladen
lxterminal --title="Alfred Update" --working-directory="/home/pi/Alfred" --command bash -c "git pull; bash" &

# Berechtigungen setzten
sudo chmod +x /home/pi/Alfred
sudo chmod +x /home/pi/Alfred/Alf_Start.sh
sudo chmod +x /home/pi/Alfred/Alf_Stop.sh
sudo chmod +x /home/pi/Alfred/Alf_Main.py

echo Alfred ist up-to-date
