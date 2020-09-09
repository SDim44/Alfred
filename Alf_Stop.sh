#!/bin/bash
pkill -f Alf_GUI.py
pkill -f Alf_Speech.py
sudo pkill -f Alf_Main.py
echo "0.gif" > emotion.conf