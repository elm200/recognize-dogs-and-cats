import os
import random
import numpy as np
from glob import glob
import tensorflow as tf
from tensorflow.contrib.keras.python.keras.models import Sequential
from tensorflow.contrib.keras.python.keras.layers import Convolution2D, MaxPooling2D
from tensorflow.contrib.keras.python.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.contrib.keras.python.keras.preprocessing.image import load_img, img_to_array
from pprint import pprint

class Predictor:
    def __init__(self):
        self.model = self.create_model()
        self.kinds = ["CAT", "DOG"]

    def get_sample_items(self):
        n_samples = 3
        sample_dir = "./static/images/samples/"
        samples = [f for f in glob(os.path.join(sample_dir, "*.jpg"))]
        paths = random.sample(samples, n_samples)
        preds = self.predict_images(paths)

        items = []
        for p, pred in zip(paths, preds):
            max_i = np.argmax(pred)
            prob = "%.1f" % (pred[max_i] * 100)
            kind = self.kinds[max_i]
            items.append(dict(image=os.path.basename(p),
                              prob=prob,
                              kind=kind))
        return items

    def get_image_item(self, img_path):
        pred = self.predict_images([img_path])[0]
        max_i = np.argmax(pred)
        prob = "%.1f" % (pred[max_i] * 100)
        kind = self.kinds[max_i]
        item = dict(prob=prob, kind=kind)
        return item

    # Special thanks to http://qiita.com/agumon/items/ab2de98a3783e0a93e66
    def create_model(self):
        self.graph = tf.get_default_graph()

        model = Sequential()

        model.add(Convolution2D(32, 3, 3, input_shape=(128, 128, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Convolution2D(64, 3, 3))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2))
        model.add(Activation('softmax'))

        model.load_weights("./data/simple_cnn_model91-loss0.34-acc0.85-vloss0.36-vacc0.85.hdf5")

        return model

    def predict_images(self, paths):
        images = []
        for p in paths:
            img = load_img(p, target_size=(128,128))
            img = img_to_array(img) / 255.0
            images.append(img)
        images = np.array(images)
        with self.graph.as_default():
            res = self.model.predict(images)
        return res
