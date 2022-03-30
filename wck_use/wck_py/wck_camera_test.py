import cv2 

#----------------------------------------------------#

#此文件用于测试摄像头能否使用

#----------------------------------------------------#

# 打开摄像头获取图片
def video_demo():
    # 打开摄像头，0代表的是设备id
    # 如果有多个摄像头，可以设置其他数值
    # VideoCapture打开摄像头
    capture = cv2.VideoCapture(0)


    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("width",width,)
    print("height",height)
    # capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
    while True:
        # # 读取摄像头,它能返回两个参数，第一个参数是bool型的ret,代表有没有读到图片；
        # 第二个参数是frame，是当前截取一帧的图片
        ret,frame = capture.read() #
        #  翻转 0:上下颠倒 大于0水平颠倒   小于180旋转
        # frame = cv.flip(frame,0) # 摄像头反置,拍出的样子是正的
        # frame = cv.flip(frame, 1)
        cv2.imshow("video",frame)
        # 键盘输入q退出窗口，
        # 不按q点击关闭会一直关不掉 也可以设置成其他键。
        
        ch = cv2.waitKey(1)####1表示delay1ms
        if ch == 27 or ch == ord("q") or ch == ord("Q"):#q时退出
            break

if __name__ == "__main__":
    video_demo()

    # image = cv2.imread("D:/yolox-pytorch-main/wck_use/wck_py/capture_now/goods_object_t_1.jpg")
    # sp = image.shape
    # print(sp)

    
    cv2.destroyAllWindows()  #如果之前没有释放掉内存的操作的话destroyallWIndows会释放掉被那个变量占用的内存