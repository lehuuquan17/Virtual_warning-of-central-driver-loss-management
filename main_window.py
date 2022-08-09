
import glob

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QThread, Qt, pyqtSignal, pyqtSlot
from thigiacmat import *
import dlib
from pygame import mixer
from main import *
import cv2
import main
from gtts import gTTS
import playsound
from ui_main_window import *
import speech_recognition as sr
r = sr.Recognizer()
musicsig = False



class WorkThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.running = False

    def run(self):
        EYE_AR_THRESH = 0.2
        EYE_AR_CONSEC_FRAMES =20
        YAWN_THRESH = 20
        alarm_status = False
        alarm_status2 = False
        saying = False
        COUNTER = 0
        cap = cv2.VideoCapture(0)
        catch=0
        while self.running:
            ret, frame = cap.read()
            if ret:
                frame = imutils.resize(frame, width=450)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # rects = detector(gray, 0)
                rects = self.widget.detector.detectMultiScale(gray, scaleFactor=1.1,
                                                              minNeighbors=5, minSize=(30, 30),
                                                              flags=cv2.CASCADE_SCALE_IMAGE)

                # for rect in rects:
                for (x, y, w, h) in rects:
                    rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

                    shape = self.widget.predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    eye = final_ear(shape)
                    ear = eye[0]
                    leftEye = eye[1]
                    rightEye = eye[2]

                    distance = lip_distance(shape)

                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

                    lip = shape[48:60]
                    cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

                    if ear < EYE_AR_THRESH:
                        COUNTER += 1

                        if ear < EYE_AR_THRESH:
                            COUNTER += 1

                            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                                if alarm_status == False:
                                    alarm_status = True
                                    t = Thread(target=alarm, args=('khong ngu nua',))
                                    t.deamon = True
                                    t.start()

                                cv2.putText(frame, "CANH BAO NGUY HIEM", (10, 30),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            import winsound
                            a = 3500
                            for i in range(a,4100,100) :
                               # a += 100
                                frequency = i  # Set Frequency To 2500 Hertz
                                duration = 200  # Set Duration To 1000 ms == 1 second
                                winsound.Beep(frequency, duration)



                            # def playsong(path):
                            #     mixer.init()
                            #     mixer.music.load(path)
                            #     mixer.music.play()
                            #     print("bài hát " + path)
                            #     while mixer.music.get_busy():  # wait for music to finish playing
                            #         cv2.putText(frame, "CANH BAO NGUY HIEM", (10, 30),
                            #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            #         time.sleep(0.5)
                            #
                            # def getlistMusic(path):
                            #     music = []
                            #     for song in glob.glob(path):
                            #         i = 0
                            #         music.insert(i, song)
                            #     return music
                            #
                            # path = "D:\\music\\alarm\\*.wav"
                            # music = getlistMusic(path)
                            # i = 0
                            # playsong(music[i])
                    else:

                        COUNTER = 0
                        #alarm_status = False
                    cound = 0
                    if (distance > YAWN_THRESH):
                        cv2.putText(frame, "Ngap ngu roi", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        def speak(mind):
                            tts = gTTS(text=mind, lang='vi')
                            print("AI:", mind)
                            filename = 'voiceVI.mp3'
                            tts.save(filename)
                            playsound.playsound(filename)
                            os.remove(filename)
                        speak("bạn nên nghe nhạc đi")
                        if alarm_status2 == False and saying == False:
                            alarm_status2 = True
                            t = Thread(target=alarm, args=('hay tinh tao',))
                            t.deamon = True
                            t.start()


                    else:
                        alarm_status2 = False

                    cv2.putText(frame, "mat: {:.2f}".format(ear), (300, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "mieng: {:.2f}".format(distance), (300, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self.running = False
        self.wait()


class MainWindow(QWidget):
    # class constructor
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # create a timer
        self.timer = QTimer()
        # set timer timeout callback function
        self.timer.timeout.connect(self.viewCam)
        # set control_bt callback clicked  function
        self.ui.control_bt.clicked.connect(self.start_stream)
        self.ui.pushButton.clicked.connect(self.openui)



        self.detector = cv2.CascadeClassifier("C:\\Users\\quanl\\Desktop\\dkmdata\\haarcascade_frontalface_default.xml")  # Faster but less accurate
        self.predictor = dlib.shape_predictor('C:\\Users\\quanl\\Desktop\\dkmdata\\shape_predictor_68_face_landmarks.dat')

        self.thread = WorkThread(self)
        self._new_window = None
        self.Videocapture_ = None

    def openui(self):
        print("ok")
        self.sreen_setup = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.sreen_setup)
        self.sreen_setup.show()
        self.uic.btDoiMK.clicked.connect(self.getProfile)
        self.uic.btDoiMK_2.clicked.connect(self.faceid)
        self.uic.btDoiMK_3.clicked.connect(self.traning)

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
      try:
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
      except:
          msg = QMessageBox()
          msg.setWindowTitle("Cảnh báo")
          msg.setText("Vui lòng điền đầy đủ thông tin !")
          msg.setIcon(QMessageBox.Warning)
          print(msg)
    def getProfile(id):
        conn = mysql.connector.connect(user='root', password='170421',
                                       host='127.0.0.1', database='nguoidung')
        cur = conn.cursor()
        tenTK = id.uic.lineTenTK.text()
        mkc = id.uic.lineMKCu.text()
        mkm = id.uic.lineMKMoi.text()
        nmkm = id.uic.lineNhapLaiMKMoi.text()
        print(tenTK, mkc, mkm, nmkm)

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
                        cur.execute("UPDATE `nguoidung`.`new_table` SET `password` = %s WHERE (`user` = %s);",
                                    (mkm, tenTK))
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


    @pyqtSlot(QImage)
    def setImage(self, image):
        self.ui.image_label.setPixmap(QPixmap.fromImage(image))

    def start_stream(self):
        if not self.thread.running:
            self.thread.running = True
            self.ui.control_bt.setText("Stop")
            self.thread.changePixmap.connect(self.setImage)
            self.thread.start()
            self.show()
        else:
            self.stop_stream(self)

    def stop_stream(self, event):
        self.thread.stop()
        self.ui.control_bt.setText("Start")

    # view camera
    def viewCam(self):
        # read image in BGR format
        ret, image = self.cap.read()
        # convert image to RGB format
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # get image infos
        height, width, channel = image.shape
        step = channel * width
        # create QImage from image
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # show image in img_label

        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # start/stop timer
    def controlTimer(self):
        # if timer is stopped
        if not self.timer.isActive():
            # create video capture

            import thigiacmat
            # start timer
            self.timer.start(15)
            # update control_bt text

            self.ui.control_bt.setText("Stop")

        # if timer is started
        else:
            # stop timer
            self.timer.stop()
            # release video capture
            self.cap.release()
            # update control_bt text
            self.ui.control_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create and show mainWindow
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())