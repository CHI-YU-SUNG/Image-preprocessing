import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import math
import os
from scipy import ndimage
from skimage.measure import label, regionprops
import getch

def get_rid_of_wrist(origin_img,shift):
	hand_without_wrist = np.copy(origin_img)
	# Obtain mask image
	mask = np.copy(origin_img)
	mask[mask>0] = 255

	# distance transform
	distance_transform = cv2.distanceTransform(mask, cv2.DIST_L2, 3)	
	gray_distance_transform = to_grayscale(distance_transform) # scaling the distance to 0~255
	 		
	#label_image = label(mask)
	props = regionprops(mask)
	#print(len(props))
	#print(props[0].centroid)

	## Obtain the line equation as threshold
	# get each parameter (radius and centeroid)
	radius = distance_transform.max()
	theta_n = (props[0].orientation)*(180/np.pi)+180 # degree
	(x_center, y_center) = props[0].centroid
	theta_n =theta_n*np.pi/180 # degree to radian
	#print("R = {},theta = {},     centroid = {},{}".format(radius,theta_n,x_center,y_center))
	x_point1 = x_center + radius * math.cos(theta_n)
	y_point1 = y_center - radius * math.sin(theta_n)
	x_point2 = x_center - radius * math.cos(theta_n)
	y_point2 = y_center + radius * math.sin(theta_n)
	# shift distance radius
	x_point1_new = x_point1 + shift * radius * abs(math.cos(theta_n))
	y_point1_new = y_point1 + shift * radius * abs(math.sin(theta_n))
	x_point2_new = x_point2 + shift * radius * abs(math.cos(theta_n))
	y_point2_new = y_point2 + shift * radius * abs(math.sin(theta_n))
	#print("point1 = {},{}    point2 = {},{}".format(x_point1,y_point1,x_point2,y_point2))
	#print("point1 = {},{}    point2 = {},{}".format(x_point1_new,y_point1_new,x_point2_new,y_point2_new))
	# Get linear equation 
	slope = (y_point2_new - y_point1_new)/(x_point2_new - x_point1_new)
	bias = y_point1_new - (slope * x_point1_new)

	# check whether the pixel is hand or wrist
	for y, row in enumerate(origin_img):
		for x, pixel in enumerate(row):
			if (wrist(y, x, slope, bias) == True):
				hand_without_wrist[y,x] = 0
	
	#cv2.imwrite('distance_transform/'+datasetlist[i]+'/distance_transform_'+origin_filename[k], gray_distance_transform)
	cv2.imwrite('hand_without_wrist/'+datasetlist[i]+'/hand_without_wrist_'+origin_filename[k], hand_without_wrist)
	#cv2.imwrite('mask/'+datasetlist[i]+'/mask'+origin_filename[k], mask)
	cv2.imwrite('distance_transform/'+datasetlist[i]+'/dt'+origin_filename[k], gray_distance_transform)


def to_grayscale(image):
	scale = 255./(np.max(image) - np.min(image))
	gray = (image - np.min(image))*scale

	return gray


# Private functions ############################################################################

def wrist(pixel_y, pixel_x, slope, bias):
	if pixel_y > (slope * pixel_x + bias):
		return True
	else:
		return False

def print_image(image):
	""" 
		Prints a 2D array nicely. For debugging.
	"""
	
	for y, row in enumerate(image):
		#print(row)
				
		file = open("file2.txt", "a+")
		# Saving the array in a text file 
		content = str(row) 
		file.write(content) 
		file.close() 

if __name__ == "__main__":
	#datasetlist = ["test","test2","test3"];
	datasetlist = ["a","b", "c","d","e"]
	# "CALIBRATION" shift condition
	shift = ['1','2','1.7','1.5','1.5']
	for i in range(len(datasetlist)): # check different folder
		origin_filename=os.listdir(r'/home/acer/Desktop/preprocessing/wrist_line_localization/Dataset/'+datasetlist[i])
		filenumber=np.size(origin_filename)
		for k in range(0, filenumber): # check different file
			# read  origin image 
			origin_image = cv2.imread('Dataset/'+datasetlist[i]+'/'+origin_filename[k])
			gray_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)

			# obtain Wrist line localization
			get_rid_of_wrist(gray_image,float(shift[i]))			

"""
#print_image(gray_mask_image)
#print(np.unique(gray_mask_image))
"""

