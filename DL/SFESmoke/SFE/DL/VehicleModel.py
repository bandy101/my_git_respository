# coding: utf-8
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.activations import relu, softmax

from .BaseModel import BaseModel


class VehicleModel(BaseModel):
    '''
    0 非车
    1 行人_摩托_三轮
    2 轿车
    3 面包车
    4 客车
    5 小货车
    6 货车
    7 其他车型
    '''
    __dict = dict()

    def __init__(self, sess=None):
        super().__init__(sess)

    @classmethod
    def _getitem(cls, key):
        if not cls.__dict:
            items1 = ['非车', "行人_摩托_三轮", '轿车', '面包车', '客车', '小货车', '货车', '其他车型']
            items2 = list(range(len(items1)))

            keys = items1 + items2
            values = items2 + items1

            cls.__dict = dict(zip(keys, values))

        return cls.__dict[key]

    @property
    def category_count(self):
        return 8

    @property
    def input_shape(self):
        return (128, 128, 3)

    def _build_model(self):
        model = Sequential()

        # 128 -> 64
        model.add(Conv2D(8, 5, activation=relu, padding="same", input_shape=self.input_shape))
        model.add(MaxPool2D(2))

        # 64 -> 32
        model.add(Conv2D(16, 3, activation=relu, padding="same"))
        model.add(MaxPool2D(2))

        # 32 -> 16
        model.add(Conv2D(32, 3, activation=relu, padding="same"))
        model.add(MaxPool2D(2))

        # 16 * 16 * 32 -> 8192 * 1
        model.add(Flatten())

        # 8192 -> 512 -> 64 -> output
        model.add(Dense(512, activation=relu))
        model.add(Dense(64, activation=relu))
        model.add(Dense(self.category_count, activation=softmax))

        return model
