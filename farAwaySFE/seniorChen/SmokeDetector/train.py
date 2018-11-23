# coding: utf-8
from SFE import DL


def main(model_name: str, data_dir: str, save_path: str, epoch: int):
    ''' 训练指定模型
    model_name str: 要训练的模型名称(SFE.DL中的模块名称)
    data_dir str: 训练数据所在路径
    save_path str: 模型保存路径
    epoch int: 训练轮数
    '''

    if not hasattr(DL, model_name):
        print('不存在模块名:', model_name)
        exit()

    model = getattr(DL, model_name)()
    dataset = DL.Dataset(data_dir)

    model.train(dataset, epoch, save_path=save_path)


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
