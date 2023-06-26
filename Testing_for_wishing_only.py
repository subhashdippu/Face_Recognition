''' Make Updation 
Here i just make a dictionary line 94
'''

import face_recognition
import os, sys
import cv2
import math, pickle
import os
import pickle
import cv2
import face_recognition
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
# from firebase_admin import storage
import numpy as np
import asyncio
from datetime import datetime
import voice

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-2ea7e-default-rtdb.firebaseio.com/",
    # 'storageBucket': "faceattendacerealtime-2ea7e.appspot.com"
})
# # Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    async def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
    async def call(self):
        studentInfo = db.reference(f'Students/{id}').get()
        print(studentInfo) 
    async def main1(self):
        # task = asyncio.create_task(self.encode_faces())
        task = asyncio.create_task(self.call())
    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')
        file = open('EncodeFile.p', 'rb')
        encodeListKnownWithIds = pickle.load(file)
        file.close()
        print("Encode File Loaded")
        self.known_face_encodings, self.known_face_names = encodeListKnownWithIds
        modeType = 0
        counter = 0
        id = -1
        imgStudent = []
        v = [0,0,0,0,0,0]
        dictionary = dict(zip(self.known_face_names, v))
        while True:
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                # rgb_small_frame = small_frame[:, :, ::-1] # This will also convert the rbg to bgr
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                ''
                # v = [0,0,0,0,0,0]
                # dictionary = dict(zip(self.known_face_names, v))
                # print(dictionary)
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                        id = name

                        if counter == 0:
                            cv2.waitKey(1)
                            counter = 1
                            modeType = 1
                    if counter != 0:
                        

                        if counter == 1:
                            # Get the Data
                            studentInfo = db.reference(f'Students/{id}').get()
                            print(studentInfo)    
                            # asyncio.run(self.main1())
                    counter +=1       
                    dictionary[name] = dictionary.get(name, 1) + 1
                    for i in dictionary:
                        if(dictionary[i] == 1):
                            # value.append(i)
                            # break
                            dictionary[name] = dictionary.get(name, 1) + 1
                            voice.speak(f"Good Morning {i}")
                            print("Good Morning",i)
                            # continue
                            # exit()
                    # value = {i for i in dictionary if dictionary[i]==1}
                    # print("key by value:",value)
                    self.face_names.append(f'{name} ({confidence})')
                    # print("fsdhiansdiu")
                    # continue

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    # fr.run_recognition()
    async def main():
        await asyncio.gather(
            fr.run_recognition(),
            # fr.main1()
        )
    asyncio.run(main())