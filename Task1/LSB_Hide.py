from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
from sys import argv
import cv2
import data_utils

#matplotlib显示中文标签用
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False



def LSB_Hide(baseimg_dir,hideimg_dir,saveimg_dir):
	'''
	使用LSB算法的嵌入程序，将待隐藏图片嵌入载体中，显示嵌入前后图片，并保存嵌入后图片
	input:
		baseimg_dir:载体图像的地址
		hideimg_dir:待隐藏图片的地址
		saveimg_dir:隐藏后图片要保存到的目录
	'''

	#读入并显示嵌入前图像
	gtimg = Image.open(baseimg_dir)					#读入图像 
	gtimg = gtimg.resize((256,256),Image.BILINEAR)	#width, height，使用双线性插值
	gtimg = gtimg.convert('L')						#彩色图像转灰度图像
	plt.subplot(1,2,1)								#原图显示在第一行第一个
	plt.imshow(gtimg, cmap='gray')
	plt.title('LSB信息隐藏前')
	plt.xticks([])
	plt.yticks([])


	a = data_utils.RGB2Gray(baseimg_dir)			#将载体图片转化为256*256的列表，其中列表每个位置都是8bit的二进制串
	c = data_utils.RGB2Bin(hideimg_dir)				#将待隐藏图片转化为256*256的列表，其中每个位置是0或1（二值图像）

	#LSB信息隐藏算法核心，替换掉最低有效位
	#修改代码可以达到其他位平面替换
	for i in range(256):
		for j in range(256):
			a[i][j] = a[i][j][0:7] + str(int(c[i][j]))		#最低位信息隐藏
			#a[i][j] =  str(int(c[i][j])) + a[i][j][1:8]	#最高位信息隐藏


	#将256*256列表中每个位置的8bit串转化为0-255的数字，仍保持256*256大小
	temp = []
	ttemp = []
	summ = 0
	for i in range(256):
		for j in range(256):
			for k in range(8):
				summ += int(a[i][j][k]) * math.pow(2,7-k)
			temp.append(int(summ))
			summ = 0
		ttemp.append(temp)
		temp = []		

	array0 = np.array(ttemp)						#从数组中恢复图片
	pimg0 = Image.fromarray(array0)
	pimg0 = pimg0.convert("L")
	pimg0.save(saveimg_dir+"cang.bmp")
	plt.subplot(1,2,2)								#隐藏后的图片显示在第一行第二个
	plt.imshow(pimg0, cmap='gray')
	plt.title('LSB信息隐藏后')
	plt.xticks([])
	plt.yticks([])
	plt.show()



if __name__ == '__main__':
	
	if len(argv) != 4:
		print("Usage:<LSB_Hide.py> <载体图片地址> <待隐藏图片地址> <隐藏后图片要保存到的目录>")
	else:
		baseimg_dir = argv[1]
		contentimg_dir = argv[2]
		saveimg_dir = argv[3]
		LSB_Hide(baseimg_dir,contentimg_dir,saveimg_dir)
