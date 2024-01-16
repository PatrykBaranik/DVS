import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt


def part1():
    train_ds = tf.keras.utils.image_dataset_from_directory("frame_data/Train", image_size=(34, 34), batch_size=32)
    val_ds = tf.keras.utils.image_dataset_from_directory("frame_data/Test", image_size=(34, 34), batch_size=32)
    return train_ds, val_ds


def part2():
    num_classes = 10
    model = tf.keras.Sequential([
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.MaxPooling2D(), 
        tf.keras.layers.MaxPooling2D(), 
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    opt = tf.keras.optimizers.Adam()
    model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(), optimizer=opt, metrics=["accuracy"])
    return model


def part3():
    train_ds, val_ds = part1()
    model = part2()
    history = model.fit(train_ds, validation_data=val_ds, epochs=5, batch_size=32)
    model.save("model")

    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.figure()
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc ='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc ='upper left')
    plt.show()


def part4():
    model = tf.keras.models.load_model("model")

    image = cv2.imread("frame_data/Test/7/00027875.png")
    image_to_pred = image.reshape(1, 34, 34, 3)
    predict = model.predict(image_to_pred, batch_size=1)
    for x in range(10):
        value = float(predict[0][x])
        print("The probaility that the number is " + str(x) + " equals " + str(value*100) + " %")
    #cv2.imshow("IMG", image)
    #cv2.waitKey()
    train_ds, val_ds = part1()
    print( "Evaluation results: " + str(model.evaluate(val_ds)))


part3()
part4()

