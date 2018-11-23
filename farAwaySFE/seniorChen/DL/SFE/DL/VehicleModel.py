# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\DL\VehicleModel.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 1650 bytes
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.activations import relu, softmax
from .BaseModel import BaseModel

class VehicleModel(BaseModel):
    """
    0 非车
    1 轿车
    2 面包车
    3 客车
    4 小货车
    5 货车
    6 其他车型
    """
    _VehicleModel__dict = dict()

    def __init__(self, sess=None):
        super().__init__(sess)

    @classmethod
    def _getitem(cls, key):
        if not cls._VehicleModel__dict:
            items1 = [
             '非车', '轿车', '面包车', '客车', '小货车', '货车', '其他车型']
            items2 = list(range(len(items1)))
            keys = items1 + items2
            values = items2 + items1
            cls._VehicleModel__dict = dict(zip(keys, values))
        return cls._VehicleModel__dict[key]

    @property
    def category_count(self):
        return 7

    @property
    def input_shape(self):
        return (64, 64, 3)

    def _build_model(self):
        model = Sequential()
        model.add(Conv2D(16, 5, activation=relu, padding='same', input_shape=self.input_shape))
        model.add(MaxPool2D(2))
        model.add(Conv2D(32, 3, activation=relu, padding='same'))
        model.add(MaxPool2D(2))
        model.add(Conv2D(64, 3, activation=relu, padding='same'))
        model.add(Dropout(0.5))
        model.add(MaxPool2D(2))
        model.add(Flatten())
        model.add(Dense(512, activation=relu))
        model.add(Dense(self.category_count, activation=softmax))
        return model
# okay decompiling SFE\DL\VehicleModel.pyc
