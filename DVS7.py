import numpy as np
import cv2
import scipy.optimize 

import DVS2

def contrast_presentation(params, xs, ys, ts, ps, image_shape):
    t_max = max(ts)
    h_image = np.zeros(image_shape)
    for i in range(len(xs)):
        x_wraped = xs[i] + 1000000 * params[0] * (t_max-ts[i])
        y_wraped = ys[i] + 1000000 * params[1] * (t_max-ts[i])
        if 0<=x_wraped<image_shape[0] and 0<=y_wraped<image_shape[1]:
            h_image[int(x_wraped), int(y_wraped)] += 1
    return h_image

def contrast(params, xs, ys, ts, ps, image_shape):
    t_max = max(ts)
    h_image = np.zeros(image_shape)
    for i in range(len(xs)):
        x_wraped = xs[i] + 1000000 * params[0] * (t_max-ts[i])
        y_wraped = ys[i] + 1000000 * params[1] * (t_max-ts[i])
        if 0<=x_wraped<image_shape[0] and 0<=y_wraped<image_shape[1]:
            h_image[int(x_wraped), int(y_wraped)] += 1
    value = -1 * np.var(h_image)
    return value


file = open("events.txt", 'r')
splited = file.read().split('\n')
time, cordx, cordy, pol = [], [], [], []
frame = 1
tau = 0.01
shape = (180,240)
for i in splited:
    t, cx, cy, p = i.split(' ')
    t, cx, cy, p = float(t), float(cx), float(cy), float(p)
    if t > frame+tau:
        im = DVS2.event_frame(time, cordy, cordx, pol, tau, shape)
        xs_temp, ys_temp, ts_temp, ps_temp = cordx, cordy, time, pol
        time, cordx, cordy, pol = [], [], [], []

        args = (xs_temp, ys_temp, ts_temp, ps_temp, (180, 240))
        argmax = scipy.optimize.fmin(contrast, (0, 0), args=args, disp=False)
        print(argmax)
        frame += tau
        conc = contrast_presentation(argmax, ys_temp, xs_temp, ts_temp, ps_temp, (180, 240))
        cv2.imshow("concrast", conc)
        #cv2.imshow("frame",image)
        cv2.waitKey(1000)
    else:
        if t>1:
            time += [t]
            cordx += [int(cx)]
            cordy += [int(cy)]
            pol += [p]
        if t>2.1:
            break
