#!/bin/bash

cd /home/pi/Alfred & git pull
sleep 3
sudo chmod +x /home/pi/Alfred
sudo chmod +x /home/pi/Alfred/Alf_Start.sh
sudo chmod +x /home/pi/Alfred/Alf_Stop.sh
sudo chmod +x /home/pi/Alfred/Alf_Main.py

echo Alfred ist up-to-date
