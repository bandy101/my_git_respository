import cv2
import queue,shutil
import os,time
from os import path

from DL import VehicleModel
from DL import Dataset
# 1080 1920 3 25

matsQ = queue.Queue(maxsize=1024)
from threading import Thread
from select_search import selectRect


fourcc = cv2.VideoWriter_fourcc(*'MP42')
videoWriter = cv2.VideoWriter('saveVideosS.avi',fourcc,25,(1920,1080))
iswrite =True

def saveVideo():
    global iswrite
    print('线程处理中···')
    while True:
        if not matsQ.empty():
            q = matsQ.get()
            try:
                videoWriter.write(q)
            except:
                print('队列写入错误!')
                break

saveVideoT =Thread(target=saveVideo)
saveVideoT.setDaemon(True)
def main():
    global iswrite
    saveVideoT.start()
    _srcs = 'testvideo/4096_2160'
    videos = [path.join(_srcs,_) for _ in os.listdir(_srcs)]
    for _ in videos:
        vc = cv2.VideoCapture(_)
        print(_,vc.get(7))
        rval=vc.isOpened()
        index = 0
        while rval:
            rval, frame = vc.read()
            if rval:
                frame = cv2.resize(frame,(1920,1080))
                matsQ.put(frame)
                if matsQ.full():
                    print('队列加载满',index)
                    while matsQ.full():
                        time.sleep(0.05)
                    index +=1
    while not matsQ.empty():
        continue
    print('end')
    # saveVideoT.join()
    videoWriter.release()


def GMM():
    cam = cv2.VideoCapture('video/qd_04.mp4')
    print(cam.get(3),cam.get(4))
    width, height= cam.get(3), cam.get(4)
    _height = 600
    _width =int(width*_height/height)
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
    ret = cam.isOpened()
    while ret:
        ret, frame = cam.read()
        if ret:
            frame = cv2.resize(frame,(_width,_height))
            _mat,_mats = frame.copy(),frame.copy()
            fgmask = fgbg.apply(frame)
            fgmask = cv2.threshold(fgmask, 244, 255, cv2.THRESH_BINARY)[1]
            # 通过腐蚀和膨胀过滤一些噪声
            erode = cv2.erode(fgmask, (21, 21), iterations=1)
            dilate = cv2.dilate(fgmask, (21, 21), iterations=1)
            (cnts,_) = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            ims_ = []
            for c in cnts:
                c_area = cv2.contourArea(c)
                if c_area < 12000 or c_area >160000:  # 过滤太小或太大的运动物体，这类误检概率比较高
                    continue
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(_mat, (x, y), (x+w, y+h), (0, 0, 255), 2)
                _im = _mat[y:y+h,x:x+w]
                _rects = selectRect(_im,400,1600)
                for _rect in _rects:
                    x1,y1,x2,y2 = _rect
                    if model_car(frame[y1:y2,x1:x2]):
                        cv2.rectangle(_mat, (x+x1, y1+y), (x2+x, y2+y), (0, 255, 0), 2)
                # ims_.append(frame[y:y+h,x:x+w])
            # for _im in ims_:
            #     _rects = selectRect(_im,100,1600)
            #     for _rect in _rects:
            #         x1,y1,x2,y2 = _rect
            #         # if model_car(frame[y1:y2,x1:x2]):
            #         cv2.rectangle(_mat, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # cv2.rectangle(_mat, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.imshow('out',_mat)
            if cv2.waitKey() == ord('q'):
                break
    cv2.destroyAllWindows()

# 视频
def classfy(srcP: str):
    videos = [path.join(p,_) for p,d,f in os.walk(srcP) for _ in f if _[-3:].lower() in ['mp4','avi']]
    for _ in videos:
        vc = cv2.VideoCapture(_)
        if vc.isOpened():
            _temp = path.join(srcP,f'{str(int(vc.get(3)))}_{str(int(vc.get(4)))}')
            os.makedirs(_temp,exist_ok=True)
            shutil.copy(_,path.join(_temp,path.basename(_)))
            vc.release()


def detect():
    # face_casade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #使用脸部检测
    # eye_casade=cv2.CascadeClassifier("haarcascade_eye.xml")
    # camera=cv2.VideoCapture(0)  #0代表调用默认摄像头，1代表调用外接摄像头
    car_casade = cv2.CascadeClassifier()
    if not car_casade.load(r"C:\Users\NHT\Desktop\car\data\cascade.xml"):
        print('加载错误！')
        return
    camera = cv2.VideoCapture('videos/qy_08.mp4')
    width,height= camera.get(3),camera.get(4)
    while (True):
        ret,frame=camera.read()
        frame = cv2.resize(frame,(int(width*350/height),350))
        if ret:
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            # gray= cv2.resize(gray,(80,60))
            faces=car_casade.detectMultiScale(gray,1.5,4)
            # print('start')
            for (x,y,w,h) in faces:
                print(x,y,w,h)
                # img=cv2.rectangle(frame,(x*10,y*10),((x+w)*10,(y+h)*10),(255,0,0),2)
                img=cv2.rectangle(frame,(x,y),((x+w),(y+h)),(255,0,0),2)
                
            cv2.imshow("camera",frame)
            key=cv2.waitKey(30)&0xff
            if key==27:
                sys.exit()
        else:
            print('error')
            break
carModel = VehicleModel.VehicleModel()
carModel.load('DL/vehicle.h5')
def model_car(im):
    height = 40
    width = im.shape[1]*height/im.shape[0]
    im = cv2.resize(im,(int(width),int(height)))
    # print('车辆识别···')
    result,r = carModel.predict(im)
    if result==0 and r:
        return False
    # else:
    #     return True
    print(r)
    return bool(r)
if __name__ == '__main__':
    # main()
    detect()
    # detect()
    # model_car()
    # classfy(input('SRCpath:'))
    # qd_04