import numpy as np
import  cv2
import  sqlite3
import os
def insertOrUpdate(id, ten):
    conn =sqlite3.connect('C:\\Users\\quanl\\Desktop\\trolyaocanhbaongugat\\AI-ndkmdt.db')
    query = "select * from nguoidung where id="+str(id)
    cusror = conn.execute(query) #lấy bản ghi

    isRecordExist =0 #kiểm tra id trong data
    for row in cusror: #duyệt từng hàng
        isRecordExist = 1 # tồn tại
    if(isRecordExist == 0):#chưa có bản ghi
        query ="INSERT INTO nguoidung(id, ten) VALUES ("+str(id)+",'"+str(ten)+"')"
    else:
        query ="UPDATE nguoidung SET ten='"+str(ten)+"'WHERE id+"+str(id)
    conn.execute(query)
    conn.commit()
    conn.close()
#loadndkm

face_cascade =cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
#nhapdl3
id = input("nhap id")
ten = input("nhap ten")
insertOrUpdate(id, ten)
sampleNum =0
while(True):
    ret,frame = cap.read() #lấy ảnh từ camera
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5,minNeighbors=5)
    for(x,y,w,h) in faces:

        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        if not os.path.exists('quanle'):
           os.makedirs('quanle')
        sampleNum +=1
        cv2.imwrite('C:\\Users\\quanl\\Desktop\\dkmdata\\quanle\\anh.'+str(id)+'.'+str(sampleNum)+'.jpg', gray[x: y+h, x:x+w])
    cv2.imshow('frame',frame)
    cv2.waitKey(1)
    if sampleNum > 50:
        break;
cap.release()
cv2.destroyAllWindows()



