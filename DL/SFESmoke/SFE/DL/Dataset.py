# coding: utf-8
import os
from os import path

import numpy as np
import cv2


class Dataset():
    '''
    将指定目录中的数据加载到数据集中 目录结构需要满足以下条件:

    - 图片分类放在文件夹中 同个文件夹中的图片即为同一类图片

    - 所有图片应该应该为同一的大小
    '''

    def __init__(self, data_path, is_gray=False):
        '''
        - data_path str: 要加载数据路径
        - is_gray bool[False]: 是否以灰度图方式读取数据
        '''
        # 获取类别
        categories = [i for i in os.listdir(data_path) if path.isdir(path.join(data_path, i))]
        categories.sort()
        self.__categories = dict(enumerate(categories))
        self.__categories.update(dict(zip(self.__categories.values(), self.__categories.keys())))

        is_gray = cv2.IMREAD_GRAYSCALE if is_gray else cv2.IMREAD_COLOR

        # 加载图片数据
        self.__labels = []
        self.__data = []
        self.__category_count = len(categories)
        for c in categories:
            d = path.join(data_path, c)
            for f in os.listdir(d):
                f = path.join(d, f)
                img = cv2.imread(f, is_gray)
                if img is not None:
                    self.__data.append(img)
                    self.__labels.append(self.categories[c])
        self.__labels = np.array(self.__labels)
        self.__data = np.array(self.data)

        if is_gray == cv2.IMREAD_GRAYSCALE:
            self.__data = self.__data.reshape((*self.__data.shape, 1))

    def getBatchIteration(self, batch_size=1, shuffle=True):
        ''' 返回一个迭代器 每次迭代最多返回`batch_size`个数据
        - batch_size int[1]: 每次迭代最多返回的数据数
        - shuffle bool[True]: 迭代前是否进行随机洗牌
        '''
        items = np.arange(self.size)
        if shuffle:
            np.random.shuffle(items)

        s_idx = 0
        e_idx = batch_size
        while s_idx < self.size:
            idx = items[s_idx:e_idx]
            yield self.labels[idx], self.data[idx]
            s_idx, e_idx = e_idx, e_idx + batch_size

    @property
    def data(self):
        ''' 数据集中的所有数据 '''
        return self.__data

    @property
    def labels(self):
        ''' 数据集中的所有标签 '''
        return self.__labels

    @property
    def categories(self):
        ''' 数据集中的分类 '''
        return self.__categories

    @property
    def category_count(self):
        ''' 分类数 '''
        return self.__category_count

    @property
    def size(self):
        ''' 数据集的数据个数 '''
        return len(self.__labels)
