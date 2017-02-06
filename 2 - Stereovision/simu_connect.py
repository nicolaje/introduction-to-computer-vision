import pymorse

import base64
import numpy as np
import cv2
import time

left=np.array([])
right=np.array([])

# Callbacks to receive left and right images from the Robot stereo camera pair
def grabLeft(data):
    d2=[e for e in base64.b64decode(data['image'])]
    
    global left
    left=cv2.cvtColor(np.array(d2).reshape(data['height'],data['width'],4).astype(np.uint8),cv2.COLOR_RGBA2RGB)
    
def grabRight(data):
    d2=[e for e in base64.b64decode(data['image'])]
    
    global right
    right=cv2.cvtColor(np.array(d2).reshape(data['height'],data['width'],4).astype(np.uint8),cv2.COLOR_RGBA2RGB)
    
## Your settings
nmDisparities=32
blkSize=31

leftMx=np.genfromtxt('leftMx').astype(np.float32)#np.array([])#
leftMy=np.genfromtxt('leftMy').astype(np.float32)#np.array([])#
rightMx=np.genfromtxt('rightMx').astype(np.float32)#np.array([])#
rightMy=np.genfromtxt('rightMy').astype(np.float32)#np.array([])#

## From here, we start chatting with the simulator
with pymorse.Morse("localhost", 4000) as simu:
    try:
        robot=simu.robot
        cam_lft=robot.cam_left
        cam_lft.subscribe(grabLeft)
        cam_rght=robot.cam_right
        cam_rght.subscribe(grabRight)
        
        cond = True
        
        b_matcher=cv2.StereoBM_create(numDisparities=nmDisparities,blockSize=blkSize)
        
        # Loop as long as we don't press 'q' on a window
        while cond:
            if not left.size == 0 and not right.size == 0:
                cv2.imshow("Left",left)
                cv2.imshow("Right",right)
                
                if not leftMx.size == 0 and not rightMy.size == 0:
                    resLeft=cv2.remap(left,leftMx,leftMy,cv2.INTER_LINEAR).copy()
                    resRight=cv2.remap(right,rightMx,rightMy,cv2.INTER_LINEAR).copy()
                    
                    cv2.imshow("Res Left",resLeft)
                    cv2.imshow("Res Right",resRight)
                    resLeftGray=cv2.cvtColor(resLeft,cv2.COLOR_RGB2GRAY)
                    resRightGray=cv2.cvtColor(resRight,cv2.COLOR_RGB2GRAY)
                    
                    stereo=b_matcher.compute(resLeftGray,resRightGray).astype(np.float32)
                    cv2.imshow("disparity BM",stereo)
                    cv2.imshow("disparity normalized",cv2.normalize(stereo,None,alpha=0,beta=255,norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_8U))
                    
                if cv2.waitKey(10) == 113:
                    cond = False
    except:
        print("Something went wrong!")
        time.sleep(1)
        
cv2.destroyAllWindows()