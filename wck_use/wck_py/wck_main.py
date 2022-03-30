from email.parser import BytesParser
from re import A
import serial
import time
from colorama import init, Fore #print的字体颜色修改
from wck_recognize import Recognize
from yolo import YOLO

PORT_CAR = "COM3"
PORT_ARM = "COM9"
baud_rate = 115200
#------------------------------------------------#
#                   car命令  
car_start_CODE = "S"      # 底盘 出门左拐 前进两格
car_goone_CODE = "C1"     # 底盘 前进一格
car_R_1_4_CODE = "R14"    # 底盘 右转 前进四格

car_finished_CODE = "D\n" # 底盘 完成 后发D过来
#------------------------------------------------#

#------------------------------------------------#
#                   arm命令  
arm_up_lef = "in01"       # 机械臂 抓 上左
arm_up_mid = "in02"       # 机械臂 抓 上中
arm_up_rig = "in03"       # 机械臂 抓 上右
arm_down_lef = "in11"     # 机械臂 抓 下左
arm_down_mid = "in12"     # 机械臂 抓 下中
arm_down_rig = "in13"     # 机械臂 抓 下右
arm_stop = "in00"

arm_finished_CODE = "K\n" # 机械臂 完成 后发K过来
#------------------------------------------------#

#-----------------------------------------#
#
#  和底盘交流  底盘发的信息一定是  \n  结尾
#
#-----------------------------------------#
class Car_Chat:
    def __init__(self):
        self.ser_car = serial.Serial(PORT_CAR,baud_rate)


    def car_start(self):   ## nano发送 出门 命令 需要收到
        self.ser_car.write(car_start_CODE.encode())
        while True:
           data_c = self.ser_car.readline().decode("utf-8")
           if data_c == car_finished_CODE :
               print("car stop")
               break
        # print("车车指令已完成")
        # return True
           

    def car_goone(self):   ## nano发送 前进 命令 需要收到
        self.ser_car.write(car_goone_CODE.encode())
        while True:
           data_c = self.ser_car.readline().decode("utf-8")
           if data_c == car_finished_CODE :
               break
        # print("车车指令已完成")
        # return True

    def car_turngo(self):
        self.ser_car.write(car_R_1_4_CODE.encode())
        while True:
           data_c = self.ser_car.readline().decode("utf-8")
           if data_c == car_finished_CODE :
               break
        # print("车车指令已完成")
        # return True


#-----------------------------------------#
#
#  和机械臂交流  机械臂发的信息一定是  \n  结尾
#
#-----------------------------------------#
class Arm_Chat:
    def __init__(self):
        self.ser_arm = serial.Serial(PORT_ARM,baud_rate)



    def arm_catch_up_lef(self):      # 机械臂 抓 上左
        self.ser_arm.write(arm_up_lef.encode())
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口01" + data_a)
           if data_a == arm_finished_CODE :
               break

    def arm_catch_up_mid(self):      # 机械臂 抓 上中
        self.ser_arm.write(arm_up_mid.encode())
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口02" + data_a)
           if data_a == arm_finished_CODE :
               break

    def arm_catch_up_rig(self):      # 机械臂 抓 上右
        self.ser_arm.write(arm_up_rig.encode())
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口03" + data_a)
           if data_a == arm_finished_CODE :
               break

    def arm_catch_down_lef(self):      # 机械臂 抓 下左
        self.ser_arm.write(arm_down_lef.encode())
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口11" + data_a)
           if data_a == arm_finished_CODE :
               break

    def arm_catch_down_mid(self):      # 机械臂 抓 下中
        self.ser_arm.write(arm_down_mid.encode())
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口12" + data_a)
           if data_a == arm_finished_CODE :
               break

    def arm_catch_down_rig(self):      # 机械臂 抓 下右
        self.ser_arm.write(arm_down_rig.encode())
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口13" + data_a)
           if data_a == arm_finished_CODE :
               break

    def arm_stop_cam_catch(self):      # 机械臂 停下拍照
        self.ser_arm.write(arm_stop.encode())
        # print("已发送in00")
        while True:
           data_a = self.ser_arm.readline().decode("utf-8")
           # print("arm串口" + data_a)
           if data_a == arm_finished_CODE :
               # print(data_a)
               break

#-----------------------------------------#
#
#         无机械臂，单底盘跑完外圈
#
#-----------------------------------------#
def run_a_circle():
    time.sleep(2)
    init(autoreset=True)#每次print完 自动变成默认颜色

    car_chat = Car_Chat()

    car_chat.car_start()
    time.sleep(2)

    Stage = "A"  #正在A货架
    for i in range(5):
        car_chat.car_goone()
        time.sleep(2)

    car_chat.car_turngo()
    time.sleep(2)
    Stage = "B"  #正在B货架
    for i in range(5):
        car_chat.car_goone()
        time.sleep(2)

    car_chat.car_turngo()
    time.sleep(2)
    Stage = "C"  #正在C货架
    for i in range(5):
        car_chat.car_goone()
        time.sleep(2)

    car_chat.car_turngo()
    time.sleep(2)
    Stage = "D"  #正在D货架
    for i in range(5):
        car_chat.car_goone()
        time.sleep(2)

