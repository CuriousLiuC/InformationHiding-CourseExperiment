from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import math
import data_utils
from sys import argv
import cv2

plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False



def DCT_Hide(baseimg_dir,hideimg_dir,saveimg_dir):	
	'''
	基于DCT的信息隐藏，其中hideimg是baseimg的1/64，因为base图片的8*8个块才能隐藏1bit信息
	input:
		baseimg_dir:载体图像的地址
		hideimg_dir:待隐藏图片的地址
		saveimg_dir:隐藏后图片要保存到的目录
	'''


	arr_base = data_utils.RGB2Gray(baseimg_dir)		#将载体图片转化为256*256的列表，其中列表每个位置都是0-255（灰度）
	arr_hide = data_utils.RGB2Bin(hideimg_dir)			#将带隐藏图片转化为32*32的列表，其中列表每个位置是0或1（二值）
	

	#将原有的256*256图像裁剪为32*32=1024个8*8的块
	temp = []
	for i in range(0,32):
		for j in range(0,32):
			temp.append(arr_base[i*8:i*8+8,j*8:j*8+8])
	
	#对每个8*8的块使用cv2模块中的dct函数进行dct变换
	for i in range(1024):
		temp[i] = cv2.dct(temp[i])

	

	#进行信息的隐藏，由于要隐藏的图片已经转化为了32*32的二值，所以在每个8*8块中隐藏1bit
	#选取5,2 4,3两个点
	#如果要嵌入的是1，(5,2)处大于(4,3)处
	#如果要嵌入的是0，(5,2)处小于(4,3)处
	for i in range(32):
		for j in range(32):
			#如果要嵌入的是0
			if arr_hide[i][j] == 0.0:
				if temp[i*32+j][5][2] > temp[i*32+j][4][3]:		#如果5,2大于4,3则交换
					tt = temp[i*32+j][4][3]
					temp[i*32+j][4][3] = temp[i*32+j][5][2]
					temp[i*32+j][5][2] = tt
				elif  temp[i*32+j][5][2] == temp[i*32+j][4][3]:	#如果5,2等于4,3则5,2处-= 1
					temp[i*32+j][5][2] -= 1

			#如果要嵌入的是1
			else:
				if temp[i*32+j][5][2] < temp[i*32+j][4][3]:		#如果5,2小于4,3则交换
					tt = temp[i*32+j][5][2]
					temp[i*32+j][5][2] = temp[i*32+j][4][3]
					temp[i*32+j][4][3] = tt

				elif  temp[i*32+j][5][2] == temp[i*32+j][4][3]:	#如果5,2等于4,3则5,2处+= 1
					temp[i*32+j][5][2] += 1


	#对1024个8*8的块进行逆dct变换
	for i in range(1024):
		temp[i] = cv2.idct(temp[i])


	#把拆分后的图重新组合起来
	#先组合行，再组合列
	#组合开始的时候要先各自组合一轮，以便于后续组合
	#组合第一行
	c = temp[0]
	for i in range(1,32):
		c = np.concatenate((c,temp[i]),axis = 1)
	#组合第二行
	b = temp[32]
	for i in range(33,64):
		b = np.concatenate((b,temp[i]),axis = 1)
	#组合第三行，并再将第三行和之前一二行的组合组合，直到结束
	for i in range(64,1024):
		if i % 32 == 0:
			c = np.concatenate((c,b),axis = 0)
			b = temp[i]
		else:
			b = np.concatenate((b,temp[i]),axis = 1)
	c = np.concatenate((c,b),axis = 0)


	#将组合后的图像保存，作为含秘载体
	pimg0 = Image.fromarray(c)
	pimg0 = pimg0.convert("L")
	pimg0.save(saveimg_dir+"cang.bmp")


if __name__ == '__main__':

	if len(argv) != 4:
		print("Usage:<DCT_Hide.py> <载体图片地址> <待隐藏图片地址> <隐藏后图片要保存到的目录>")
	else:
		baseimg_dir = argv[1]
		contentimg_dir = argv[2]
		saveimg_dir = argv[3]
		DCT_Hide(baseimg_dir,contentimg_dir,saveimg_dir)




#	base_dir = 'C:\\Users\\Administrator\\Desktop\\信息隐藏任务3\\Base.bmp'
#	hide_dir = 'C:\\Users\\Administrator\\Desktop\\信息隐藏任务3\\Hidecontent.bmp'


#	after_hide_dir = 'C:\\Users\\Administrator\\Desktop\\信息隐藏任务3\\cang.bmp'

#	DCT_hide(base_dir, hide_dir)

#	DCT_extract(after_hide_dir)
