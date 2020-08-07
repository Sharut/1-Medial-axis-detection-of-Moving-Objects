from extract_frames import *
from background_subtraction import *
from image_cleaning import *
from edge_detection import *
from hough import *
from save_video import *

for i in range(10):
	if(i!=1):
		continue
	video = str(i)
	fps=30

	print("converting video to frames ...")
	fps=int(ExtractFrames(video=video))

	print("\nrunning background subtraction ...")
	BgSubtract(video,fps=fps,varThreshold=22)

	print("\ncleaning all  frames ...")
	Cleaning(video,type="opening",kernel=3,structural="yes",size=150)

	print("\nrunning edge detector ...")
	EdgeDetection(video,type='canny',kernel=3)

	print("\nrunning hough transform ...")
	HoughTransform(video)
		
	print("\nsaving video ...")
	SaveVideo(video)