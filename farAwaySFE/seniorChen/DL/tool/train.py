# uncompyle6 version 3.2.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.3 (v3.6.3:2c5fed8, Oct  3 2017, 18:11:49) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: .\tools\train.py
# Compiled at: 2018-11-02 11:51:23
# Size of source mod 2**32: 1243 bytes
from importlib import import_module
from SFE.DL.Dataset import Dataset

def main(model_name, data_dir, save_path, epoch, load_path=None):
    """ 训练指定模型
    - model_name str: 要训练的模型名称(SFE.DL中的模块名称)
    - data_dir str: 训练数据所在路径
    - save_path str: 模型保存路径
    - epoch int: 训练轮数
    - load_path str[None]: 是否从指定模型中加载权重, 当路径有效加载
    """
    try:
        model = import_module(('SFE.DL.{}').format(model_name))
        model = getattr(model, model_name)
    except:
        try:
            model = import_module(model_name)
            model = getattr(model, model_name)
        except:
            print('不存在模块名:', model_name)
            exit()

    model = model()
    if load_path:
        if model.load(load_path):
            print('权重加载成功')
        else:
            print('权重加载失败')
        dataset = Dataset(data_dir)
        model.train(dataset, epoch, save_path=save_path)
        del model


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
# okay decompiling tool\train.pyc
