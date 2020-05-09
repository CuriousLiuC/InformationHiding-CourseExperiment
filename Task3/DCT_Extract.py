from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
import data_utils
from sys import argv
import cv2

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False


def DCT_Extract(img_dir):
	'''
	基于DCT的隐藏信息提取
	input:
		img_dir:待提取图像的地址
	'''

	after_hide = data_utils.RGB2Gray(img_dir)		#将载体图片转化为256*256的列表，其中列表每个位置都是0-255（灰度）

	#将256*256图像裁剪为32*32=1024个8*8的块
	temp = []
	for i in range(0,32):
		for j in range(0,32):
			temp.append(after_hide[i*8:i*8+8,j*8:j*8+8])


	#这里提取的时候还要先DCT变换过去，之后比的是DCT系数
	#对1024个块每个块进行dct变化
	for i in range(1024):
		temp[i] = cv2.dct(temp[i])


	#进行隐藏信息的提取，比较每个块中5,2 和4,3两个dct变换后数值的大小，重构32*32的二值图像
	#(5,2)处大于(4,3)处，嵌入的是1
	#(5,2)处小于(4,3)处，嵌入的是0
	changtemp = []
	chang = []
	for i in range(32):
		for j in range(32):

			#攻击的时候可能会有等于，怎么说
			if temp[i*32+j][5][2] >= temp[i*32+j][4][3]:		
				changtemp.append(int(1))

			elif temp[i*32+j][5][2] < temp[i*32+j][4][3]:
				changtemp.append(int(0))
		chang.append(changtemp)
		changtemp = []


	#显示提取后的隐藏图片
	arrayy2 = np.array(chang)
	#print(arrayy2.shape)
	print(arrayy2)
	pimg2 = Image.fromarray(arrayy2)
	pimg2 = pimg2.convert("L")
	plt.subplot(1,4,3)
	plt.imshow(pimg2, cmap='gray')
	plt.title(u'提取出的水印')
	plt.xticks([])
	plt.yticks([])

	plt.show()

if __name__ == '__main__':

	if len(argv) != 2:
		print("Usage:<DCT_Extract.py> <载体图片地址> <待隐藏图片地址> <隐藏后图片要保存到的目录>")
	else:
		img_dir = argv[1]
		DCT_Extract(img_dir)