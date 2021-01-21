import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math
import os
smallest_depth=4
picture_x=480
picture_y=640
picture_size=128
def cropping(x,y,w,h,img, filename):
	crop_img = img[y-h:y+h, x-w:x+w]
	#cv2.imshow("cropped", crop_img)
	#cv2.waitKey(1)
	cv2.imwrite('crop/crop_'+filename, crop_img)
def handdetect(gray_image):
	mini=gray_image.min()
	gray_image=gray_image-mini
	for i in range(1, picture_x):
		for j in range(1, picture_y):
			if gray_image[i][j]>smallest_depth:
				gray_image[i][j]= 255-mini
			else:
				gray_image[i][j]= gray_image[i][j]
	return gray_image+mini

filename=os.listdir(r'/home/vssdeep/Desktop/chi_yu/preprocessing/Dataset')	
filenumber=np.size(filename)
for k in range(0, filenumber-1):
	image = cv2.imread('Dataset'+filename[k])
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	output=gray_image
	gray_image=handdetect(gray_image)

#find upper left point
	mini=9999999
	for i in range(1, picture_x-picture_size):
		for j in range(1, picture_y-picture_size):
			cut=gray_image[i:i+picture_size, j:j+picture_size]
			a=np.sum(cut)	
			if a<=mini:
				mini=a
				upi=i
				upj=j
#find lower right
	mini=9999999
	for i in range(picture_x, picture_size+1,-1):
		for j in range(picture_y, picture_size+1,-1):
			cut=gray_image[i-picture_size:i, j-picture_size:j]
			a=np.sum(cut)	
			if a<=mini:
				mini=a
				downi=i
				downj=j
#find center point
	centeri=math.ceil((upi+downi)/2)
	centerj=math.ceil((upj+downj)/2)
#print(centeri, centerj)
	cropping(centerj, centeri, math.ceil(picture_size/2), math.ceil(picture_size/2), gray_image, filename[k])#75 is radius


