import sys
from PyQt5.QtWidgets import QMessageBox
# pip install pyqt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow ,QMessageBox
import numpy as np
import  cv2
import  os
from  PIL import Image
import  sqlite3
import main_window
from loginUi4 import Ui_Form
from main_window import MainWindow
import mysql.connector
import numpy
from PyQt5.QtWidgets import QApplication, QDialog
from  PyQt5.QtWidgets import  QMainWindow
db = mysql.connector.connect(user='root', password='170421',
                             host='127.0.0.1', database='nguoidung')

class MainWindow1:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_Form()
        self.uic.setupUi(self.main_win)
        # self.uic.setupUi(self.main_win)
        # khai bao nut an
        self.uic.pushButton.clicked.connect(self.showinfo)

    def show(self):

        self.main_win.show()


    def showinfo(self):
        #training hình ảnh nhan diên với thư viện nhận diện khuôn mặt
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")#nhận diện khôn mặt ở trong camera
        recognizer = cv2.face.LBPHFaceRecognizer_create()#thao tác trên khuôn măt

        recognizer.read('C:\\Users\\quanl\\Desktop\\dkmdata\\quanle.yml')
        # ketnoisqltruyvanlinq
        sampleNum = 0

        def getProfile(id):
            conn = sqlite3.connect('C:\\Users\\quanl\\Desktop\\trolyaocanhbaongugat\\AI-ndkmdt.db')
            query = "select * from nguoidung where id=" + str(id) #truyền id về chuỗi
            cusror = conn.execute(query)
            profile = None #lưu giá trị lấy đc từ database
            for row in cusror:
                profile = row
            conn.close()
            return profile

        cap = cv2.VideoCapture(0)
        fontface = cv2.FONT_HERSHEY_SIMPLEX
        check = True
        while check:

            # frame = cv2.imread('C:\\Users\\quanl\\Desktop\\dkmdata\\dataset12\\anh')
            ret, frame = cap.read() # đọc dl từ camera
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4) #kết hợp wedcam và face_cascade để có dl nhận diện trên wedcam
            for (x, y, w, h) in faces: #vẽ hình vuông
                cv2.rectangle(frame, (x, y), (x + w, y + h), (552, 255, 0), 5) # truyền vào tham số để vừa vặn với mặt
                roi_gray = gray[y:y + h, x: x + w]  # cắt fame trong cam so sánh vs tập dl đã train , tọa độ tịnh tiến
                id, confidence = recognizer.predict(roi_gray) # nhận diện km có trong tập dl , nó trẽ trả về id mà mình train
                if confidence < 40:
                    profile = getProfile(id)
                    if (profile != None):
                        cv2.putText(frame, "" + str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
                        self.uic.main_win = main_window.MainWindow()
                        self.uic.setupUi(self.main_win)
                        self.uic.main_win.show()
                        check= False
                                                #sys.exit()



                else:
                    cv2.putText(frame, "SAINHE", (x + 10, y + h + 30), fontface, 1, (0, 255, 0), 2)
            sampleNum += 1
            cv2.imshow('ndkm1', frame)
            cv2.waitKey(50)
            if sampleNum > 50:
                break;
        user = self.uic.lineEdit.text()
        password = self.uic.lineEdit_2.text()
        # lenh chay
        code_8 = 'SELECT * FROM new_table'
        # lệnh chạy code
        mycursor = db.cursor()
        mycursor.execute(code_8)  # make database
        result = mycursor.fetchall()
        b = numpy.array(result)
        print(b)
        s_users = []
        s_passwords = []

        for i in b:
            s_users.append(i[1])
            s_passwords.append(i[2])

        print(s_users)
        print(s_passwords)

        try:
            location_user = s_users.index(user)
            print("locaiton user", location_user)
            correct_password = s_passwords[location_user]
            print("correct password", correct_password)
            if password == correct_password:
                print("dang nhap thanh cong")
                self.uic.main_win = main_window.MainWindow()
                self.uic.setupUi(self.main_win)
                self.uic.main_win.show()


            elif password != correct_password:
                print("sai passsword")
                msg = QMessageBox()
                msg.setWindowTitle("Cành báo")
                msg.setText("Sai passwword")
                msg.setIcon(QMessageBox.Warning)

                x = msg.exec_()


        except:

            print("sai user")
            msg = QMessageBox()
            msg.setWindowTitle("Cảnh báo")
            msg.setText("Tên đăng nhập hoặc Face id không hoạt động !")
            msg.setIcon(QMessageBox.Warning)

            x = msg.exec_()



if __name__=="__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow1()
    main_win.show()
    sys.exit(app.exec())
