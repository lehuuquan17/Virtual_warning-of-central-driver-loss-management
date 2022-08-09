import cv2
import numpy as np
import  os
from  PIL import Image
recognizer = cv2.face.LBPHFaceRecognizer_create()#thư viện huấn luyện
path ='C:\\Users\\quanl\\Desktop\\dkmdata\\quanle'
def getImageWithId(path):
    imagePaths =[os.path.join(path, f)for f in os.listdir(path)]#lấy ra các anh trong đường dẫn
    faces = []
    IDs= []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')#lấy tất cả anh đưa về kiểu L
        faceNp =np.array(faceImg,'uint8')# chuyển định dạng ma trận điểm ảnh
        print(faceNp)
        Id = int(imagePath.split('\\')[6].split('.')[1]) # lấy id của ảnh
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