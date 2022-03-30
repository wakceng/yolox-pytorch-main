#---------------------------------------------------#
#
#   此文件用于拍摄一张照片并对此进行预测
#
#---------------------------------------------------#
import re
from turtle import st
from PIL import Image
from unittest import result
from utils.utils import resize_image
from yolo import YOLO

from colorama import init, Fore #print的字体颜色修改
from wck_capture import *

path_catched_now = "D:/yolox-pytorch-main/wck_use/wck_py/capture_now/goods_object_t.jpg"

##  c
# 0 xuehua         CD货架
# 1 dongpeng       CD货架
# 2 red            AB货架
# 3 blue           AB货架
# 4 cube           AB货架
# 5 admilk         E 仓库

class Recognize:
    def __init__(self):
        self.capture=Capture()
        self.path = "D:/yolox-pytorch-main/wck_use/wck_py/capture_now/goods_test_wck.jpg"
        self.img_name = 'object_t'


    def catch_picture(self): 
        self.capture.capture_goods(self.img_name)
        print("catch picture over!")

    def recognize(self):
        self.catch_picture()  ##用camera拍摄照片并保存  在./capture_now/ 中的 goods_object.jpg
        time.sleep(0.1)

        img = path_catched_now
        image = Image.open(img)
        yolo = YOLO()
        r_image , num_of_goods , data_of_goods = yolo.detect_image(image, crop = False)  #crop是否在单张图片预测后对目标进行截取
        #                      data_of_goods 的内容 [c,score,top,left,bottom,right]
        r_image.show()         #可以关
        # print( num_of_goods )
        list_goods_location = []
        for i in range(num_of_goods):   #num_of_goods 是识别到的物品数量
            # print(data_of_goods[i])
            list_goods_location.append(self.a_good_judge(data_of_goods[i]))

        # return num_of_goods , data_of_goods
        print(len(list_goods_location))
        print(list_goods_location)

        return list_goods_location
        ######     [judge_c , judge_score , judge_location]


#--------------------------------------------------------------------#
#
#                     213            426
#          0-------------------------------------->640  x坐标
#          |
#          |
#          |
#          |
#     240  |
#          |
#          |
#          |
#          |
#          v
#         480
#         y坐标
#
#
#--------------------------------------------------------------------#

    def a_good_judge(self,data_ofa_good):
        self.judge_c = data_ofa_good[0]
        self.judge_score = data_ofa_good[1]
        self.judge_x = (  data_ofa_good[3] + data_ofa_good[5]  ) /2       
        self.judge_y = (  data_ofa_good[2] + data_ofa_good[4]  ) /2   



        if self.judge_y > 240 :   #下层
            # if self.judge_x >=600:    #640 * (446+448+310+476)/2200 = 488
            #     pass
            if (self.judge_x >= 350 and self.judge_x <= 488):    #640 * (446+448+310)/2200
                self.judge_location = 13 # 下层 右边
            elif self.judge_x >= 260 :                   #640 * (446+448)/2200
                self.judge_location = 12 # 下层 中间
            elif self.judge_x >= 129 :                   #640 * (446)/2200
                self.judge_location = 11 # 下层 左边
        else:
            # if self.judge_x >=488:    #640 * (446+448+310+476)/2200
            #     pass
            if (self.judge_x >= 350 and self.judge_x <= 488):  # 640 * (446+448+310)/2200
                self.judge_location = 3 # 上层 右边
            elif self.judge_x >= 260:  # 640 * (446+448)/2200
                self.judge_location = 2 # 上层 中间
            elif self.judge_x >= 129:  # 640 * (446)/2200
                self.judge_location = 1 # 上层 左边
            # else:
            #     pass

        # print("物品",self.judge_c,"在",self.judge_location)
        # return [self.judge_c , self.judge_score , self.judge_location]


#-------------------------------------------------------#
#
#     该函数用于，跑外圈时候的识别，return的是要抓的位置     
#      
#-------------------------------------------------------#
    def recognize_for_running(self,stage,yolo):
        # self.catch_picture()  ##用camera拍摄照片并保存  在./capture_now/ 中的 goods_object_t.jpg
        time.sleep(1)
        # print("img loading over")
        img = path_catched_now
        image = Image.open(img)
        print("img open over!")
        # yolo = YOLO()
        # print("yolo over!")
        r_image , num_of_goods , data_of_goods = yolo.detect_image(image, crop = False)  #crop是否在单张图片预测后对目标进行截取
        #                      data_of_goods 的内容 [c,score,top,left,bottom,right]
        # r_image.show()         #可以关
        # print( num_of_goods )
        # print(data_of_goods)
        loc_needed_catch =[]
        
        for i in range(num_of_goods):   #num_of_goods 是识别到的物品数量
            # print(data_of_goods[i])
            # list_goods_location.append(self.a_good_judge(data_of_goods[i]))
            #-----------------------------------------#
            #      在for循环中 对每个judge进行判断
            #-----------------------------------------#
            self.a_good_judge(data_of_goods[i])
            #-----------------------------------------#
            # judge_c
            # 0 xuehua         CD货架
            # 1 dongpeng       CD货架
            # 2 red            AB货架
            # 3 blue           AB货架
            # 4 cube           AB货架
            # 5 admilk         E 仓库
            #-----------------------------------------#
            if stage == "A" or stage == "B":
                if self.judge_c == 2 or self.judge_c == 3 or self.judge_c == 4 :
                    # print(self.judge_location)
                    loc_needed_catch.append(self.judge_location)
            elif stage == "C" or stage == "D":
                if self.judge_c == 0 or self.judge_c == 1 :
                    # print(self.judge_location)
                    loc_needed_catch.append(self.judge_location)



        print("前",loc_needed_catch)
        #以下对 loc_needed_catch 进行排序，将2和12拿到最前面
        ##################################################################
        for i_list in range(1, len(loc_needed_catch)):
            if loc_needed_catch[i_list] == 2:
                    ch_l = loc_needed_catch[0]
                    loc_needed_catch[0] = loc_needed_catch[i_list]
                    loc_needed_catch[i_list] = ch_l
            if loc_needed_catch[i_list] == 12:
                if loc_needed_catch[0] == 2:
                    ch_l = loc_needed_catch[1]
                    loc_needed_catch[1] = loc_needed_catch[i_list]
                    loc_needed_catch[i_list] = ch_l
                else:
                    ch_l = loc_needed_catch[0]
                    loc_needed_catch[0] = loc_needed_catch[i_list]
                    loc_needed_catch[i_list] = ch_l
        ##################################################################

        print("list:", loc_needed_catch)
        return loc_needed_catch

            










if __name__ == '__main__':
    init(autoreset=True)#每次print完 自动变成默认颜色
    rec = Recognize()
    time.sleep(3)
    yolo = YOLO()
    re_list_goods_location = rec.recognize_for_running("D",yolo)
    # print("list:",re_list_goods_location)


    