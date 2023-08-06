import cv2 as cv
import sys
import os
import matplotlib.pyplot as plt
from PIL import Image

if __name__ == '__main__':
    #读取图像并判断是否读取成功
    root_path = '/home/xjm/Code/R2GenCMN-main/Aug_image/d646_0015_again/'
    save_path = '/home/xjm/Code/R2GenCMN-main/Aug_image/d646_0015_again_all/'
    if not os.path.exists(save_path):
        os.makedirs(save_path,exist_ok=True)
    top_ax = [85,133]  #h,w
    bottom_ax = [200,190]
    Aug_para = 2
    Aug_location = 'left'
    for img_name in os.listdir(root_path):
        if 'no_limited' not in img_name:
            img_path = os.path.join(root_path, img_name)
            #cv2读出来的坐标是h,w,c(比如288，512，3) Image.open读出来是(w,h),比如512，288
            img = cv.imread(img_path)
            # img = cv.imread("/home/xjm/Code/R2GenCMN-main/WAIFA/vm512-motion-0020/0095--rvm.png")
            # img_= Image.open("/home/xjm/Code/R2GenCMN-main/WAIFA/vm512-motion-0020/0095--rvm.png")
            
            #需要放大的部分  这里是cv2读取的图片，所以，第二维度是宽，也就是x轴，第一维度是高，也就是y轴
            part = img[top_ax[0]:bottom_ax[0],top_ax[1]:bottom_ax[1]]  #h,w(y,x)
            #双线性插值法
            orig_heiht = bottom_ax[0] - top_ax[0]
            orig_width = bottom_ax[1] - top_ax[1]

            Aug_width = int(orig_width * Aug_para)
            Aug_height = int(orig_heiht * Aug_para)
            mask = cv.resize(part, (Aug_width, Aug_height), fx=0, fy=0, interpolation=cv.INTER_LINEAR) #cv.resize要用w,h(即x,y)
            if img is None is None:
                print('Failed to read picture')
                sys.exit()
                
            #放大后局部图的位置h,w
            if Aug_location == 'left':
                Aug_top = [top_ax[0] - int((orig_heiht * (Aug_para -1) )// 2) + 50 ,top_ax[1]- Aug_width -10] #h,w
                img[Aug_top[0]: Aug_top[0] + Aug_height, Aug_top[1]:Aug_top[1] + Aug_width]=mask
                cv.rectangle(img,(top_ax[1],top_ax[0]),(bottom_ax[1],bottom_ax[0]),(255,255,0),1)
                cv.rectangle(img,(Aug_top[1],Aug_top[0]),(Aug_top[1] + Aug_width,Aug_top[0] + Aug_height),(255,255,0),1)
                img = cv.line(img,(Aug_top[1]+ Aug_width, Aug_top[0]),(top_ax[1], top_ax[0]),(255,255,0))
                img = cv.line(img,(Aug_top[1]+ Aug_width,Aug_top[0] + Aug_height),(top_ax[1], bottom_ax[0]),(255,255,0))
            elif Aug_location == 'right':
                Aug_top = [top_ax[0] - int((orig_heiht * (Aug_para -1) )// 2) +100, bottom_ax[1] + 30]
                img[Aug_top[0]: Aug_top[0] + Aug_height, Aug_top[1]:Aug_top[1] + Aug_width]=mask
                cv.rectangle(img,(top_ax[1],top_ax[0]),(bottom_ax[1],bottom_ax[0]),(0,0,255),1)
                cv.rectangle(img,(Aug_top[1],Aug_top[0]),(Aug_top[1] + Aug_width,Aug_top[0] + Aug_height),(0,0,255),1)
                img = cv.line(img,(Aug_top[1], Aug_top[0]),(bottom_ax[1], top_ax[0]),(0,0,255))
                img = cv.line(img,(Aug_top[1], Aug_top[0] + Aug_height),(bottom_ax[1], bottom_ax[0]),(0,0,255))
                # img = cv.line(img,(Aug_top[1],Aug_top[2]),(100,50),(0,255,0))
                # img = cv.line(img,(350,400),(100,350),(0,255,0))
            elif Aug_location == 'bottom':
                Aug_top = [top_ax[0] - int((orig_heiht * (Aug_para -1) )// 2) +120, top_ax[1] + 10]  #h,w
                img[Aug_top[0]: Aug_top[0] + Aug_height, Aug_top[1]:Aug_top[1] + Aug_width]=mask
                cv.rectangle(img,(top_ax[1],top_ax[0]),(bottom_ax[1],bottom_ax[0]),(0,0,255),1) #w,h
                cv.rectangle(img,(Aug_top[1],Aug_top[0]),(Aug_top[1] + Aug_width,Aug_top[0] + Aug_height),(0,0,255),1)
                img = cv.line(img,(Aug_top[1], Aug_top[0]),(top_ax[1], bottom_ax[0]),(0,0,255)) #w,h
                img = cv.line(img,(Aug_top[1] + Aug_height, Aug_top[0]),(bottom_ax[1], bottom_ax[0]),(0,0,255))

            #画框并连线cv2的函数都是x,y的坐标
           

            #展示结果
            image_save_path = os.path.join(save_path, img_name)
            cv.imwrite(image_save_path,img)