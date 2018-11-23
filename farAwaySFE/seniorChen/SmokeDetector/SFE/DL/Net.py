# coding: utf-8
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.activations import relu, softmax


from .BaseModel import BaseModel


class Net(BaseModel):

    def __init__(self, sess=None):
        super().__init__(sess)

    @property
    def category_count(self):
        return 2

    @property
    def input_shape(self):
        return (128, 128, 3)

    def _build_model(self):
        model = Sequential()

        # 128 -> 124 -> 62
        model.add(Conv2D(6, 5, activation=relu, input_shape=self.input_shape))
        model.add(MaxPool2D(2))

        # 62 -> 58 -> 29
        model.add(Conv2D(16, 5, activation=relu))
        model.add(MaxPool2D(2))

        # 29 -> 25 -> 12
        model.add(Conv2D(32, 5, activation=relu))
        model.add(Dropout(0.5))
        model.add(MaxPool2D(2))

        # 12 * 12 * 32 -> 4608
        model.add(Flatten())

        # 4608 -> 120 -> 84 -> 2
        model.add(Dense(120, activation=relu))
        model.add(Dense(84, activation=relu))
        model.add(Dense(self.category_count, activation=softmax))

        return model
