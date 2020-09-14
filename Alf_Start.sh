#!/bin/bash

# Ladescreen setzten
echo "99.gif" > emotion.conf
# Modus setzten
echo "0" > mode.conf
sleep 1

#Programme starten
lxterminal --title="Alfred GUI" --working-directory="/home/pi/Alfred" --command bash -c "python2.7 Alf_GUI.py; bash" &
lxterminal --title="Alfred Speech" --working-directory="/home/pi/Alfred" --command bash -c "sudo python2.7 Alf_Speech.py; bash" &
lxterminal --title="Alfred Main" --working-directory="/home/pi/Alfred" --command bash -c "sudo python2.7 Alf_Main.py; bash"