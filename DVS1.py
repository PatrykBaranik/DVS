import matplotlib.pyplot as plt
import numpy as np

file = open("events.txt", 'r')
splited = file.read().split('\n')
time, cordx, cordy, pol = [], [], [], []

for i in splited:
    t, cx, cy, p = i.split(' ')
    t, cx, cy, p = float(t), float(cx), float(cy), float(p)
    if t > 1:
        break
    time += [t]
    cordx += [cx]
    cordy += [cy]
    pol += [p]


print("number of events")
print(len(time))
print("first timestamp")
print(time[0])
print("last timestamp")
print(time[len(time)-1])
print("maximum values of pixel coordinates x")
print(max(cordx))
print("minimum values of pixel coordinates x")
print(min(cordx))
print("maximum values of pixel coordinates y")
print(max(cordy))
print("minimum values of pixel coordinates y")
print(min(cordy))
print("sum of polarity")
print(sum(pol))

start = 0
end = 0
for i in range(len(time)):
    if float(time[i]) >= 0.5 and start == 0:
        start = i
    if float(time[i]) >= 1.:
        end = i
        break

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
for i in range(start, end, 200):#(len(time)):
    xs = cordx[i]
    ys = cordy[i]
    zs = time[i]
    if pol[i]>0:
        ax.scatter(xs, zs, ys, color='red')
    else:
        ax.scatter(xs, zs, ys, color='blue')

ax.set_xlabel('X Label')
ax.set_ylabel('T Label')
ax.set_zlabel('Y Label')

plt.show()
print("fin")