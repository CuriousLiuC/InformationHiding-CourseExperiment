from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
import cv2

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False

def RGB2Gray(img_dir):
	'''
	处理载体图像，RGB转灰度图像函数并resize为256*256大小
	input:
		img_dir:待转化图像的地址
	output:
		ttemp:256*256的列表，其中列表每个位置都是0-255
	'''
	img = Image.open(img_dir)					#读入图像 
	img = img.resize((256,256),Image.BILINEAR)	#width=256, height=256，使用双线性插值
	img = img.convert('L')						#彩色图像转灰度图像
	img_gray = np.asarray(img,np.float32)		#list[[]],256*256个
	return img_gray


#待隐藏图像，要转化成32*32，这样才能进行DCT隐藏，因为是8*8
def RGB2Bin(img_dir):
	'''
	处理待隐藏图像，RGB转灰度图像函数并resize为32*32大小
	32*32是因为DCT每8*8只能隐藏一个bit，所以256*256可以隐藏32*32
	input:
		img_dir:待转化图像的地址
	output:
		ttemp:32*32的列表，其中列表每个位置都是0或1（二值）
	'''
	img = Image.open(img_dir)					#读入图像 
	img = img.resize((32,32),Image.BILINEAR)	#width=256, height=256，使用双线性插值
	img = img.convert('1')						#彩色图像转二值图像
	img_bin = np.asarray(img,np.float32)#list[[]],256*256个
	return img_bin