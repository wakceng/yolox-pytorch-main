# -*- coding: UTF-8 -*-

#涉及编码的一定要加上面这句话

#----------------------------------------------------#


###此文件用于实现拍一张照片，并将其保存至特定地址



#----------------------------------------------------#



from ast import For
import cv2
import os
import threading, time
from colorama import init, Fore #print的字体颜色修改
# import sys
# sys.path.append(".")
# from cut_jpg import *  # 这样才可以使用文件里面的一些函数
# from PIL import Image

#以下统一修改捕获的内容大小
camera_id  =  0   #电脑用是为1  nano时为0   在99行附近
name_to_use = "wck222" #设置保存的图片的名字
CAPTURE_FRAME_WIDTH = 1920    #宽    默认的    宽 * 高=  640 * 480
CAPTURE_FRAME_HEIGHT = 1080   #高    没有用上 在65行将它屏蔽了
IMAGES_DIR = './capture_now/'  #相对地址 在my_py文件夹下新创建一个文件夹用于存放照片


def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        print(path + ' 目录已创建成功过')
        # del_file(path)
        return False


def del_file(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_file(path_file)


mkdir(IMAGES_DIR)  #创建文件夹


class MyThreadCapture(threading.Thread):
    def __init__(self, capture_source, capture_frame_width, capture_frame_height):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(capture_source)      #打开摄像头
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, capture_frame_width)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_frame_height)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # print(Fore.LIGHTRED_EX+"width",width,)
        # print(Fore.LIGHTRED_EX+"height",height)
        self.img = None
        self.lock = threading.Lock() #只是定义一个锁,并不是给资源加锁,你可以定义多个锁
        #                                     当你需要占用这个资源时，任何一个锁都可以锁这个资源 
        self.stop_cap = False
        # print('用的是camera:' + str(capture_source) + "  "+ str(self.cap.isOpened()))
        # print("电脑时用的是camera 1,nano上应为camera 0,在wck_capture.py文件前面行数上改")

    def is_opened(self):
        return self.cap.isOpened()

    def run(self):  # 当线程获得调度机会时 重构函数会自动执行，相当于摄像头一直在录屏
        ret, frame = self.cap.read()
        while True:
            if self.stop_cap is True:
                print('cap stop !')
                self.cap.release()
                break
            if self.lock.acquire():
                ret, frame = self.cap.read()
                if ret is True:
                    self.img = frame
                self.lock.release()
            time.sleep(0.01)

    def get_img(self):  # 获取帧
        frame = None  # 初始化帧
        while True:
            if self.lock.acquire():  # 得到信号量
                frame = self.img
                self.lock.release()
                break
        return frame

    def lock_acquire(self):
        return self.lock.acquire()

    def lock_release(self):
        self.lock.release()

    def stopp(self):
        self.stop_cap = True


class Capture:
    def __init__(self):
        self.cap = MyThreadCapture(camera_id, CAPTURE_FRAME_WIDTH, CAPTURE_FRAME_HEIGHT)

        if self.cap.is_opened() is False:
            self.cap = MyThreadCapture(0, CAPTURE_FRAME_WIDTH, CAPTURE_FRAME_HEIGHT)

        self.cap.setDaemon(True)    
        self.cap.start() #开启线程

# setDaemon函数说明
# 在启动线程前设置thread.setDaemon(True)，就是设置该线程为守护线程，表示该线程是不重要的,进程退出时不需要等待这个线程执行完成。
# 这样可以避免子线程无限死循环，导致退不出程序，也就是避免传说中的孤儿进程。
# thread.setDaemon（）设置为True, 则主线程执行完毕后会将子线程回收掉;设置为false,主进程执行结束时不会回收子线程,默认False不回收，
# 需要在 start 方法前调用

    # def img_cut(self, img):
    #     img1 = img[CUT_POSITION_1[1]:CUT_POSITION_2[1], CUT_POSITION_1[0]:CUT_POSITION_2[0]]
    #     img2 = img[CUT_POSITION_3[1]:CUT_POSITION_4[1], CUT_POSITION_3[0]:CUT_POSITION_4[0]]
    #     img3 = img[CUT_POSITION_5[1]:CUT_POSITION_6[1], CUT_POSITION_5[0]:CUT_POSITION_6[0]]
    #     return img1, img2, img3

    def capture_goods(self, img_name):
        print(Fore.GREEN+'capture start...')
        time.sleep(0.5)

        img = self.cap.get_img()
        # print(img) #打印的是帧

        img_str = IMAGES_DIR + ("goods_%s.jpg" % str(img_name))
        cv2.imwrite(img_str, img)
        print(Fore.GREEN+'capture ok!'+'the photo have been saved!')

    def cap_stop(self):
        self.cap.stopp()





if __name__ == '__main__':
    init(autoreset=True)#每次print完 自动变成默认颜色
    # def cap_shot():
    capture = Capture()
    while_flag_temp = 1
    time.sleep(0.5)         # 设置这个时间的目的是为了不出错，否则拍不出照片
    try:
        while while_flag_temp:
            # img_name=input('input image name\n')
            img_name = name_to_use
            capture.capture_goods(img_name)

            # capture.capture_goods("001")
            print(Fore.LIGHTGREEN_EX+'successful!')
            while_flag_temp = 0
            break

            # for i in range(1,5):

            #     #img_name = input('input image name\n')
            #     capture.capture_goods(i)
            #     print('cap ok !')
            #   #  time.sleep(1)

    except:
        capture.cap_stop()
        print('error：照片拍摄失败')

    #cv2.destroyAllWindows()#可以不用这个函数关闭窗口（因为根本没有打开）

    # img = Image.open("/home/pi/raspberry/capture/images/goods_1223.jpg")
    # cut_picture(img)

# cap_shot()
