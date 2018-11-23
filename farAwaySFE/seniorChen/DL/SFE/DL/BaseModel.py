# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\DL\BaseModel.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 9742 bytes
import os
from os import path
import stat
from tempfile import mkstemp
import cv2, numpy as np, tensorflow as tf
from keras.models import Model
from keras.optimizers import Adam
from keras.losses import categorical_crossentropy
from keras.metrics import categorical_accuracy
from keras.utils import to_categorical

class BaseModelMetaclass(type):

    def __init__(self, name, bases, attrs):
        key = '_getitem'
        if key in attrs:
            self._BaseModelMetaclass__getitem = attrs[key]
        else:

            def getitem(x):
                raise KeyError()

            self._BaseModelMetaclass__getitem = getitem

    def __getitem__(self, key):
        return self._BaseModelMetaclass__getitem(key)


class BaseModel(metaclass=BaseModelMetaclass):
    """ ### ������ģ�ͻ���
    ����಻�ܵ���ʵ���� ����ʵ����ʱ��**�׳��쳣** �������ʵ����������/����:
    
    - ```
    @property
    def category_count() -> int # �������ӵ��������� ������Է������ģ�͵ķ�������
    ```
    
    - ```
    @property
    def input_shape() -> tuple # �������ӵ��������� ������Է������ģ���������ݵ�shape, ���ظ�ʽΪ (�߶�, ���, ͨ����)
    ```
    
    - ```
    def _build_model() -> keras.models.Model # �������ʵ��������� �����������һ��`keras`ģ��
    ```
    
    ����ʵ�����з�����һ���� ����ʵ���༶��`__getitem__`(��ѡ):
    
    - ```
    @classmethod
    def _getitem(cls, key) -> any
    ```
    
    - ```
    @staticmethod
    def _getitem(key) -> any
    ```
    """
    _BaseModel__DEFAULT_KEY = 'gd - sfe'

    @property
    def category_count(self):
        """ �������ӵ��������� ������Է������ģ�͵ķ������� """
        raise NotImplementedError()

    @property
    def input_shape(self):
        """ �������ӵ��������� ������Է������ģ���������ݵ�shape """
        raise NotImplementedError()

    def _build_model(self):
        """ �������ʵ��������� �����������һ��`keras`ģ�� """
        raise NotImplementedError()

    @property
    def input_dim(self):
        """ �����������ݵ�ά�� """
        return len(self.input_shape)

    def __init__(self, sess=None):
        """ - sess tf.Session[None]: ������ʹ�õ�`tf.Session` Ϊ`None`ʱ���Զ����� """
        if isinstance(sess, tf.Session):
            self._BaseModel__self_sess = False
            self._BaseModel__sess = sess
        else:
            self._BaseModel__self_sess = True
            config = tf.ConfigProto()
            config.gpu_options.allow_growth = True
            self._BaseModel__sess = tf.Session(config=config)
        with self._BaseModel__sess.as_default():
            self._BaseModel__model = self._build_model()
            self._BaseModel__graph = tf.get_default_graph()

    def __del__(self):
        if self._BaseModel__self_sess:
            self._BaseModel__sess.close()

    def load(self, model_path, key=None):
        """ ����Ȩ��
        - model_path str/bytes: Ҫ���ص�ģ��Ȩ���ļ���·����ģ���ļ�����
        - key str[None]: ��Կ, Ϊ`None`ʱ��ʾʹ��Ĭ����Կ����
        
        - return bool: ���ؼ����Ƿ�ɹ�
        """
        if key is None:
            key = self._BaseModel__DEFAULT_KEY
        try:
            if not isinstance(model_path, (str, bytes)):
                raise AssertionError('ģ��·�����ͱ���Ϊ`str/bytes`')
            if isinstance(model_path, str):
                if not path.isfile(model_path):
                    raise AssertionError('ģ��·��������')
                fd, fp = mkstemp()
                os.chmod(fp, 448)
                if isinstance(model_path, bytes):
                    self._BaseModel__decryptData(model_path, fd, key)
                else:
                    self._BaseModel__decrypt(model_path, fd, key)
                model_path = fp
            with self._BaseModel__sess.as_default():
                with self._BaseModel__graph.as_default():
                    self._BaseModel__model.load_weights(model_path)
                    try:
                        os.remove(fp)
                    except:
                        pass

                    return True
        except:
            import traceback
            traceback.print_exc()
            return False

    def save(self, save_path, key=None):
        """ ����Ȩ��
        - save_path str: Ȩ�ر���·��
        - key str[None]: ��Կ, Ϊ`None`ʱ��ʾʹ��Ĭ����Կ����
        
        - reutrn bool: ���ر����Ƿ�ɹ�
        """
        try:
            if not isinstance(save_path, str):
                raise AssertionError('ģ��·�����ͱ���Ϊ`str`')
            if key is None:
                key = self._BaseModel__DEFAULT_KEY
            with self._BaseModel__sess.as_default():
                with self._BaseModel__graph.as_default():
                    self._BaseModel__model.save_weights(save_path)
                    self.encrypt(save_path, key=key)
                    return True
        except:
            import traceback  #定位出错的行
            traceback.print_exc()
            return False

    def train(self, dataset, epochs, batch_size=32, save_path=None, key=None):
        """ ѵ��ģ��
        - dataset SFE.DL.Dataset: ���ݼ�, ���ͱ���Ϊ`SFE.DL.Dataset`
        - epochs int: ѵ������
        - batch_size int[32]: ÿ��ͼƬ�Ĵ�С
        - save_path str[None]: ѵ����ɺ�ģ�͵ı���·��, Ϊ`None`ʱ������
        - key str[None]: ��Կ, Ϊ`None`ʱ��ʾʹ��Ĭ����Կ����
        """
        from .Dataset import Dataset
        if not isinstance(dataset, Dataset):
            return
        optimizer = Adam()
        self._BaseModel__model.compile(optimizer=optimizer, loss=categorical_crossentropy, metrics=[categorical_accuracy])
        data = dataset.data
        data = self._convert(data)
        label = dataset.labels
        label = to_categorical(label, self.category_count)
        with self._BaseModel__sess.as_default():
            with self._BaseModel__graph.as_default():
                self._BaseModel__model.fit(x=data,
                  y=label,
                  batch_size=batch_size,
                  epochs=epochs)
        if save_path:
            self.save(save_path, key)

    def predict(self, data):
        """ Ԥ����
        - data np.ndarray: ��ҪԤ�������
        
        - return list: ���ظ������ݵ����п��ܽ��
        """
        if len(data) == 0:
            return []
        else:
            data = self._convertData(data)
            data = self._convert(data)
            with self._BaseModel__sess.as_default():
                with self._BaseModel__graph.as_default():
                    logits = self._BaseModel__model.predict_on_batch(data)
            result = np.argmax(logits, 1)
            del data
            return result

    def _convert(self, data):
        """ ����������ת��Ϊ0~1֮��ĸ����� """
        return (data / 255).astype('float32')

    def _convertData(self, data):
        """ ���ڽ����Ż����ͼƬ����ת��Ϊ���Ա���ǰ����ֱ��ʹ�õ�����
        - data: Ҫת�������� ���ͱ���Ϊ`list`��`tuple`��`numpy.ndarray`�е�һ��, ͼƬ�������ͱ���Ϊ`numpy.ndarray`
        - return: ����ת�����ͼƬ
        """
        if not isinstance(data, (tuple, list, np.ndarray)):
            raise AssertionError(('�����������ͱ���Ϊ(tuple|list|np.ndarray), ����Ϊ`{}`').format(type(data)))
        if isinstance(data, np.ndarray):
            pass
        if data.shape[1:] == self.input_shape:
            return data
        elif data.shape == self.input_shape:
            return data.reshape((*(-1, ), *self.input_shape))
        else:
            if data.ndim == self.input_dim:
                data = [
                 data]
            else:
                data = list(data)
            if len(data) == 0:
                return np.zeros((*(0, ), *self.input_shape))
            size = self.input_shape[1::-1]
            result = []
            for img in data:
                if not isinstance(img, np.ndarray):
                    raise AssertionError('�������ͱ���Ϊ`np.ndarray`')
                if not img.ndim == self.input_dim:
                    raise AssertionError('��������ά������')
                if img.shape[1::-1] != size:
                    img = cv2.resize(img, size)
                result.append(img.reshape((*(1, ), *img.shape)).astype('float32'))

            del img
            del data
            return np.vstack(result)

    @staticmethod
    def __initAES(key=None):
        from Crypto.Cipher import AES as _BaseModel__AES
        from Crypto.Hash import MD5 as _BaseModel__MD5
        from Crypto.Util import Counter as _BaseModel__Counter
        key = str(key)
        _BaseModel__key = _BaseModel__MD5.new(('sfe model encrypt key={}').format(key).encode('utf-8')).digest()
        return _BaseModel__AES.new(_BaseModel__key, mode=_BaseModel__AES.MODE_CTR, counter=_BaseModel__Counter.new(32, b'sfepre', b'sfesuf'))

    @classmethod
    def __decrypt(cls, src, dst, key=None):
        with open(src, 'rb') as (f):
            data = f.read()
        cls._BaseModel__decryptData(data, dst, key)

    @classmethod
    def __decryptData(cls, data, dst, key=None):
        _BaseModel__aes = cls._BaseModel__initAES(key)
        data = _BaseModel__aes.decrypt(data)
        with open(dst, 'wb') as (f):
            f.write(data)

    @classmethod
    def encrypt(cls, src, dst=None, key=None):
        with open(src, 'rb') as (f):
            data = f.read()
        cls.encryptData(data, dst or src, key)

    @classmethod
    def encryptData(cls, data, dst, key=None):
        _BaseModel__aes = cls._BaseModel__initAES(key)
        data = _BaseModel__aes.encrypt(data)
        with open(dst, 'wb') as (f):
            f.write(data)
# okay decompiling SFE\DL\BaseModel.pyc
