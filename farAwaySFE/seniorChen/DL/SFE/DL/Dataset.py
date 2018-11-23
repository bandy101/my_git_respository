# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\SFE\DL\Dataset.py
# Compiled at: 2018-11-02 11:51:19
# Size of source mod 2**32: 2708 bytes
import os
from os import path
import numpy as np, cv2

class Dataset:
    """
    ��ָ��Ŀ¼�е����ݼ��ص����ݼ��� Ŀ¼�ṹ��Ҫ������������:
    
    - ͼƬ��������ļ����� ͬ���ļ����е�ͼƬ��Ϊͬһ��ͼƬ
    
    - ����ͼƬӦ��Ӧ��Ϊͬһ�Ĵ�С
    """

    def __init__(self, data_path, is_gray=False):
        """
        - data_path str: Ҫ��������·��
        - is_gray bool[False]: �Ƿ��ԻҶ�ͼ��ʽ��ȡ����
        """
        categories = [i for i in os.listdir(data_path) if path.isdir(path.join(data_path, i))]
        categories.sort()
        self._Dataset__categories = dict(enumerate(categories))
        self._Dataset__categories.update(dict(zip(self._Dataset__categories.values(), self._Dataset__categories.keys())))
        is_gray = cv2.IMREAD_GRAYSCALE if is_gray else cv2.IMREAD_COLOR
        self._Dataset__labels = []
        self._Dataset__data = []
        self._Dataset__category_count = len(categories)
        for c in categories:
            d = path.join(data_path, c)
            for f in os.listdir(d):
                f = path.join(d, f)
                img = cv2.imread(f, is_gray)
                if img is not None:
                    self._Dataset__data.append(img)
                    self._Dataset__labels.append(self.categories[c])

        self._Dataset__labels = np.array(self._Dataset__labels)
        self._Dataset__data = np.array(self.data)
        if is_gray == cv2.IMREAD_GRAYSCALE:
            self._Dataset__data = self._Dataset__data.reshape((*self._Dataset__data.shape, *(1, )))

    def getBatchIteration(self, batch_size=1, shuffle=True):
        """ ����һ�������� ÿ�ε�����෵��`batch_size`������
        - batch_size int[1]: ÿ�ε�����෵�ص�������
        - shuffle bool[True]: ����ǰ�Ƿ�������ϴ��
        """
        items = np.arange(self.size)
        if shuffle:
            np.random.shuffle(items)
        s_idx = 0
        e_idx = batch_size
        while s_idx < self.size:
            idx = items[s_idx:e_idx]
            yield (self.labels[idx], self.data[idx])
            s_idx, e_idx = e_idx, e_idx + batch_size

    @property
    def data(self):
        """ ���ݼ��е��������� """
        return self._Dataset__data

    @property
    def labels(self):
        """ ���ݼ��е����б�ǩ """
        return self._Dataset__labels

    @property
    def categories(self):
        """ ���ݼ��еķ��� """
        return self._Dataset__categories

    @property
    def category_count(self):
        """ ������ """
        return self._Dataset__category_count

    @property
    def size(self):
        """ ���ݼ������ݸ��� """
        return len(self._Dataset__labels)
# okay decompiling SFE\DL\Dataset.pyc
