import numpy as np

from SFE import loadModule
from SFE.DL.Dataset import Dataset


def main(model_name: str, model_path: str, test_dir: str):
    ''' 测试指定模型
    - model_name str: 要训练的模型名称(SFE.DL中的模块名称)
    - model_path str: 模型文件路径
    - test_dir str: 测试集路径
    '''
    module = None
    for n in [model_name, "SFE.DL.{}".format(model_name)]:
        module = loadModule(n)
        if module is not None:
            break
    else:
        raise ModuleNotFoundError(model_name)

    if "." in model_name:
        model_name = model_name.split(".")[-1]
    model = getattr(module, model_name)

    model = model()
    assert model.load(model_path), "模型加载失败"

    dataset = Dataset(test_dir)
    result = model.predict(dataset.data)
    t = (dataset.labels == result).sum()
    print("测试集大小：{}, 正确识别数: {}, 识别率: {:.2%}".format(dataset.size, t, t / dataset.size))
    for i in range(dataset.category_count):
        print("-"*50)
        print(dataset.categories[i])
        # 识别率
        print("总数:", (dataset.labels == i).sum(), end=", ")
        print("正确识别数:", (result[dataset.labels == i] == i).sum(), end=", ")
        # 误检
        print("误检:", (result[dataset.labels != i] == i).sum(), end=", ")
        # 漏检
        print("漏检:", (result[dataset.labels == i] != i).sum())
    del model


if __name__ == "__main__":
    from fire import Fire
    Fire(main)
