# coding: utf-8
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.activations import relu, softmax

from .BaseModel import BaseModel


class VehicleModel(BaseModel):
    '''
    0 非车
    1 轿车
    2 面包车
    3 客车
    4 小货车
    5 货车
    6 其他车型
    '''
    __dict = dict()

    def __init__(self, sess=None):
        super().__init__(sess)

    @classmethod
    def _getitem(cls, key):
        if not cls.__dict:
            items1 = ['非车', '轿车', '面包车', '客车', '小货车', '货车', '其他车型']
            items2 = list(range(len(items1)))

            keys = items1 + items2
            values = items2 + items1

            cls.__dict = dict(zip(keys, values))

        return cls.__dict[key]

    @property
    def category_count(self):
        return 7

    @property
    def input_shape(self):
        return (64, 64, 3)

    def _build_model(self):
        model = Sequential()

        # 64 -> 60 -> 30
        model.add(Conv2D(16, 5, activation=relu, input_shape=self.input_shape))
        model.add(MaxPool2D(2))

        # 30 -> 28 -> 14
        model.add(Conv2D(32, 3, activation=relu))
        model.add(MaxPool2D(2))

        # 14 -> 12 -> 6
        model.add(Conv2D(64, 3, activation=relu))
        model.add(Dropout(0.5))
        model.add(MaxPool2D(2))

        # 6 * 6 * 64 -> 2304
        model.add(Flatten())

        # 2304 -> 512 -> 64 -> output
        model.add(Dense(512, activation=relu))
        model.add(Dense(64, activation=relu))
        model.add(Dense(self.category_count, activation=softmax))

        return model
