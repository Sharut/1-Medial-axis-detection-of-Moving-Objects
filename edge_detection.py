#IDENTIFY EDGES (DERIVATIVES)

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def EdgeDetection(video,type="canny",kernel=3):

	w_path = './Edge-Detection-Results/Laplacians'
	r_path = './Image-Cleaning-Results/cleaned'
	
	for img_name in os.listdir(r_path):
		if not img_name.endswith(video+'.jpg'):
			continue
		# loading image
		img = cv2.imread(r_path+'/'+img_name)
		#print(img_name)

		# converting to gray scale
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# remove noise
		img = cv2.GaussianBlur(gray,(3,3),0)

		# convolute with proper kernels
		if type == 'laplacian':
			out = cv2.Laplacian(img,cv2.CV_64F,ksize=kernel)
		elif type == 'sobelx':
			out = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=kernel)  
		elif type == 'sobely':
			out = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=kernel)
		elif type == 'sobelxy':
			out = cv2.Sobel(img,cv2.CV_64F,1,1,ksize=kernel)
		elif type == 'canny':
			v = np.mean(img)
			# print(v)
			sigma = 0.5
			lower = int(max(0, (1.0 - sigma) * 30*v))
			upper = int(min(255, (1.0 + sigma) * 30*v))
			out = cv2.Canny(img,lower,upper)

		#print(np.unique(out))
		cv2.imwrite(os.path.join(w_path ,img_name),out)
