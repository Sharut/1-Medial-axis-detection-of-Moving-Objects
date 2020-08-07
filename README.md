# Medial-axis-detection-of-Moving-Objects

The aim of this assignment is to get you familiarised with basic OpenCV
operations. Your task is to highlight the medial axis of the moving object in
the video clips given using OpenCV’s inbuilt operations.
• You can access the videos here.
• We’ll be working on the frames extracted from the video. Please refer to
the following example (https://www.geeksforgeeks.org/python-program-extract-frames-using-opencv/).
Once you get the frames, you should follow the below template - 


## 1.1 Background Subtraction
As the name suggests, background subtraction is the process of separating
out foreground objects from the background in a sequence of video frames.

![alt text](https://github.com/Sharut/1-Medial-axis-detection-of-Moving-Objects/blob/master/Images/fig1.png?raw=true)

![alt text](https://github.com/Sharut/1-Medial-axis-detection-of-Moving-Objects/blob/master/Images/fig2.png?raw=true)


## 1.2 Cleaning of image
The thus obtained background subtracted image may contain noise, imperfections etc. which should be cleaned to get a better picture of the moving
object in the foreground. Fundamental morphological image processing techniques like erosion, dilation etc. can be used for achieving the same.

## 1.3 Identification of edges and lines
The next step is to identify the edges in the cleaned image, which can be
done by using derivatives as covered in the class. Once you detect the edges,
you can identify the straight ones in them by using the Hough Line transforms
to get an image of the edges.

## 1.4 Medial axis identification
After getting the straight edges, you should compute the medial axis of the
object and highlight it on the original frame.
![alt text](https://github.com/Sharut/1-Medial-axis-detection-of-Moving-Objects/blob/master/Images/fig3.png?raw=true)
![alt text](https://github.com/Sharut/1-Medial-axis-detection-of-Moving-Objects/blob/master/Images/fig4.png?raw=true)
