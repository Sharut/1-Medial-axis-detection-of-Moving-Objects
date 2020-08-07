import cv2
import os
from os.path import isfile, join

def SaveVideo(name):
	if(name=='0'):
		name=10
	w_path = './Videos/result_'+name+'.avi'
	r_path = './Final-Frames'  
	#frame = cv2.imread(r_path+'/'+'Frame0.jpg')
	files = [f for f in os.listdir(r_path) if (isfile(join(r_path, f)) and not f.startswith('.') and f.endswith('_'+name+'.jpg'))]
	files.sort(key = lambda x: int(x[5:-6]))
	# print(files)
	frame_array = []
	for i in range(len(files)):
	    filename=r_path +'/'+ files[i]
	    if i%100 ==0:
	    	print(filename)
	    #reading each files
	    img = cv2.imread(filename)
	    height, width, layers = img.shape
	    size = (width,height)
	    
	    #inserting the frames into an image array
	    frame_array.append(img)
	myvideo = cv2.VideoWriter(w_path,cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
	for i in range(len(frame_array)):
	    # writing to a image array
	    myvideo.write(frame_array[i])
