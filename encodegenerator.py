import os
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage

cred = credentials.Certificate("resource/DB/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-77a58-default-rtdb.firebaseio.com/",
    'dataBucket': "attendance-system-77a58.appspot.com"
})

#importing  a images in to a list
folderPath = 'Resized'
imgPathList = os.listdir(folderPath)
print(imgPathList)
imgList = []
stdIds = []
for path in imgPathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    #print(os.path.splitext(path)[0])
    #print(path)
    stdIds.append(os.path.splitext(path)[0])

    #storing image to DB
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket('attendance-system-77a58.appspot.com')
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

print(stdIds)

# def findEncodings(imgList, cache):
#     encodeList = []
#     for img in imgList:
#         img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)
#         if len(encode) > 0:
#             # Only store the encoding if a face was found in the image
#             encode = encode[0]
#             encodeList.append(encode)
#             cache[hash(encode.tobytes())] = stdIds[len(encodeList) - 1]
#     return encodeList


def findEncodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

#encode start
print("Encoding started")
encodeListKnown = findEncodings(imgList)
encodeListKnownwithIds = [encodeListKnown,stdIds]
print(encodeListKnown)
print("Encode finished...")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownwithIds, file)
file.close()
print("Encode file saved")