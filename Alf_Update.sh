#!/bin/bash
lxterminal --title="Alfred Update" --working-directory="/home/pi/Alfred" --command bash -c "cd /home/pi/Alfred & git pull & echo "Alfred ist up-to-date"; bash"
sudo chmod +x /home/pi/Alfred
sudo chmod +x /home/pi/Alfred/Alf_Start.sh
sudo chmod +x /home/pi/Alfred/Alf_Stop.sh
sudo chmod +x /home/pi/Alfred/Alf_Main.py



