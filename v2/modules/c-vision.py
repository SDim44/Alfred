#
#       Alfred Computer-Vision
#
#       Stefan Dimnik, 14.08.2020
#
#       V0.1
#       Dieses Programm uebernimmt die Objekterkennung mit opencv.
#       Für dieses Programm wird eine Webcam benoetigt -> Pixy Cam kann nicht verwendet werden

#Libarys
import cv2
import numpy as np

#------------------------------------------------------------------------------------------------- 
#Bild in Variable schreiben
cap = cv2.VideoCapture(0)


#------------------------------------------------------------------------------------------------- 
#Auf dem Bild nach Gesicht suchen und Koordinaten zurueckgeben
def facedetect():
    face_cascade = cv2.CascadeClassifier('DATA/haarcascades/haarcascade_frontalface_default.xml')

    ret, frame = cap.read(0)
    face_img = frame.copy()
    face_rects = face_cascade.detectMultiScale(face_img)

    for (x,y,w,h) in face_rects:
        midx = (x+w) /2
        midy = (y+h) /2

    cap.release()
    #print midx,midy,x,y,w,h
    return midx,midy,x,y,w,h