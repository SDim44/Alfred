#
#       Alfred Computer-Vision
#
#       Stefan Dimnik, 14.08.2020
#
#       V0.1
#       Dieses Programm uebernimmt die Objekterkennung mit opencv.


import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def facedetect()
    face_cascade = cv2.CascadeClassifier('DATA/haarcascades/haarcascade_frontalface_default.xml')

    ret, frame = cap.read(0)
    face_img = frame.copy()
    face_rects = face_cascade.detectMultiScale(face_img)

    for (x,y,w,h) in face_rects:
        midx = (x+w) /2
        midy = (y+h) /2

    cap.release()

    return midx,midy,x,y,w,h