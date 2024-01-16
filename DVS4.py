import os
import open_bin as ob
import DVS2
test_path = "raw_data/Test"
train_path = "raw_data/Train"


def counter(path):
    counter_ = 0
    for dir_list in os.listdir(path):
        for file in os.listdir(test_path + "/" + str(dir_list)):
            counter_ += 1
    return counter_


def viewer(path):
    counter_ = 0
    events = 0
    for dir_listed in os.listdir(path):
        for file_listed in os.listdir(test_path + "/" + str(dir_listed)):
            ts, x, y, p, h, w = ob.read_dataset(test_path + "/" + str(dir_listed) + "/" + str(file_listed))
            print(test_path + "/" + str(dir_listed) + "/" + str(file_listed) + ": " + str(len(ts)) + " " + str(w) + " " + str(h))
            events += len(ts)
            counter_ += 1
    return events/counter_


def preperer(test_path, res_path):
    counter_ = 0
    events = 0
    for dir_listed in os.listdir(test_path):
        for file_listed in os.listdir(test_path + "/" + str(dir_listed)):
            ts, x, y, p, h, w = ob.read_dataset(test_path + "/" + str(dir_listed) + "/" + str(file_listed))
            image_e_decay = DVS2.exponential_decay(ts, x, y, p, 1, (34,34))



for i in range(lent):
    if time[i] < 1 + frame * tau:
        t += [time[i]]
        cx += [cordx[i]]
        cy += [cordy[i]]
        p += [pol[i]]
    else:



#print(counter(test_path))
#print(counter(train_path))
#print(viewer(test_path))
#print(viewer(train_path))
