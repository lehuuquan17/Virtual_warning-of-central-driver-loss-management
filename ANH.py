# import cv2
# import numpy as np
# img = cv2.imread('lena.png') # đưa ảnh vào thư mục python rồi viết dòng này
# print(type(img))# nhớ có dòng này img ở đây phải dống cái biến ảo ở trên mà mình đã đặt , nó alf biến ảo
# print(img.shape)# ghi vô nó mới chạy đc
# #img =  cv2.imwrite('lena.png',img)
# # # img1 = cv2.resize(img,(100,100)) #này ảnh size cho bức ảnh 1
# # # print(img1.shape) #in nó ra thôi
# img2 = cv2.resize(img,(0,0),fx=0.5 , fy=0.5 )#này ảnh size cho bức ảnh 2 , sử dụng trục tung , trục hoành
# # # print(img2.shape)#in nó ra thôi
# #
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #đổi màu sang trắng đen
# ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) # thay đổi kích thước
# print(thresh1.shape)# in nó ra , hình như laf truyền kích thươc
# print(gray.shape)# in nó ra , hình như là truyền ra ảnh đã đổi màu
# face_cascade =cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
# # #cv2.imwrite('thresh1.png',thresh1) # đổi màu sang trắng đen
# # # blur =cv2.blur(img,(5,5)) # này là làm mờ thôi , 5 nhân 5 tỷ lẹ gì đó
# # # cv2.imwrite('blur1.jpg',blur) # cho nó đọc file , nó sẽ tự tạo ra 1 file trong pychram
# # # blur2 =cv2.blur(img,(13,13))# này là làm mờ thôi , 13 nhân 13 tỷ lẹ gì đó
# # # cv2.imwrite('blur2.jpg',blur2) # cho nó đọc file , nó sẽ tự tạo ra 1 file trong pychram
# # # crop =img2[:150,150:]
# # # print(crop.shape)
# # # cv2.imwrite('crop.jpg',crop)
# # #
# # # cv2.imshow('idol iu',crop )
# # # #cv2.imshow('idol iu2',blur2 )# show nó lên , ở cụm'idol iu ' thì các bạn để như thế nào cũng đc
# # # cv2.waitKey(0) # cho nó dừng , sau khi show lên
# # # cap =cv2.VideoCapture(0)
# # # if(cap.isOpened()==False):
# # #     print("loi mo cam")
# # # while(cap.isOpened()):
# # #     ret , frame = cap.read()
# # #     if ret == True:
# # #         cv2.imshow('quanle',frame)
# # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # #             break
# # # cap.release()
# # # cv2.destroyAllWindows()
# # # import  cv2
# # # lena =cv2.imread('a.jpg')
# # # gray = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
# # # face_cascade = cv2.CascadeClassifier('train.xml')
# # # faces = face_cascade.detectMultiScale(gray)
# # # print(faces)
# # # for(x, y , w, h) in faces:
# # #     cv2.rectangle(lena, (x,y),(x+w, y+h),(255,0,0),3)
# #tìm dudiuongwf dọc
#
# cv2.imwrite('lena.png',img2)
# cv2.imshow('lena',img2)
# cv2.waitKey()
import numpy as np
import cv2
face_cascade =cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_eye.xml")

img = cv2.imread('lena.jpg')

img2=cv2.resize(img,(0,0),fx=2,fy=2)
gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
	    img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img2[y:y+h, x:x+w]
eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
for (ex,ey,ew,eh) in eyes:
	     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
cv2.imshow('ABC',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

