from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense, MaxPool2D
from keras.activations import relu, softmax

from SFE.DL.BaseModel import BaseModel


class Net(BaseModel):

    def __init__(self, sess=None):
        super().__init__(sess)

    @property
    def category_count(self) -> int:
        return 2

    @property
    def input_shape(self) -> tuple:
        return (512, 512, 3)

    def _build_model(self):
        model = Sequential()

        # 512 -> 256
        model.add(Conv2D(4, 5, input_shape=self.input_shqpe, padding="same", activation=relu))
        model.add(MaxPool2D())

        # 256 - > 128
        model.add(Conv2D(8, 5, padding="same", activation=relu))
        model.add(MaxPool2D())

        # 128 -> 64
        model.add(Conv2D(16, 5, padding="same", activation=relu))
        model.add(MaxPool2D())

        # 64 -> 32
        model.add(Conv2D(32, 3, padding="same", activation=relu))
        model.add(MaxPool2D())

        # 32 * 32 * 32 -> 32768
        model.add(Flatten())

        model.add(Dense(8192, activation=relu))
        model.add(Dense(1024, activation=relu))
        model.add(Dense(256, activation=relu))
        model.add(Dense(64, activation=relu))
        model.add(Dense(self.category_count, activation=softmax))

        return model
