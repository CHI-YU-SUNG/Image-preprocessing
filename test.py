import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math
import os
def ccl(gray_image):
	

filename=os.listdir(r'/home/vssdeep/Desktop/chi_yu/preprocessing/Dataset/test')	
filenumber=np.size(filename)

for k in range(0, filenumber):
	image = cv2.imread('Dataset/test/'+filename[k])
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	cv2.imshow('crop_'+filename[k],gray_image)
	cv2.imwrite('crop/crop_'+filename[k], gray_image)
	# 按下任意鍵則關閉所有視窗
	cv2.waitKey(0)
	cv2.destroyAllWindows()


