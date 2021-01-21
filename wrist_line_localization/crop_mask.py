import cv2
import numpy as np
import math
from scipy import ndimage
import os
def crop_out_mask(mask,origin):
	"""
	cropmask image 
	"""
	# Find nonzero value
	image_start_x = 10000
	image_start_y = 10000
	image_end_y = 0
	image_end_x = 0
	for y, row in enumerate(mask):
		for x, pixel in enumerate(row):
			if mask[y,x] == 255:
				image_start_y = y if image_start_y > y else image_start_y
				image_start_x = x if image_start_x > x else image_start_x
				image_end_y = y if image_end_y < y else image_end_y
				image_end_x = x if image_end_x < x else image_end_x

	# Get the height and width
	image_width = image_end_x - image_start_x
	image_height = image_end_y - image_start_y
	# crop image
	crop_img = origin[image_start_y:image_end_y, image_start_x:image_end_x]
		
	# zero paddig on short side 	
	if image_width > image_height:
		if (image_width-image_height)%2 == 1: # The difference of width and height is odd
			padding = cv2.copyMakeBorder(crop_img,math.ceil((image_width-image_height)/2),math.ceil((image_width-image_height)/2),1,0,cv2.BORDER_CONSTANT,value=0)
		else:                                 # The difference of width and height is even
			padding = cv2.copyMakeBorder(crop_img,math.ceil((image_width-image_height)/2),math.ceil((image_width-image_height)/2),0,0,cv2.BORDER_CONSTANT,value=0)
	
	else:
		if (image_width-image_height)%2 == 1: # The difference of width and height is odd
			padding = cv2.copyMakeBorder(crop_img,1,0,math.ceil((image_height-image_width)/2),math.ceil((image_height-image_width)/2),cv2.BORDER_CONSTANT,value=0)
		else:                                 # The difference of width and height is even
			padding = cv2.copyMakeBorder(crop_img,0,0,math.ceil((image_height-image_width)/2),math.ceil((image_height-image_width)/2),cv2.BORDER_CONSTANT,value=0)		
	
	#print(image_height)
	#print(image_width)
	return padding
	
# Private functions ############################################################################
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
	# folder	
	#datasetlist = ["test","test2"];
	datasetlist = ["a","b", "c","d","e"]	
	# parameter
	dimension_64 = 64
	
	for i in range(len(datasetlist)): # check different folder			
		# path	
		origin_filename=os.listdir(r'/home/acer/Desktop/preprocessing/wrist_line_localization/Dataset/'+datasetlist[i])			
		filenumber=np.size(origin_filename)
		for k in range(0, filenumber): # check different file
			# read mask image and origin image			
			mask_image = cv2.imread('mask/'+datasetlist[i]+'/crop_'+origin_filename[k])
			origin_image = cv2.imread('Dataset/'+datasetlist[i]+'/'+origin_filename[k])
			gray_mask_image = cv2.cvtColor(mask_image, cv2.COLOR_RGB2GRAY)
			gray_image = cv2.cvtColor(origin_image, cv2.COLOR_RGB2GRAY)
			# crop the mask	and origin image
			crop_mask_image = crop_out_mask(gray_mask_image,gray_mask_image)
			crop_image = crop_out_mask(gray_mask_image,gray_image)
			#print(np.unique(crop_image))
			# resize
			#result_64 = cv2.resize(crop_image, (dimension_64, dimension_64), interpolation = cv2.INTER_CUBIC)

			cv2.imwrite('crop_mask/'+datasetlist[i]+'/crop_mask_'+origin_filename[k], crop_mask_image)
			cv2.imwrite('hand_without_resize/'+datasetlist[i]+'/hand_without_resize'+origin_filename[k], crop_image)
		print(i)



"""
	＃check whether the folder exist
    output = '%s_mask/' % gesture
    if not os.path.exists(output):
        os.makedirs(output)
    img.save(output + '%s' % name)
    print(name)
"""

