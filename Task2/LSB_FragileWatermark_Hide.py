from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
import cv2
from sys import argv
import data_utils

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False


def FragileWaterMark_LSBHide(baseimg_dir,saveimg_dir):
	'''
	基于LSB+奇偶校验的脆弱水印算法-隐藏函数，替换待加入水印图像的最低比特位为奇偶校验
	input:
		baseimg_dir:待加入数字水印的图片
	'''
	#加载并显示原图
	gtimg = Image.open(baseimg_dir)					#读入图像 
	gtimg = gtimg.resize((256,256),Image.BILINEAR)	#width=256, height=256，使用双线性插值
	gtimg = gtimg.convert('L')						#彩色图像转灰度图像
	plt.subplot(1,2,1)								#将原图显示在一行二列中的第一行第一列
	plt.imshow(gtimg, cmap='gray')
	plt.title('嵌入脆弱数字水印前')
	plt.xticks([])
	plt.yticks([])
	
	a = data_utils.RGB2Gray(baseimg_dir)			#将载体图片转化为256*256的列表，其中列表每个位置都是8bit的二进制串
	#脆弱水印算法核心，最低比特位存储前七个比特位的奇偶校验位
	for i in range(256):
		for j in range(256):
			#把a[i][j][0-6]计数1的个数，如果为奇数a[7]=0 否则a[7]=1，
			count = 0
			for k in range(7):
				if a[i][j][k] == '1':
					count += 1
			if count % 2 != 0:
				a[i][j] = a[i][j][0:7] + str(1)
			else:
				a[i][j] = a[i][j][0:7] + str(0)
	
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

	#保存并显示嵌入数字水印后的图像
	array0 = np.array(ttemp)
	pimg0 = Image.fromarray(array0)
	pimg0 = pimg0.convert("L")
	pimg0.save(saveimg_dir+"watermark.bmp")
	plt.subplot(1,2,2)
	plt.imshow(pimg0, cmap='gray')
	plt.title('嵌入脆弱数字水印后')
	plt.xticks([])
	plt.yticks([])
	plt.show()

if __name__ == '__main__':

	if len(argv) != 3:
		print("Usage:<LSB_FragileWatermark_Hide.py> <载体图片地址> <嵌入数字水印后图片要保存到的目录>")
	else:
		baseimg_dir = argv[1]
		saveimg_dir = argv[2]
		FragileWaterMark_LSBHide(baseimg_dir,saveimg_dir)