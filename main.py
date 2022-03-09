import mediapipe as mp
import cv2
import time
import numpy as np
import pandas as pd
import os

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils # For drawing keypoints
points = mpPose.PoseLandmark # Landmarks
path = "DATASET/TRAIN/plank" # enter dataset path
data = []
for p in points:
        x = str(p)[13:]
        data.append(x + "_x")
        data.append(x + "_y")
        data.append(x + "_z")
        data.append(x + "_vis")
data = pd.DataFrame(columns = data) # Empty dataset
cap = cv2.VideoCapture(0)
i = 0
 
while(cap.isOpened()):
    ret, frame = cap.read()
     
    # This condition prevents from infinite looping
    # incase video ends.
    if ret == False:
        break

    temp = []

    img = frame

    imageWidth, imageHeight = img.shape[:2]

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    blackie = np.zeros(img.shape) # Blank image

    results = pose.process(imgRGB)

    if results.pose_landmarks:

            # mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #draw landmarks on image

            mpDraw.draw_landmarks(blackie, results.pose_landmarks, mpPose.POSE_CONNECTIONS) # draw landmarks on blackie
            
            landmarks = results.pose_landmarks.landmark
            for i,j in zip(points,landmarks):

                temp = temp + [j.x, j.y, j.z, j.visibility]
            

            data.loc[0] = temp

            print(data["LEFT_WRIST_y"])
            #print(data.tail(0)["LEFT_WRIST_y"].values)
            # if (data.tail(1)["LEFT_WRIST_y"].values[0]>=1):
            #     print("kiri")
            # elif (data.tail(1)["RIGHT_WRIST_y"].values[0]>=1):
            #     print("Kanan")
            # else:
            #     print("nothing happen")
    cv2.imshow("Image", img)

    cv2.imshow("blackie",blackie)

    cv2.waitKey(100)
data.to_csv("datasetkanan.csv")
