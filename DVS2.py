import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import cv2


def event_frame(t, cx, cy, p, tau, shape):
    image = np.ones(shape)
    image = image * 127
    image = image.astype(np.uint8)
    for i in range(len(t)):
        if p[i] > 0:
            image[cx[i], cy[i]] = np.uint(255)
        else:
            image[cx[i], cy[i]] = np.uint(0)
    return image


def exponential_decay(timestamps,coordinatesx, coordinatesy, polarities, tau, shape):
    image = np.zeros(shape)
    ct = max(timestamps)
    for i in range(len(timestamps)):
        t = timestamps[i]
        if t > ct:
            break
        cx = coordinatesx[i]
        cy = coordinatesy[i]
        if  polarities[i] > 0:
            image[cx, cy] += 1 * np.exp((ct-t)/tau)
        else:
            image[cx, cy] += -1 * np.exp((ct-t)/tau)
    norm = np.zeros(shape)
    normalizedImg = cv2.normalize(image, shape, 0, 255, cv2.NORM_MINMAX)
    normalizedImg = np.array(normalizedImg, np.uint8)
    return normalizedImg

def event_frequency(timestamps,coordinatesx, coordinatesy, polarities, tau, shape):
    image = np.zeros(shape)
    for i in range(len(timestamps)):
        t = timestamps[i]
        cx = coordinatesx[i]
        cy = coordinatesy[i]
        image[cx, cy] += 1


    imageRes = np.zeros(shape)
    for x in range(shape[1]):
        for y in range(shape[0]):
            imageRes[y,x] = 255/(1+np.exp(-1*image[y,x]/2))


    norm = np.zeros(shape)
    normalizedImg = cv2.normalize(imageRes, shape, 0, 255, cv2.NORM_MINMAX)
    normalizedImg = np.array(normalizedImg, np.uint8)
    return normalizedImg

def res():
    file = open("events.txt", 'r')
    splited = file.read()
    splited = splited.split('\n')
    file.close()
    time, cordx, cordy, pol = [], [], [], []
    shape = (240, 180)
    for i in splited:
        t, cx, cy, p = i.split(' ')
        t, cx, cy, p = float(t), float(cx), float(cy), float(p)
        if t < 1:
            continue
        if t > 1.21:
            break
        time += [t]
        cordx += [int(cx)]
        cordy += [int(cy)]
        pol += [p]
    lent = len(time)
    frame = 1
    tau = 0.01
    t, cx, cy, p = [],[],[],[]

    for i in range(lent):
        if time[i] < 1 + frame * tau:
            t += [time[i]]
            cx += [cordx[i]]
            cy += [cordy[i]]
            p += [pol[i]]
        else:
            image_e_frame = event_frame(t, cx, cy, p, tau, shape)
            image_e_decay = exponential_decay(t, cx, cy, p, tau, shape)
            image_e_freq = event_frequency(t, cx, cy, p, tau, shape)
            print(frame)
            frame += 1
            t, cx, cy, p = [], [], [], []
            image = np.concatenate((image_e_frame, image_e_decay, image_e_freq), axis=1)
            cv2.imshow("snap", image)
            cv2.waitKey()
    exit()

res()