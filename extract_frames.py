import cv2
import os

def ExtractFrames(video):
	# Opens the Video file
	r_path='Videos/'+video+'.mp4'
	video_frame = cv2.VideoCapture(r_path)
	w_path = './Frames'

	#Number of frames per second (fps) and number of frames that will be extracted
	fps = video_frame.get(cv2.CAP_PROP_FPS)
	print("Frames per second : {0}".format(fps))
	No_of_frames = int(video_frame.get(cv2.CAP_PROP_FRAME_COUNT))
	print("Number of frames: ", No_of_frames)

	#Extract video frames
	i=0
	while(True):
	    success , frame = video_frame.read()
	    if not success:
	    	break
	    cv2.imwrite(os.path.join(w_path ,'Frame'+str(i)+'_'+video+'.jpg'),frame)		#Save the Image frames to this location
	    i+=1
	return fps