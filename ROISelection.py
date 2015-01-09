# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 17:28:42 2015

@author: Argentina Ortega Sáinz

Adapted from the code found at http://aroberge.blogspot.de/2014/11/practical-python-and-opencv-review-part_25.html
"""

import cv2
import copy

WIDTH = 640
HEIGHT = 480
SELECT_COLOUR = (255, 0, 0)  # blue
SAVE_COLOUR = (0, 255, 0)    # green
_x1 = _y1 = _x2=_y2 = 0
_original = _cropped = None
_clicked = False

img = 'images/images_rojo/c2_image00.png'
im = cv2.imread(img)
im1 = cv2.resize(im,(640,480))
im1 = cv2.GaussianBlur(im1,(5,5),0)

def init(original):    
    cv2.namedWindow('Original image')
    cv2.imshow('Original image', original)
    cropped = original[0:HEIGHT, 0:WIDTH]  #[y,x]
    cv2.namedWindow('Cropped')
    cv2.imshow("Cropped", cropped)
    return original, cropped


def paintROI(x, y,x2,y2, colour=SELECT_COLOUR):
    global _x1, _y1,_x2,_y2, _original, _cropped
    _x1, _y1, _x2, _y2 = x, y, x2, y2
    img = copy.copy(_original)
    cv2.rectangle(img, (x, y), (x2, y2), colour, 3)
    cv2.imshow('Original image', img)

def showCroppedImg():
    global _original, _cropped, _x1, _y1, _x2, _y2
    _cropped = _original[_y1:_y2,_x1:_x2]
    cv2.imshow("Cropped",_cropped)
    

def mouseROI(event, x, y, flags, param):
    global _clicked, _x1, _x2, _y1, _y2

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.destroyWindow("Cropped")
        _x1=x
        _y1=y
        _x2=x
        _y2=y
        _clicked = True
        #print "P1: %d  %d"%(_x1,_y1)
    elif event == cv2.EVENT_LBUTTONUP:
        _x2=x
        _y2=y
        _clicked = False
        #print "P2: %d  %d"%(_x2,_y2) 
        showCroppedImg()
    elif event == cv2.EVENT_MOUSEMOVE:
        if _clicked:
            _x2 = x
            _y2 = y

    if _clicked:
        paintROI(_x1, _y1,_x2,_y2)



def getROI(img):
    global _original, _cropped
    _original, _cropped = init(img)

    cv2.setMouseCallback('Original image', mouseROI)

    while True:
        key = cv2.waitKey(1) & 0xFF  
        if key == 27: 
            break
        elif key == ord("s"):
            return _x1, _y1, _x2, _y2
            
    cv2.destroyAllWindows()

if __name__ == '__main__':
    getROI(im1)