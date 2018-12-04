from SFE import loadModule
from SFE.DL.Dataset import Dataset


def main(model_name: str, data_dir: str, save_path: str, epoch: int, load_path: str=None):
    ''' 训练指定模型
    - model_name str: 要训练的模型名称(SFE.DL中的模块名称)
    - data_dir str: 训练数据所在路径
    - save_path str: 模型保存路径
    - epoch int: 训练轮数
    - load_path str[None]: 是否从指定模型中加载权重, 当路径有效加载
    '''
    model = None
    for n in [model_name, "SFE.DL.{}".format(model_name)]:
        model = loadModule(n)
        if n is not None:
            break
    else:
        raise ModuleNotFoundError(model_name)

    if "." in model_name:
        model_name = model_name.split(".")[-1]
    model = getattr(model, model_name)

    model = model()
    if load_path:
        if model.load(load_path):
            print("权重加载成功")
        else:
            print("权重加载失败")
    dataset = Dataset(data_dir)
    model.train(dataset, epoch, save_path=save_path)

    del model


if __name__ == '__main__':
    from fire import Fire
    Fire(main)
