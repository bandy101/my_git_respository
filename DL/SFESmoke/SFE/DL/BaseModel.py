# coding: utf-8
import os
from os import path
import stat
from tempfile import mkstemp

import cv2
import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from keras.metrics import categorical_accuracy
from keras.utils import to_categorical


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

    __DEFAULT_KEY = "gd - sfe"

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
        ''' - sess tf.Session[None]: 该网络使用的`tf.Session` 为`None`时会自动创建 '''
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
            self.__graph = tf.get_default_graph()

    def __del__(self):
        # 为自动创建的Session时自动释放
        if self.__self_sess:
            self.__sess.close()

    def load(self, model_path: str or bytes, key=None) -> bool:
        ''' 加载权重
        - model_path str/bytes: 要加载的模型权重文件的路径或模型文件数据
        - key str[None]: 密钥, 为`None`时表示使用默认密钥加密

        - return bool: 返回加载是否成功
        '''
        if key is None:
            key = self.__DEFAULT_KEY
        try:
            if not isinstance(model_path, (str, bytes)):
                raise Exception('模型路径类型必须为`str/bytes`')

            if isinstance(model_path, str):
                if not path.isfile(model_path):
                    raise Exception('模型路径不存在')

                fd, fp = mkstemp()
                os.chmod(fp, 0o700)

                if isinstance(model_path, bytes):
                    self.__decryptData(model_path, fd, key)
                else:
                    self.__decrypt(model_path, fd, key)

                model_path = fp

            with self.__sess.as_default():
                with self.__graph.as_default():
                    self.__model.load_weights(model_path)
                    try:
                        os.remove(fp)
                    except:
                        pass
                    return True
        except:
            # 输出异常信息
            import traceback
            traceback.print_exc()
            return False

    def save(self, save_path: str, key=None) -> bool:
        ''' 保存权重
        - save_path str: 权重保存路径
        - key str[None]: 密钥, 为`None`时表示使用默认密钥加密

        - reutrn bool: 返回保存是否成功
        '''
        try:
            if not isinstance(save_path, str):
                raise Exception('模型路径类型必须为`str`')
            if key is None:
                key = self.__DEFAULT_KEY

            with self.__sess.as_default():
                with self.__graph.as_default():
                    self.__model.save_weights(save_path)
                    self.encrypt(save_path, key=key)
                    return True
        except:
            # 输出异常信息
            import traceback
            traceback.print_exc()
            return False

    def train(self, dataset, epochs: int, batch_size=32, save_path=None, key=None):
        ''' 训练模型
        - dataset SFE.DL.Dataset: 数据集, 类型必须为`SFE.DL.Dataset`
        - epochs int: 训练轮数
        - batch_size int[32]: 每批图片的大小
        - save_path str[None]: 训练完成后模型的保存路径, 为`None`时不保存
        - key str[None]: 密钥, 为`None`时表示使用默认密钥加密
        '''
        from .Dataset import Dataset

        if not isinstance(dataset, Dataset):
            return

        optimizer = Adam()
        self.__model.compile(optimizer=optimizer, loss=categorical_crossentropy, metrics=[categorical_accuracy])

        # 转换数据格式、标签格式
        data = dataset.data
        data = self._convert(data)
        label = dataset.labels
        label = to_categorical(label, self.category_count)

        # 开始训练
        with self.__sess.as_default():
            with self.__graph.as_default():
                self.__model.fit(
                    x=data,
                    y=label,
                    batch_size=batch_size,
                    epochs=epochs
                )

        # 保存模型
        if save_path:
            self.save(save_path, key)

    def predict(self, data: np.ndarray) -> list:
        ''' 预测结果
        - data np.ndarray: 需要预测的数据

        - return list: 返回各个数据的最有可能结果
        '''
        if len(data) == 0:
            return []
        # 转换数据格式
        data = self._convertData(data)
        data = self._convert(data)

        # 识别
        with self.__sess.as_default():
            with self.__graph.as_default():
                logits = self.__model.predict_on_batch(data)

        # 格式化结果
        result = np.argmax(logits, 1)
        del data
        return result

    def _convert(self, data):
        """ 将输入数据转化为0~1之间的浮点数 """
        return (data / 255).astype('float32')

    def _convertData(self, data):
        ''' 用于将单张或多张图片数据转换为可以被当前网络直接使用的数据
        - data: 要转换的数据 类型必须为`list`、`tuple`、`numpy.ndarray`中的一种, 图片数据类型必须为`numpy.ndarray`
        - return: 返回转换后的图片
        '''
        # 判断类型
        if not isinstance(data, (tuple, list, np.ndarray)):
            raise Exception("输入数据类型必须为(tuple|list|np.ndarray), 不能为`{}`".format(type(data)))

        if isinstance(data, np.ndarray):
            if data.shape[1:] == self.input_shape:
                return data
            if data.shape == self.input_shape:
                return data.reshape((-1, *self.input_shape))

            if data.ndim == self.input_dim:
                data = [data]
            else:
                data = list(data)

        if len(data) == 0:
            return np.zeros((0, *self.input_shape))

        # 重置大小
        size = self.input_shape[1::-1]
        result = []
        for img in data:
            if not isinstance(img, np.ndarray):
                raise Exception('数据类型必须为`np.ndarray`')
            if img.ndim != self.input_dim:
                raise Exception('输入数据维数错误')

            if img.shape[1::-1] != size:
                img = cv2.resize(img, size)
            result.append(img.reshape((1, *img.shape)).astype("float32"))
        del img, data
        return np.vstack(result)

    @staticmethod
    def __initAES(key=None):
        from Crypto.Cipher import AES as __AES
        from Crypto.Hash import MD5 as __MD5
        from Crypto.Util import Counter as __Counter

        key = str(key)

        __key = __MD5.new(("sfe model encrypt key={}".format(key)).encode("utf-8")).digest()
        return __AES.new(__key, mode=__AES.MODE_CTR, counter=__Counter.new(32, b"sfepre", b"sfesuf"))

    @classmethod
    def __decrypt(cls, src, dst, key=None):
        with open(src, "rb") as f:
            data = f.read()
        cls.__decryptData(data, dst, key)

    @classmethod
    def __decryptData(cls, data, dst, key=None):
        __aes = cls.__initAES(key)
        data = __aes.decrypt(data)
        with open(dst, "wb") as f:
            f.write(data)

    @classmethod
    def encrypt(cls, src, dst=None, key=None):
        with open(src, "rb") as f:
            data = f.read()
        cls.encryptData(data, dst or src, key)

    @classmethod
    def encryptData(cls, data, dst, key=None):
        __aes = cls.__initAES(key)
        data = __aes.encrypt(data)

        with open(dst, "wb") as f:
            f.write(data)
