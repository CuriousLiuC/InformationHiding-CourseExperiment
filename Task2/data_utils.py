from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
import cv2
from sys import argv

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False

#载体
def RGB2Gray(img_dir):
	'''
	处理载体图像，RGB转灰度图像函数并resize为256*256大小
	input:
		img_dir:待转化图像的地址
	output:
		ttemp:256*256的列表，其中列表每个位置都是8bit的二进制串
	'''
	img = Image.open(img_dir)							#读入图像
	img = img.resize((256,256),Image.BILINEAR)			#width=256, height=256，使用双线性插值放缩
	img = img.convert('L')								#彩色图像转灰度图像						
	img_gray = np.asarray(img)							#list[[]],256*256个，现在list每个位置是0-255（灰度图像）

	#将list中每个位置的0-255转化为8bit的二进制串
	temp = []
	ttemp = []
	for i in range(256):
		for j in range(256):
			temp.append('{:08b}'.format(img_gray[i][j]))#关键转化代码，确保补足8位
		ttemp.append(temp)
		temp = []

	return ttemp										#返回256*256的列表，其中列表每个位置都是8bit的二进制串