#-----------------------------------------#
#
#            主函数，识别+跑外圈
#
#-----------------------------------------#
def recognize_run_circle(car_chat,arm_chat,yolo):
    time.sleep(2)
    init(autoreset=True)#每次print完 自动变成默认颜色
    rec = Recognize()
    # car_chat = Car_Chat()
    # arm_chat = Arm_Chat()
    
    car_chat.car_start()  # 结束后已经到达第一个要检测的点
    print("s 已发送")
    stage_now = "D"           # 处于货架A
    print("stage_now:",stage_now)
    arm_chat.arm_stop_cam_catch()
    # print("11")
    result_needed_location = rec.recognize_for_running(stage_now,yolo)
    for i in range(len(result_needed_location)):
        switch_arm(arm_chat,result_needed_location[i])
    for i_5_times in range(5):
        car_chat.car_goone()
        # time.sleep(2)
        arm_chat.arm_stop_cam_catch()
        result_needed_location = rec.recognize_for_running(stage_now,yolo)
        for ii in range(len(result_needed_location)):
            switch_arm(arm_chat,result_needed_location[ii])
    
    car_chat.car_turngo() # 结束后到达货架B的第一个监测点
    stage_now = "C"
    print("stage_now:", stage_now)
    arm_chat.arm_stop_cam_catch()
    result_needed_location = rec.recognize_for_running(stage_now,yolo)
    for i in range(len(result_needed_location)):
        switch_arm(arm_chat,result_needed_location[i])
    for i_5_times in range(5):
        car_chat.car_goone()
        # time.sleep(2)
        arm_chat.arm_stop_cam_catch()
        result_needed_location = rec.recognize_for_running(stage_now,yolo)
        for ii in range(len(result_needed_location)):
            switch_arm(arm_chat,result_needed_location[ii])

    car_chat.car_turngo() # 结束后到达货架C的第一个监测点
    stage_now = "B"
    print("stage_now:", stage_now)
    result_needed_location = rec.recognize_for_running(stage_now,yolo)
    for i in range(len(result_needed_location)):
        switch_arm(arm_chat,result_needed_location[i])
    for i_5_times in range(5):
        car_chat.car_goone()
        # time.sleep(2)
        arm_chat.arm_stop_cam_catch()
        result_needed_location = rec.recognize_for_running(stage_now,yolo)
        for ii in range(len(result_needed_location)):
            switch_arm(arm_chat,result_needed_location[ii])

    car_chat.car_turngo() # 结束后到达货架D的第一个监测点
    stage_now = "A"
    print("stage_now:", stage_now)
    arm_chat.arm_stop_cam_catch()
    result_needed_location = rec.recognize_for_running(stage_now,yolo)
    for i in range(len(result_needed_location)):
        switch_arm(arm_chat,result_needed_location[i])
    for i_5_times in range(5):
        car_chat.car_goone()
        # time.sleep(2)
        arm_chat.arm_stop_cam_catch()
        result_needed_location = rec.recognize_for_running(stage_now,yolo)
        for ii in range(len(result_needed_location)):
            switch_arm(arm_chat,result_needed_location[ii])


def switch_arm(arm_chat,n_lo):
    if n_lo == 1:
        arm_chat.arm_catch_up_lef()
    elif n_lo == 2:
        arm_chat.arm_catch_up_mid()
    elif n_lo == 3:
        arm_chat.arm_catch_up_rig()
    elif n_lo == 11:
        arm_chat.arm_catch_down_lef()
    elif n_lo == 12:
        arm_chat.arm_catch_down_mid()
    elif n_lo == 13:
        arm_chat.arm_catch_down_rig()



















if __name__ == '__main__':
    # run_a_circle()
    # recognize_run_circle()




    # time.sleep(2)
    # init(autoreset=True)  # 每次print完 自动变成默认颜色
    #
    # arm_chat = Arm_Chat()
    # time.sleep(2)
    # arm_chat.arm_catch_up_lef()
    # print("ul")
    # time.sleep(2)
    # arm_chat.arm_catch_up_mid()
    # print("um")
    # time.sleep(2)
    # arm_chat.arm_catch_up_rig()
    # print("ur")
    # time.sleep(2)
    # arm_chat.arm_catch_down_lef()
    # print("dl")
    # time.sleep(2)
    # arm_chat.arm_catch_down_mid()
    # print("dm")
    # time.sleep(2)
    # arm_chat.arm_catch_down_rig()
    # print("dr")

    # stage_now = "D"           # 处于货架A
    # rec = Recognize()
    # result_needed_location = rec.recognize_for_running(stage_now)
    # for i in range(len(result_needed_location)):
    #     switch_arm(arm_chat,result_needed_location[i])


    car_chat = Car_Chat()
    arm_chat = Arm_Chat()
    yolo = YOLO()
    recognize_run_circle(car_chat,arm_chat,yolo)
    #


