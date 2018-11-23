# coding: utf-8
import os
from os import path

import cv2
import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from keras.metrics import categorical_accuracy
from keras.utils import to_categorical

from .Dataset import Dataset

#元类 类的工厂
class BaseModelMetaclass(type):

    def __init__(self, name, bases, attrs):
        key = '_getitem'
        if key in attrs:
            self.__getitem = attrs[key]
        else:
            def getitem(x):
                raise KeyError()
            self.__getitem = getitem

    def __getitem__(self, key):
        return self.__getitem(key)


class BaseModel(metaclass=BaseModelMetaclass):
    ''' ### 神经网络模型基类
    这个类不能单独实例化 单独实例化时会**抛出异常** 子类必须实现下列属性/方法:

    - ```
    @property
    def category_count() -> int # 子类必须拥有这个属性 这个属性返回这个模型的分类总数
    ```

    - ```
    @property
    def input_shape() -> tuple # 子类必须拥有这个属性 这个属性返回这个模型输入数据的shape, 返回格式为 (高度, 宽度, 通道数)
    ```

    - ```
    def _build_model() -> keras.models.Model # 子类必须实现这个方法 这个方法返回一个`keras`模型
    ```

    可以实现下列方法任一方法 用于实现类级的`__getitem__`(可选):

    - ```
    @classmethod
    def _getitem(cls, key) -> any
    ```

    - ```
    @staticmethod
    def _getitem(key) -> any
    ```
    '''

    @property
    def category_count(self) -> int:
        ''' 子类必须拥有这个属性 这个属性返回这个模型的分类总数 '''
        raise NotImplementedError()

    @property
    def input_shape(self) -> tuple:
        ''' 子类必须拥有这个属性 这个属性返回这个模型输入数据的shape '''
        raise NotImplementedError()

    def _build_model(self) -> Model:
        ''' 子类必须实现这个方法 这个方法返回一个`keras`模型 '''
        raise NotImplementedError()

    @property
    def input_dim(self) -> int:
        ''' 返回输入数据的维数 '''
        return len(self.input_shape)

    def __init__(self, sess=None):
        ''' 该网络使用的`tf.Session` 为`None`时会自动创建 '''
        if isinstance(sess, tf.Session):
            self.__self_sess = False
            self.__sess = sess
        else:
            self.__self_sess = True
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            self.__sess = tf.Session(config=config)

        # 编译模型
        with self.__sess.as_default():
            self.__model = self._build_model()
            optimizer = Adam()
            self.__model.compile(optimizer=optimizer, loss=categorical_crossentropy, metrics=[categorical_accuracy])

    def __del__(self):
        # 为自动创建的Session时自动释放
        if self.__self_sess:
            self.__sess.close()

    def load(self, model_path: str) -> bool:
        ''' 加载模型, 返回加载是否成功 '''
        try:
            assert isinstance(model_path, str), '模型路径类型必须为`str`'
            assert path.isfile(model_path), '模型路径不存在'

            with self.__sess.as_default():
                self.__model.load_weights(model_path)
                return True
        except:
            # 输出异常信息
            import traceback
            traceback.print_exc()
            return False

    def save(self, save_path: str) -> bool:
        ''' 保存模型, 返回保存是否成功 '''
        try:
            assert isinstance(save_path, str), '模型路径类型必须为`str`'

            with self.__sess.as_default():
                self.__model.save_weights(save_path)
                return True
        except:
            # 输出异常信息
            import traceback
            traceback.print_exc()
            return False

    def train(self, dataset: Dataset, epochs: int, batch_size=32, save_path=None):
        ''' 训练模型
        dataset: 数据集, 类型必须为`SFE.DL.Dataset`
        epochs: 训练轮数
        batch_size: 每批图片的大小
        save_path: 训练完成后模型的保存路径, 为`None`时不保存
        '''
        if not isinstance(dataset, Dataset):
            return

        # 转换数据格式、标签格式
        data = dataset.data
        data = self.__convert(data)
        label = dataset.labels
        label = to_categorical(label, self.category_count)

        # 开始训练
        with self.__sess.as_default():
            self.__model.fit(
                x=data,
                y=label,
                batch_size=batch_size,
                epochs=epochs
            )

        # 保存模型
        if save_path:
            self.save(save_path)

    def predict(self, data: np.ndarray) -> list:
        ''' 使用当前模型预测输入数据的类别 '''
        # 转换数据格式
        data = self.__convertData(data)
        data = self.__convert(data)

        # 识别
        with self.__sess.as_default():
            logits = self.__model.predict_on_batch(data)

        # 格式化结果
        result = np.argmax(logits, 1)

        return result

    def __convert(self, data):
        return (data / 255).astype('float32')

    def __convertData(self, data):
        ''' 用于将单张或多张图片数据转换为可以被当前网络直接使用的数据
        data: 要转换的数据 类型必须为`list`、`tuple`、`numpy.ndarray`中的一种, 图片数据类型必须为`numpy.ndarray`
        return: 返回转换后的图片
        '''
        # 判断类型
        assert isinstance(data, (tuple, list, np.ndarray)), f'输入数据类型必须为(tuple|list|np.ndarray), 不能为`{type(data)}`'

        # 如果为单张图片
        if isinstance(data, np.ndarray) and data.ndim == self.input_dim:
            data = data.reshape((-1, *data.shape))

        # 重置大小
        shape = self.input_shape[1::-1]
        size = len(data)
        ret = np.zeros((size, *self.input_shape))
        for i in range(size):
            assert isinstance(data[i], np.ndarray), '数据类型必须为`np.ndarray`'
            assert data[i].ndim == self.input_dim, '输入数据维数错误'
            ret[i] = cv2.resize(data[i], shape)

        return ret
