import numpy as np
import cv2
import scipy.optimize 
import math
import DVS2

frame_00000022 = cv2.imread("shape_rotation/images/frame_00000022.png", cv2.IMREAD_GRAYSCALE)


# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 200;
# Filter
params.filterByArea = True
params.minArea = 100
params.filterByCircularity = False
params.filterByConvexity = False
ver = (cv2.__version__).split(".")
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else :
    detector = cv2.SimpleBlobDetector_create(params)
    
keypoints = detector.detect(frame_00000022)
outImage = frame_00000022

objects = []
for keypoint in keypoints:
    objects.append([int(keypoint.pt[0]), int(keypoint.pt[1]), int(keypoint.size)])
    
for i in objects:    
    print(i)

outImage = cv2.drawKeypoints(frame_00000022, keypoints, outImage)
cv2.imshow("res" , outImage)


    
    


file = open("shape_rotation/events.txt", 'r')
splited = file.read().split('\n')
time, cordx, cordy, pol = [], [], [], []




    


frame = 1
tau = 0.01
tim = []
i = 0
for iv in splited:
    t, cx, cy, p = iv.split(' ')
    t, cx, cy, p = float(t), float(cx), float(cy), float(p)
    if t<1:
        continue
    if t>1:
        i+=1
        time += [t]
        cordx += [int(cx)]
        cordy += [int(cy)]
        pol += [p]
    if t>5:
        break
    for j in objects:
        distance = np.sqrt((int(j[0])-cordx[i])**2 +  (int(j[1])-cordy[i])**2)
        object_diameter = j[2]
        old_center_x = j[0]
        old_center_y = j[1]
        event_x = cordx[i]
        event_y = cordy[i]
        if (distance < object_diameter/2 and distance > 0):
            new_center_x = old_center_x + (event_x - old_center_x)/2
            new_center_y = old_center_y + (event_y - old_center_y)/2
            objects[j.key] = [new_center_x, new_center_y, object_diameter]
            continue
    if t[i] > frame+tau:
        e_frame = DVS2.event_frame(time, cordx, cordy, pol, tau, 240,180) 
        
        for i in range(objects):
            keypoints[i].pt[0] = objects[i][0]
            keypoints[i].pt[1] = objects[i][1]
            keypoints[i].pt.size = objects[i][2]
        outImage = cv2.drawKeypoints(e_frame, keypoints, e_frame)
        cv2.imshow("res" , outImage)
                
        
        
