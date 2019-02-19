import cv2
from skimage.feature import local_binary_pattern


def main():
    im = cv2.imread('../mine/0.jpg',0) # 灰度
    lbp = local_binary_pattern(im,8,1)

    cv2.imshow('src',im)
    # cv2.imshow('lbp',lbp)
    print(lbp)

    print(im)
    return lbp
if __name__ == "__main__":
    main()