#!/bin/bash

#Programme beenden
sudo pkill -f Alf_GUI.py
sudo pkill -f Alf_Speech.py
sudo pkill -f Alf_Main.py

#Emotion/Bild setzten
echo "0.gif" > emotion.conf