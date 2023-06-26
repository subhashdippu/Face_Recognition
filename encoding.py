import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage

# Importing student images
folderPath = 'faces' 
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))# Here in imgList the image is stored as cv2 form means in a metrix form and exect link of the image
    studentIds.append(os.path.splitext(path)[0])# Here we just spliting the image in two parts from .
    
    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds)


def findEncodings(imagesList): # Converting the image in cv2 form
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)# It will convert the every element of BGR TO RGB
        encode = face_recognition.face_encodings(img)[0]# Encode the image in cv2  
        encodeList.append(encode)

    return encodeList
  

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")