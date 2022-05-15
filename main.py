from decimal import ROUND_UP
import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
from connectArduino import write_read
import math

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils # For drawing keypoints
points = mpPose.PoseLandmark # Landmarks
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

    #Start marker
    val = write_read(1)
    print(val)

    if results.pose_landmarks:
        #Ada Orang
        val = write_read(1)
        print(val)

        # mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #draw landmarks on image

        mpDraw.draw_landmarks(blackie, results.pose_landmarks, mpPose.POSE_CONNECTIONS) # draw landmarks on blackie
            
        landmarks = results.pose_landmarks.landmark
        for i,j in zip(points,landmarks):

            temp = temp + [j.x, j.y, j.z, j.visibility]
            

        data.loc[0] = temp

        if (data.tail(1)["LEFT_WRIST_y"].values[0]<1 or data.tail(1)["RIGHT_WRIST_y"].values[0]<1):

            rounding = lambda x : 9 if (x>0.9) else (1 if x<0.1 else math.ceil(x*10))

            valxkiri = write_read(rounding(float(data.tail(1)["LEFT_WRIST_x"].values[0])))
            valykiri = write_read(255-round(data.tail(1)["LEFT_WRIST_y"].values[0]*255))
            valxkanan = write_read(rounding(float(data.tail(1)["RIGHT_WRIST_x"].values[0])))
            valykanan = write_read(255-round(data.tail(1)["RIGHT_WRIST_y"].values[0]*255))
            print(f"X Kanan: {valxkanan} Y Kanan: {valykanan} X Kiri: {valxkiri} Y Kiri: {valykiri}")

        #     if(data.tail(1)["LEFT_WRIST_x"].values[0]>0.9 and data.tail(1)["RIGHT_WRIST_x"].values[0]>0.9):
        #         valxkiri = write_read(9)
        #         valykiri = write_read(255-round(data.tail(1)["LEFT_WRIST_y"].values[0]*255))
        #         valxkanan = write_read(9)
        #         valykanan = write_read(255-round(data.tail(1)["RIGHT_WRIST_y"].values[0]*255))
        #     elif(data.tail(1)["LEFT_WRIST_x"].values[0]<0.1):
        #         valx = write_read(1)
        #         valy = write_read(255-round(data.tail(1)["LEFT_WRIST_y"].values[0]*255))
        #     else:
        #         valx = write_read(math.ceil(data.tail(1)["LEFT_WRIST_x"].values[0]*10))
        #         valy = write_read(255-round(data.tail(1)["LEFT_WRIST_y"].values[0]*255))
        #     print(valx,valy)


        # elif (data.tail(1)["RIGHT_WRIST_y"].values[0]<1):
        #     if(data.tail(1)["RIGHT_WRIST_x"].values[0]>0.9):
        #         valx = write_read(9)
        #         valy = write_read(255-round(data.tail(1)["RIGHT_WRIST_y"].values[0]*255))
        #     elif(data.tail(1)["RIGHT_WRIST_x"].values[0]<0.1):
        #         valx = write_read(1)
        #         valy = write_read(255-round(data.tail(1)["RIGHT_WRIST_y"].values[0]*255))
        #     else:
        #         valx = write_read(math.ceil(data.tail(1)["RIGHT_WRIST_x"].values[0]*10))
        #         valy = write_read(255-round(data.tail(1)["RIGHT_WRIST_y"].values[0]*255))
        #     print(valx,valy)
    else:
        #Ga ada
        val = write_read(0)
        print(val)
    cv2.imshow("Image", img)

    cv2.imshow("blackie",blackie)

    cv2.waitKey(100)