import cv2
import numpy as np
import os

# Morphological transformations are some simple operations based on the image shape.

def Cleaning(video,type,kernel,structural="no",size=100):

	w_path = './Image-Cleaning-Results/cleaned'
	r_path = './Background-Subtraction-Frames'
	kernel = np.ones((kernel,kernel),np.uint8)  #Create a kernel for erosion
	for img_name in os.listdir(r_path):
		if not img_name.endswith(video+'.jpg'):
			continue
		img = cv2.imread(r_path+'/'+img_name)


		if type == "erosion":
			'''
			Method 1: EROSION
			The basic idea of erosion is just like soil erosion only, 
			it erodes away the boundaries of foreground object (Always 
			try to keep foreground in white)
			A pixel in the original image (either 1 or 0) will be 
			considered 1 only if all the pixels under the kernel
			is 1, otherwise it is eroded (made to zero).
			'''
			out = cv2.erode(img,kernel,iterations = 1)
			# cv2.imwrite(os.w_path.join(w_path ,'Erosion'+ str(size) + 'X' + str(size) + '.jpg'),erosion)

		elif type == "dilation":
			'''
			Method 2: DILATION
			It is just opposite of erosion. Here, a pixel element is 
			‘1’ if atleast one pixel under the kernel is ‘1’. So it 
			increases the white region in the image or size of foreground 
			object increases. Normally, in cases like noise removal, 
			erosion is followed by dilation. Because, erosion removes 
			white noises, but it also shrinks our object. So we dilate it.
			'''
			out = cv2.dilate(img,kernel,iterations = 1)

		elif type == "opening":
			'''
			Method 3: OPENING
			Opening is just another name of erosion followed by dilation. 
			It is useful in removing noise, as we explained above. 
			'''
			out = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

		elif type == "closing":
			'''
			Method 4: CLOSING
			Closing is reverse of Opening, Dilation followed by Erosion. 
			It is useful in closing small holes inside the foreground
			objects, or small black points on the object.
			'''
			out = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

		elif type == "gradient":
			'''
			Method 5: Morphological Gradient
			It is the difference between dilation and erosion of an image.
			The result will look like the outline of the object.
			'''
			gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

		elif type == "tophat":
			'''
			Method 6: Top Hat
			It is the difference between input image and Opening of the image. 
			'''
			out = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

		elif type == "blackhat":
			'''
			Method 7: Black Hat
			It is the difference between the closing of the input image and input image.
			'''
			out = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
		if(structural=="yes"):
			# cv2.imshow('original.jpg',out)
			# key = cv2.waitKey(30000)
			# if key==27:
			# 	cv2.destroyAllWindows()
			# Specify size on horizontal axis
			horizontal_size = 1920//100
			horizontal = out.copy()
			# Create structure element for extracting horizontal lines through morphology operations
			horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,(horizontal_size, 1))
			# Apply morphology operations
			out1=cv2.erode(horizontal, horizontalStructure)
			out1=cv2.dilate(out1, horizontalStructure)
			# cv2.imshow('mask.jpg',out1)
			# key = cv2.waitKey(30000)
			# if key==27:
			# 	cv2.destroyAllWindows()
			out1=cv2.bitwise_not(out1)
			out=cv2.bitwise_and(out,out1)
			# cv2.imshow('final.jpg',out)
			# key = cv2.waitKey(30000)
			# if key==27:
			# 	cv2.destroyAllWindows()
		cv2.imwrite(os.path.join(w_path ,img_name),out)
