from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
import cv2
from sys import argv
import data_utils

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False


#数字水印提取并比较
def FragileWaterMark_LSBExtract(img_dir):

	'''
	基于LSB+奇偶校验的脆弱水印算法-水印提取函数，提取加入的水印检测是否遭到篡改，并显示遭到篡改的区域
	input:
		img_dir:待提取数字水印的图片（可能遭遇攻击）
	'''

	#读入待提取图片并显示
	img = Image.open(img_dir)
	plt.subplot(1,4,1)
	plt.imshow(img, cmap='gray')
	plt.title('Watermark Image')
	plt.xticks([])
	plt.yticks([])

	ttemp = data_utils.RGB2Gray(img_dir)	#将待提取图片转化为256*256的列表，其中列表每个位置都是8bit的二进制串
	#提取出最低比特位的图片，并显示
	t_img = []
	img1 = []
	for i in range(256):
		for j in range(256):
			t_img.append(int(ttemp[i][j][7])*math.pow(2,7-7))
		img1.append(t_img)
		t_img = []
	arrayy = np.array(img1)
	pimg = Image.fromarray(arrayy)
	pimg = pimg.convert("L")
	plt.subplot(1,4,2)
	plt.imshow(pimg, cmap='gray')
	plt.title(u'直接提取得到的水印')
	plt.xticks([])
	plt.yticks([])

	#依据0-6角标处位平面，计算出应有的数字水印
	tt_img = []
	img2 = []

	for i in range(256):
		for j in range(256):
			#把a[i][j][0-6]计数，如果为奇数a[7]=0 否则a[7]=1，
			count = 0
			for k in range(7):
				if ttemp[i][j][k] == '1':
					count += 1
			if count % 2 != 0:
				tt_img.append(int(1))
			else:
				tt_img.append(int(0))
		img2.append(tt_img)
		tt_img = []
	arrayy2 = np.array(img2)
	pimg2 = Image.fromarray(arrayy2)
	pimg2 = pimg2.convert("L")
	plt.subplot(1,4,3)
	plt.imshow(pimg2, cmap='gray')
	plt.title(u'计算得到的水印')
	plt.xticks([])
	plt.yticks([])

	#比较直接提取得到的水印，和通过计算得到的水印，判断是否遭遇篡改
	flag = 1	
	showimg = Image.new("RGB",(256,256))		#创建一张新的256*256的图，来标出遭遇篡改的区域
	arr = np.array(showimg)
	for i in range(256):
		for j in range(256):
			#如果遭遇篡改，将对应位置处角标设置为红色（255,0,0）
			if arrayy[i][j] != arrayy2[i][j]:
				flag = 0
				arr[i][j][0] = 255
	if flag:
		print("未检测到遭遇篡改")
	else:
		print("检测到遭遇篡改！")

		#如果检测到遭遇篡改，就打出这张图片
		pimg3 = Image.fromarray(arr)
		plt.subplot(1,4,4)
		plt.imshow(pimg3)
		plt.title(u'检测到的篡改区域')
		plt.xticks([])
		plt.yticks([])
	plt.show()

if __name__ == '__main__':

	if len(argv) != 2:
		print("Usage:<LSB_FragileWatermark_Extract.py> <待提取水印图片地址>")
	else:
		img_dir = argv[1]
		FragileWaterMark_LSBExtract(img_dir)


