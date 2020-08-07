import cv2
import os

#BACKGROUND SUBTACTION ON THE EXTRACTED FRAMES
'''
METHOD 1 : Gaussian Mixture-based Background/Foreground Segmentation Algorithm
This models each background pixel by a mixture of K Gaussian distributions (K = 3 to 5). 
One important feature of this algorithm is that it selects the appropriate number of 
gaussian distribution for each pixel and not a simgle combination throughout the image. 
The weights of the mixture represent the time proportions that those colours stay 
in the scene. The probable background colours are the ones which stay longer and more static.
'''

def BgSubtract(video,fps,varThreshold):
    #HEHEHEHHEHEHEHEHEEHEH

    w_path = './Background-Subtraction-Frames'
    #history=10*fps,detectShadows=True,varThreshold = varThreshold
    r_path = 'Frames'
    Subtraction_MOG = cv2.createBackgroundSubtractorMOG2(history=10*fps,detectShadows=True,varThreshold = varThreshold)   #history=10*fps,nmixtures=10, backgroundRatio=0.7

    #history= 4*fps, detectShadows=True, varThreshold = 400
    for img_name in os.listdir(r_path):

        if not img_name.endswith(video+'.jpg'):
            continue
        frame = cv2.imread(r_path+'/'+img_name)
        Image_foreground = Subtraction_MOG.apply(frame)
        Image_foreground[Image_foreground==127]=0
        # ret,Image_foreground = cv2.threshold(img,128,255,cv2.THRESH_BINARY)
        # print(Image_foreground)
        cv2.imwrite(os.path.join(w_path ,img_name),Image_foreground)
        #fg = cv2.copyTo(frame,Image_foreground)
        # cv2.namedWindow('Coloured Foreground',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Coloured Foreground', 600,600)
        # cv2.imshow('Coloured Foreground',fg)

        # myvideo.write(fg)

        # cv2.namedWindow('Foreground',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Foreground', 600,600)
        # cv2.imshow('Foreground',Image_foreground)
        
        

        # cv2.namedWindow('Background',cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Background', 600,600)
        # cv2.imshow('Background',cv2.copyTo(frame,cv2.bitwise_not(Image_foreground)))
        # cv2.waitKey(30)
        # video_frame.release()
        # cv2.destroyAllWindows()



