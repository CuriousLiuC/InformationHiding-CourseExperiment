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


#LSB解码并显示的算法
def LSB_Extract(img_dir):
	'''
	使用LSB算法的提取程序，显示隐藏后的图片和其8个位平面
	input:
		img_dir:待提取图片的地址
	'''
	#加载并显示隐藏后的图片
	img = Image.open(img_dir)				#读入图像 
	img = img.convert('L')					#彩色图像转灰度图像	
	plt.subplot(3,3,1)						#显示在3行3列中第一行第一列位置处
	plt.imshow(img, cmap='gray')
	plt.title('待提取图片')
	plt.xticks([])
	plt.yticks([])

	ttemp = data_utils.RGB2Gray(img_dir)	#将待提取图片转化为256*256的列表，其中列表每个位置都是8bit的二进制串
	#拆分位平面
	t_img = [[] for x in range(10)]
	img = [[] for x in range(10)]
	for i in range(256):
		for j in range(256):
			for k in range(8):				#每个位置8bit串，拆分后对应加入到位平面img[i]中
				t_img[k].append(int(ttemp[i][j][k])*math.pow(2,7-k))
			
		for k in range(8):
			img[k].append(t_img[k])
		t_img = [[] for x in range(10)]

	#逐个位平面输出显示
	arrayy = [[] for x in range(10)]
	pimg = [[] for x in range(10)]
	for i in range(8):
		arrayy[i] = np.array(img[i])
		pimg[i] = Image.fromarray(arrayy[i])
		pimg[i] = pimg[i].convert("L")		#将每个位平面都使用灰度图像显示
		plt.subplot(3,3,i+2)
		plt.imshow(pimg[i], cmap='gray')
		plt.title(u'第'+str(i+1)+'位平面')
		plt.xticks([])
		plt.yticks([])
	plt.show()

if __name__ == '__main__':

	if len(argv) != 2:
		print("Usage:<LSB_Extract.py> <待提取图片地址>")
	else:
		hideimg_dir = argv[1]
		LSB_Extract(hideimg_dir)

