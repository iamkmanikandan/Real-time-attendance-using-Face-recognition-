import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("Resources/DB/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-77a58-default-rtdb.firebaseio.com/",
    # 'storageBucket': ""
})

bucket = storage.bucket('attendance-system-77a58.appspot.com')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
# print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
# encodeListKnownWithIds = pickle.load(file)
encodeListKnownWithIds = np.load(file, allow_pickle=True)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds


# print(studentIds)
# print("Encode File Loaded")


def update_total_absent(id, stdInfo):
    """Updates the total absent of a student."""

    # Get the current time
    now = datetime.now()

    # Get the last attendance time
    last_attendance_time = datetime.strptime(stdInfo['last_attendance_time'], '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference
    seconds_elapsed = (now - last_attendance_time).total_seconds()
    ref = db.reference(f'Students/{id}')

    # If the student's face was not detected in the timeframe of seconds_elapsed
    if seconds_elapsed > 30:
        # Increment the total absent
        stdInfo['total_absent'] += 1
        ref.child('total_absent').set(stdInfo['total_absent'])
        stdInfo['total_class'] = stdInfo['total_present'] + stdInfo['total_absent']
        ref.child('total_class').set(stdInfo['total_class'])
        ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


modeType = 0
counter = 0
id = -1
imgStudent = []
imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

while True:
    success, img = cap.read()

    imgBackground[162:162 + 480, 55:55 + 640] = img

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.face_distance(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face Attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Resized/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                   "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_present'] += 1
                    ref.child('total_present').set(studentInfo['total_present'])
                    studentInfo['total_class'] = studentInfo['total_present'] + studentInfo['total_absent']
                    ref.child('total_class').set(studentInfo['total_class'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                # for id in studentIds:
                #     # print(id)
                #     studentInfo = db.reference(f'Students/{id}').get()
                #     update_total_absent(id, studentInfo)

                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_class']), (945, 82),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    cv2.putText(imgBackground, str(studentInfo['department']), (1026, 405),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['semester']), (1000, 480),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['registration number']), (997, 570),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['total_present']), (930, 645),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['total_absent']), (1046, 645),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1150, 645),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 2)
                    offset = (410 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (815 + offset, 330),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

                    # display std image into the frame
                    imgBackground[125:125 + 159, 935:935 + 157] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        for id in studentIds:
            # print(id)
            studentInfo = db.reference(f'Students/{id}').get()
            update_total_absent(id, studentInfo)


    else:
        modeType = 0
        counter = 0
        for id in studentIds:
            # print(id)
            studentInfo = db.reference(f'Students/{id}').get()
            update_total_absent(id, studentInfo)
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKeyEx(1)
