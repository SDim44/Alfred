#
#       Alfred Computer-Vision
#
#       Stefan Dimnik, 14.08.2020
#
#       V0.1
#       Dieses Programm uebernimmt die Objekterkennung mit opencv.


import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('DATA/haarcascades/haarcascade_frontalface_default.xml')


def detect_face(img):
    
    face_img = img.copy()
    
    face_rects = face_cascade.detectMultiScale(face_img)
    
    for (x,y,w,h) in face_rects:
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 5)
        print("x={0}, y={1}, w={2}, h={3}".format(x,y,w,h))
    
    return face_img



cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read(0)

    frame = detect_face(frame)
    
    cv2.imshow('Video Bild Identification', frame)
    
    c = cv2.waitKey(1) #Esc
    
    if c == 27:
        break
        
cap.release()
cv2.destroyAllWindows()