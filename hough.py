#IDENTIFY LINES (HOUGH TRANSFORM)

import cv2
import numpy as np
import os
import math
from os.path import isfile, join
import statistics
import random

def find_key(mydict, search_val):
	for key, value in mydict.items():
	    if value == search_val:
	        return key


def HoughTransform(video):
	c_array={}
	param_array={}
	w_path1 = 'Line-Detection-Results/all'
	w_path2 = 'Line-Detection-Results/max_freq'
	r_path = 'Edge-Detection-Results/Laplacians'
	o_path = 'Final-Frames'
	o1_path = 'Final-Frames1'
	xa=0
	xb=0
	ya=0
	yb=0
	files = [f for f in os.listdir(r_path) if (isfile(join(r_path, f)) and not f.startswith('.') and f.endswith('_'+video+'.jpg'))]
	print(files[0][5:-6])
	files.sort(key = lambda x: int(x[5:-6]))
	
	frame_array = []


	avg_length = 100
	counter=0
	m_array={'x1':[],'x2':[],'y1':[],'y2':[]}
	window=5 # 11 on each side
	# gaussian = [1/64 , 6/64, 15/64, 20/64, 15/64, 6/64, 1/64]
	gaussian = [35/1230,  50/1230,  100/1230,  150/1230, 180/1230, 200/1230, 180/1230, 150/1230, 100/1230,  50/1230, 35/1230] 
	for i in range(len(files)):
		c_array[str(i)]={}
		img_name=files[i]
		if not img_name.endswith('.jpg'):
			continue

		frame_no = img_name[5:-6]
		original_img  =	cv2.imread('Frames/'+img_name)
		original_img1 = cv2.imread('Frames/'+img_name)
		original_img2 = cv2.imread('Frames/'+img_name)

		img = cv2.imread(r_path+'/'+img_name)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		avg_int=np.mean(gray)
		# print("Abg intensity is ",np.mean(gray))

		lines = cv2.HoughLinesP(gray, rho = 1, theta = 1*np.pi/180, threshold = 60, minLineLength = max(avg_length,100), maxLineGap = 100)
		# print(lines)
		if(lines is None or len(lines)<=0):
			cv2.line(original_img1,(xa, ya),(xb,yb),(0,0,255),3)
			cv2.line(original_img2,(xa, ya),(xb,yb),(0,0,255),3)
			cv2.imwrite(os.path.join(w_path1 ,img_name),original_img1)
			cv2.imwrite(os.path.join(w_path2 ,img_name),original_img2)

			# counter+=1
			# if counter<8:
				# cv2.line(original_img,(xa,ya),(xb,yb),(0,0,255),3)
			# else: 
				# print(frame_no)
			# cv2.imwrite(os.path.join(o_path ,img_name),original_img)
			c_array[frame_no][(float((yb-ya)/(xb-xa+0.00012)))]=(xa,ya,xb,yb)
			if(ya>yb):
				(s,t)=(xa,ya)
				(xa,ya)=(xb,yb)
				(xb,yb)=(s,t)
			m_array['x1'].append(xa)
			m_array['x2'].append(xb)
			m_array['y1'].append(ya)
			m_array['y2'].append(yb)


		else:
			counter=0
			maps={}
			avg_length=0
			line_count=0
			for i in range(len(lines)):
				cv2.line(original_img1,(xa, ya),(xb,yb),(0,0,255),3)
				line_count+=len(lines[i])
				for x1,y1,x2,y2 in lines[i]:
					avg_length += math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
					cv2.line(original_img1,(x1, y1),(x2,y2),(0,0,255),3)
					slope = (float)((y2-y1)/(x2-x1+0.0001))
					theta = math.atan(slope)
					if(theta*180/np.pi//10 not in maps.keys()):
						maps[theta*180/np.pi//10]=[]
					maps[theta*180/np.pi//10].append((x1,y1,x2,y2,theta))
			avg_length/=line_count*1.17
			avg_length+=np.random.normal(-10,10)
			if(int(frame_no)%20==0):
				print('frame_no ',str(frame_no),':',str(avg_length))
			#print(maps)
			maximum = -math.inf
			for b,a in maps.items():
				if(len(a)>maximum):
					maxbin = a
					my_theta = b*10
					maximum = len(a)


			# if (abs(my_theta-prev_theta)>20):
			# 	cv2.line(original_img2,(xa, ya),(xb,yb),(0,255,255),2)
			# 	cv2.imwrite(os.path.join(w_path2 ,img_name),original_img2)
			# 	continue

			maxi = -math.inf
			mini = math.inf
			
			(rx1,ry1,rx2,ry2,theta1)=maxbin[0]
			for x1,y1,x2,y2,theta in maxbin:
				prev_theta = theta*180/np.pi
				cv2.line(original_img2,(x1, y1),(x2,y2),(0,0,255),3)
				slope = (float)((y2-y1)/(x2-x1+0.0001))
				c = y1 - slope * x1
				if(c<=mini):
					lx1 = x1 
					ly1 = y1 
					lx2 = x2 
					ly2 = y2 
					mini=c
				elif(c>=maxi):
					rx1 = x1 
					ry1 = y1 
					rx2 = x2 
					ry2 = y2 
					maxi=c
			# if(ly1>ry1):
			# 	print('lx1 rx1: ',str(lx1),str(rx1))

			if(len(maxbin)>=2):
				xa = int((lx1 + rx1)/2)
				ya = int((ly1 + ry1)/2)
				xb = int((lx2 + rx2)/2)
				yb = int((ly2 + ry2)/2)
				c_array[frame_no][(float((yb-ya)/(xb-xa+0.00012)))]=(xa,ya,xb,yb)
				if(ya>yb):
					(s,t)=(xa,ya)
					(xa,ya)=(xb,yb)
					(xb,yb)=(s,t)
				m_array['x1'].append(xa)
				m_array['x2'].append(xb)
				m_array['y1'].append(ya)
				m_array['y2'].append(yb)
				# cv2.line(original_img,(xa, ya),(xb,yb),(0,0,255),3)

				# cv2.line(original_img,(lx1, ly1),(lx2,ly2),(255,0,0),2)
				# cv2.line(original_img,(rx1, ry1),(rx2,ry2),(0,0,255),2)
			else:
				xa = int(x1)
				xb = int(x2)
				ya = int(y1)
				yb = int(y2)
				c_array[frame_no][(float((y2-y1)/(x2-x1+0.00012)))]= (x1,y1,x2,y2)
				if(y1>y2):
					(s,t)=(x1,y1)
					(x1,y1)=(x2,y2)
					(x2,y2)=(s,t) 
				m_array['x1'].append(x1)
				m_array['x2'].append(x2)
				m_array['y1'].append(y1)
				m_array['y2'].append(y2)
				# cv2.line(original_img,(xa, ya),(xb,yb),(0,0,255),3)

			# cv2.imwrite(os.path.join(o_path ,img_name),original_img)
			cv2.imwrite(os.path.join(w_path1 ,img_name),original_img1)
			cv2.imwrite(os.path.join(w_path2 ,img_name),original_img2)


	med_array=[]
	print("mean filtering started....")
	for i in range(window):
		img_name=files[i]
		my_img = cv2.imread('Frames/'+img_name)
		my_img1  = cv2.imread('Frames/'+img_name)
		cv2.line(my_img,(m_array['x1'][i], m_array['y1'][i]),(m_array['x2'][i],m_array['y2'][i]),(0,0,255),3)
		cv2.imwrite(os.path.join(o_path ,img_name),my_img)
		# theta=math.atan((m_array['y2'][i]-m_array['y1'][i])/(m_array['x2'][i]-m_array['x1'][i]+0.00012))
		(avg_coordx1_prev,avg_coordx2_prev,avg_coordy1_prev,avg_coordy2_prev)=(m_array['x1'][i], m_array['y1'][i],m_array['x2'][i],m_array['y2'][i])
	equal_count=0
	flag = True
	for i in range(window,len(files)-window):
		img_name=files[i]
		my_img = cv2.imread('Frames/'+img_name)
		# med_frame = statistics.mean([list(c_array[str(i-2)].keys())[0],list(c_array[str(i-1)].keys())[0],list(c_array[str(i)].keys())[0],list(c_array[str(i+1)].keys())[0],list(c_array[str(i+2)].keys())[0]])
		
		# if(abs(math.atan((m_array['y2'][i+window]-m_array['y1'][i+window])/(m_array['x2'][i+window]-m_array['x1'][i+window]+0.00012)) - theta) <= math.pi/18):
		# 	theta=math.atan((m_array['y2'][i+window]-m_array['y1'][i+window])/(m_array['x2'][i+window]-m_array['x1'][i+window]+0.00012))
		# else :
		# 	f=0.0
		# 	m_array['x1'][i+window]=int(m_array['x1'][i+window-1]*f+m_array['x1'][i+window]*(1-f))
		# 	m_array['x2'][i+window]=int(m_array['x2'][i+window-1]*f+m_array['x2'][i+window]*(1-f))
		# 	m_array['y1'][i+window]=int(m_array['y1'][i+window-1]*f+m_array['y1'][i+window]*(1-f))
		# 	m_array['y2'][i+window]=int(m_array['y2'][i+window-1]*f+m_array['y2'][i+window]*(1-f))
		avg_coordx1 = int(np.average(m_array['x1'][i-window:i+window+1]))
		avg_coordx2 = int(np.average(m_array['x2'][i-window:i+window+1]))
		avg_coordy1 = int(np.average(m_array['y1'][i-window:i+window+1]))
		avg_coordy2 = int(np.average(m_array['y2'][i-window:i+window+1]))


		
		if (avg_coordx1_prev,avg_coordx2_prev,avg_coordy1_prev,avg_coordy2_prev) == (avg_coordx1,avg_coordx2,avg_coordy1,avg_coordy2):
			equal_count+=1
			print('equal count & frame: ',equal_count,i)

			flag=True
			if(equal_count<=3):
				cv2.line(my_img,(avg_coordx1_prev+int(2*np.random.normal()), avg_coordy1_prev+int(2*np.random.normal())),
							(avg_coordx2_prev+int(2*np.random.normal()),avg_coordy2_prev+int(2*np.random.normal())),(0,0,255),3)
			# else:
				# print(equal_count)

		else:
			if(equal_count>=3 and flag):
				# print('set eql cnt for frame:',i)
				equal_count=2*window
				flag = False
			equal_count-=1
			if(equal_count<=0):
				flag=True
				# print('frame no: ',i)
				equal_count=0
				(avg_coordx1_prev,avg_coordx2_prev,avg_coordy1_prev,avg_coordy2_prev)=(avg_coordx1,avg_coordx2,avg_coordy1,avg_coordy2)
				cv2.line(my_img,(avg_coordx1_prev, avg_coordy1_prev),(avg_coordx2_prev,avg_coordy2_prev),(0,0,255),3)

		cv2.imwrite(os.path.join(o_path ,img_name),my_img)
		# for j in range(-window,window+1):
		# 	if(i+j>=0 and i+j<=len(files)-1):
		# 		if(list(c_array[str(i+j)].keys())[0]==med_frame):
		# 			x1,y1,x2,y2 = c_array[str(i+j)][med_frame]
		# 			cv2.line(my_img,(x1, y1),(x2,y2),(0,0,255),2)
		# 			cv2.imwrite(os.path.join(o_path ,img_name),my_img)
		# 			break


	for i in range(len(files)-window,len(files)):
		img_name=files[i]
		my_img = cv2.imread('Frames/'+img_name)
		cv2.line(my_img,(m_array['x1'][i], m_array['y1'][i]),(m_array['x2'][i],m_array['y2'][i]),(0,0,255),3)
		cv2.imwrite(os.path.join(o_path ,img_name),my_img)









