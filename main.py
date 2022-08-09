import sys
import numpy
import mysql.connector
import numpy as numpy
from PyQt5.QtWidgets import QMessageBox
# pip install pyqt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from Form_DoiMK import Ui_MainWindow
import numpy as np
import cv2
import sqlite3
import os
conn = mysql.connector.connect(user='root', password='170421',
                                     host='127.0.0.1', database='nguoidung')


class MainWindow1():
    # def __init__(self):
    #     self.main_win = QMainWindow()
    #     self.uic = Ui_MainWindow()
    #     self.uic.setupUi(self.main_win)
    #     # self.uic.setupUi(self.main_win)
    #     # khai bao nut an
    #     self.uic.btDoiMK.clicked.connect(self.getProfile)
    #     self.uic.btDoiMK_2.clicked.connect(self.faceid)
    #     self.uic.btDoiMK_3.clicked.connect(self.traning)

    # def show(self):
    #
    #     self.main_win.show()
    def traning(self):
        import cv2
        import numpy as np
        import os
        from PIL import Image
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        path = 'C:\\Users\\quanl\\Desktop\\dkmdata\\quanle'

        def getImageWithId(path):
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faces = []
            IDs = []
            for imagePath in imagePaths:
                faceImg = Image.open(imagePath).convert('L')
                faceNp = np.array(faceImg, 'uint8')
                print(faceNp)
                Id = int(imagePath.split('\\')[6].split('.')[1])
                faces.append(faceNp)
                IDs.append(Id)
                cv2.imshow('traninganh', faceNp)
                cv2.waitKey(10)
            return faces, IDs

        faces, Ids = getImageWithId(path)
        recognizer.train(faces, np.array(Ids))
        if not os.path.exists('recoginzer'):
            os.makedirs('recoginzer')
        recognizer.save('C:\\Users\\quanl\\Desktop\\dkmdata\\quanle.yml')
        cv2.destroyAllWindows()

    def faceid(self):


        def insertOrUpdate(id, ten):

            conn = sqlite3.connect('C:\\Users\\quanl\\Desktop\\trolyaocanhbaongugat\\AI-ndkmdt.db')
            query = "select * from nguoidung where id=" + str(id)
            cusror = conn.execute(query)

            isRecordExist = 0
            for row in cusror:
                isRecordExist = 1
            if (isRecordExist == 0):
                query = "INSERT INTO nguoidung(id, ten) VALUES (" + str(id) + ",'" + str(ten) + "')"
            else:
                query = "UPDATE nguoidung SET ten='" + str(ten) + "'WHERE id+" + str(id)
            conn.execute(query)
            conn.commit()
            conn.close()

        # loadndkm

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        cap = cv2.VideoCapture(0)
        tenTK = self.uic.lineTenTK.text()
        mkc = self.uic.lineMKCu.text()
        id = mkc
        ten = tenTK
        insertOrUpdate(id, ten)
        sampleNum = 0
        while (True):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
            for (x, y, w, h) in faces:

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if not os.path.exists('quanle'):
                    os.makedirs('quanle')
                sampleNum += 1
                cv2.imwrite(
                    'C:\\Users\\quanl\\Desktop\\dkmdata\\quanle\\anh.' + str(id) + '.' + str(sampleNum) + '.jpg',
                    gray[x: y + h, x:x + w])
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            if sampleNum > 50:
                break;
        cap.release()
        cv2.destroyAllWindows()

    def getProfile(id):
        conn = mysql.connector.connect(user='root', password='170421',
                                     host='127.0.0.1', database='nguoidung')
        cur = conn.cursor()
        tenTK = id.uic.lineTenTK.text()
        mkc = id.uic.lineMKCu.text()
        mkm = id.uic.lineMKMoi.text()
        nmkm= id.uic.lineNhapLaiMKMoi.text()
        print(tenTK,mkc,mkm,nmkm)

        try:
            code_8 = 'SELECT * FROM new_table'
            mycursor = conn.cursor()
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
                location_user = s_users.index(tenTK)
                print("locaiton user", location_user)
                correct_password = s_passwords[location_user]
                print("correct password", correct_password)
                if mkc != correct_password:
                    print("mkc ko dung")
                    msg = QMessageBox()
                    msg.setWindowTitle("Cảnh báo")
                    msg.setText("Mật khẩu cũ không đúng !")
                    msg.setIcon(QMessageBox.Warning)

                    x = msg.exec_()

                if mkc == correct_password:
                    print("dang nhap thanh cong")
                    if mkm != nmkm:
                        msg = QMessageBox()
                        msg.setWindowTitle("Cảnh báo")
                        msg.setText("Mật khẩu nhập lại không trùng !")
                        msg.setIcon(QMessageBox.Warning)

                        x = msg.exec_()
                    if mkm == nmkm:
                        cur.execute("UPDATE `nguoidung`.`new_table` SET `password` = %s WHERE (`user` = %s);", (mkm, tenTK))
                        conn.commit()
                        msg = QMessageBox()
                        msg.setWindowTitle("Cảnh báo")
                        msg.setText("Đổi mật khẩu thành công !")
                        msg.setIcon(QMessageBox.Warning)

                        x = msg.exec_()


                elif mkc != correct_password:
                    print("sai passsword")
            except:
                print("sai user")

        except:
            conn.rollback()
            conn.close()
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_win = MainWindow1()
#     main_win.show()
#     sys.exit(app.exec())
