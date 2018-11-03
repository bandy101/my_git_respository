import os
from os import path
import sys

import cv2

try:
    from SFE.DL.Net import Net
except:
    from DL.Net import Net

net = Net()
net.load("smoke.h5")


def getSmokeROI(img, x, y, w, h):
    x2, y2 = x + w, y + h
    width, height = w // 2, h // 2
    img[y:y2, x:x2] = 0

    x, x2 = max(x - width, 0), x2 + width
    y, y2 = max(y - height, 0), y2 + height

    img = img[y:y2, x:x2]
    return img


def roi(img):
    box = cv2.selectROI(f"ROI", img, False, False)
    if box[:2] == (0, 0):
        return None
    print(box)

    return getSmokeROI(img, *box)


def predict(img, box=None) -> int:
    if box is None:
        img = roi(img)
    else:
        img = getSmokeROI(img, *box)

    if img is not None:
        return net.predict(img)[0]
    return -1


def predictImage(img_path, x=None, y=None, w=None, h=None, scale=None):
    box = (x, y, w, h)
    if not any(box):
        box = None

    img = cv2.imread(img_path)
    if scale:
        img = cv2.resize(img, None, fx=scale, fy=scale)
    print(predict(img, box))


def predictFile(img_path):
    img = cv2.imread(img_path)
    print(net.predict(img))


def predictVideo(video_path, scale=None):

    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if scale:
            frame = cv2.resize(frame, None, fx=scale, fy=scale)

        print(predict(frame))


def grabVideo(video_path, scale=None):
    save_dir = path.splitext(video_path)[0]
    if path.isdir(save_dir):
        import shutil
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)

    cap = cv2.VideoCapture(video_path)
    c = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if scale:
            frame = cv2.resize(frame, None, fx=scale, fy=scale)

        img = roi(frame)
        if img is not None:
            print(cv2.imwrite(f"{save_dir}/{c:05}.jpg", img))
            c += 1


def grab(img_path, scale=None):
    for i in os.listdir(img_path):
        img = cv2.imread(path.join(img_path, i))
        if scale:
            frame = cv2.resize(frame, None, fx=scale, fy=scale)
        img = roi(img)
        cv2.imwrite(i, img)


if __name__ == "__main__":
    from fire import Fire
    Fire()
