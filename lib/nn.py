import os
import random
import numpy as np
from glob import glob
import tensorflow as tf
from keras.applications.vgg16 import VGG16
from keras.models import Input, Model, Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing.image import load_img, img_to_array
from pprint import pprint

class Predictor:
    def __init__(self):
        self.model = self.create_model()
        self.kinds = ["CAT", "DOG"]

    def get_prob_and_kind(self, pred):
        if pred < 0.5:
            prob = "%.1f" % ((1 - pred) * 100)
            kind = self.kinds[0]
        else:
            prob = "%.1f" % (pred * 100)
            kind = self.kinds[1]
        return (prob, kind)

    def get_sample_items(self):
        n_samples = 3
        sample_dir = "./static/images/samples/"
        samples = [f for f in glob(os.path.join(sample_dir, "*.jpg"))]
        paths = random.sample(samples, n_samples)
        preds = self.predict_images(paths)

        items = []
        for p, pred in zip(paths, preds):
            prob, kind = self.get_prob_and_kind(pred)
            items.append(dict(image=os.path.basename(p),
                              prob=prob,
                              kind=kind))
        return items

    def get_image_item(self, img_path):
        pred = self.predict_images([img_path])[0]
        prob, kind = self.get_prob_and_kind(pred)
        item = dict(prob=prob, kind=kind)
        return item

    # Special thanks to http://aidiary.hatenablog.com/entry/20170110/1484057655
    def create_model(self):
        self.graph = tf.get_default_graph()

        vgg16_model = VGG16(include_top=False, weights='imagenet', input_tensor=Input(shape=(150, 150, 3)))

        top_model = Sequential()
        top_model.add(Flatten(input_shape=vgg16_model.output_shape[1:]))
        top_model.add(Dense(256, activation='relu'))
        top_model.add(Dropout(0.5))
        top_model.add(Dense(1, activation='sigmoid'))

        model = Model(inputs=vgg16_model.input, outputs=top_model(vgg16_model.output))

        model.summary()
        model.load_weights("./data/weights/vgg16_finetune_model39-loss0.13-acc0.95-vloss0.16-vacc0.94.h5")

        return model

    def predict_images(self, paths):
        images = []
        for p in paths:
            img = load_img(p, target_size=(150,150))
            img = img_to_array(img) / 255.0
            images.append(img)
        images = np.array(images)
        with self.graph.as_default():
            res = self.model.predict(images)
        return res
