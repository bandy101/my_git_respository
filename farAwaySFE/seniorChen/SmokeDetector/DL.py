# coding: utf-8
import cv2
import os
from os import path
import argparse
import sys
from datetime import datetime

from SFE.DL import Net, Dataset


def __log(message, fw, newline=False):
    l = "\n" if newline else "\r"
    print(l + message, end="")
    fw.write(message + "\n")


def __test(model_path, image_path):
    ''' 测试模型 网络模型为 SFE.DL.Net
    model_path str: 模型所在路径
    image_path str: 测试图片所在路径
    '''
    assert path.exists(model_path), "目标模型不存在"
    model = Net()
    model.load(model_path)

    classes = {'yes': 1, 'other': 0, 0: 'other', 1: 'yes'}

    TP, FP, FN, TN, succ = 0, 0, 0, 0, 0
    total = 0

    fn = f"./{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    fw = open(fn, "w")

    # 遍历目录
    for cp, ds, fs in os.walk(image_path):
        name = path.basename(cp)
        for f in fs:
            f = path.join(cp, f)
            # 加载图片
            img = cv2.imread(f)
            if img is None:
                continue
            else:
                img = cv2.resize(img, (128, 128))
            total += 1
            # 获取最大值的标签值
            label = model.predict(img) or [0]
            label = int(label[0])

            __log("{} is {}".format(f, classes[label]), fw)
            if label == classes[name]:
                succ += 1
                if name == "yes":
                    TP += 1
                else:
                    TN += 1
            else:
                if name == "yes":
                    FN += 1
                else:
                    FP += 1

    __log("\n正确率：{:.2%}".format(succ / total), fw, True)
    __log("TP:{} FP:{} FN:{} TN:{}".format(TP, FP, FN, TN), fw, True)
    __log("P:{:.2%}".format(TP / (TP + FP)), fw, True)
    __log("S:{:.2%}".format(TP / (TP + FN)), fw, True)
    __log("DSC:{:.2%}".format((2 * TP / (2 * TP + FP + FN))), fw, True)
    __log("", fw, True)
    print(f"输出文件已保存到 {fn}")

    fw.close()


def __train(model_path, image_path, time, load_model=False):
    ''' 训练模型 网络模型为 SFE.DL.Net
    model_path str: 模型保存路径
    image_path str: 数据集路径
    time int: 训练轮数
    load_model bool[False]: 是否加载模型权重
    '''

    assert time > 0, "次数应大于0"

    dataset = Dataset(image_path)
    print(dataset.categories)
    net = Net()
    if load_model and path.isfile(model_path):
        net.load(model_path)
    net.train(dataset, time, save_path=model_path)

    print(f"model save in {model_path}")


if __name__ == "__main__":
    from fire import Fire

    Fire({
        'train': __train,
        'test': __test,
    })
