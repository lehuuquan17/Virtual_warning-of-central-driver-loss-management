import sys

import numpy as np
import  cv2
import  os
from  PIL import Image
import  sqlite3
#nhandienkmtrongfile
face_cascade =cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('C:\\Users\\quanl\\Desktop\\dkmdata\\quanle.yml')

#ketnoisqltruyvanlinq

def getProfile(id):
    conn = sqlite3.connect('C:\\Users\\quanl\\Desktop\\trolyaocanhbaongugat\\AI-ndkmdt.db')
    query = "select * from nguoidung where id=" + str(id)
    cusror = conn.execute(query)
    profile = None
    for row in cusror:
        profile = row
    conn.close()
    return profile
cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX

while(True):

   # frame = cv2.imread('C:\\Users\\quanl\\Desktop\\dkmdata\\dataset12\\anh')
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (551, 255, 2), 4)
        roi_gray = gray[y:y+h , x: x+ w]
        id,confidence = recognizer.predict(roi_gray)
        if confidence <40:
            profile = getProfile(id)
            if(profile != None):
                cv2.putText(frame,""+str(profile[1]),(x+10,y+h+30),fontface,1,(0, 255, 0), 2)


        else:
            cv2.putText(frame,"SAINHE",(x+10,y+h+30), fontface,1,(0, 255, 0), 2)

    cv2.imshow('ndkm1',frame)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break;
cap.release()
cv2.destroyAllWindows()



