#!/usr/bin/env python

import cv2
import numpy as np
import base64
from time import sleep
    
class Camera:
    
    
    def __init__(self,ws):
        # Capture video from camera
        self.capture = cv2.VideoCapture(0)
        self.websocket = ws
    
    def run(self):
        videoFrame = self.capture.read()[1]
        videoFrameSize = videoFrame.shape
        
        # Capture cam image
        _,colourImage = self.capture.read()
        #blur image to remove false positives
        colourImage = cv2.GaussianBlur(colourImage, (5,5), 0)
        
        #create moving average image with depth 32
        movingAverageImage = np.float32(colourImage)
        #create grey image with depth 8
        greyImage = np.zeros(videoFrameSize, np.uint8)
        
        differenceImage = colourImage
        tempImage = colourImage
        
        
        while True:
            
            _,colourImage = self.capture.read()
            
            # smooth colour image to get rid of false negatives 
            colourImage = cv2.GaussianBlur(colourImage, (5,5), 0)
            
            cv2.accumulateWeighted(colourImage, movingAverageImage, 0.02)
            
            tempImage = cv2.convertScaleAbs(movingAverageImage)
            
            differenceImage = cv2.absdiff(colourImage, tempImage)
            
            #convert differenceImage to gray scale
            greyImage = cv2.cvtColor(differenceImage, cv2.COLOR_RGB2GRAY)
            
            #convert grayImage to binary black and white
            cv2.threshold(greyImage, 70, 255, cv2.THRESH_BINARY,greyImage)
            
            
            cv2.dilate(greyImage, None, greyImage, None, 18)
            cv2.erode(greyImage, None, greyImage, None, 10)
            
            contour,_ = cv2.findContours(greyImage, cv2.cv.CV_RETR_CCOMP, cv2.cv.CV_CHAIN_APPROX_SIMPLE)
            
            
            while contour:
                areas = [cv2.contourArea(c) for c in contour]
                max_index = np.argmax(areas)
                cnt=contour[max_index]
                x,y,w,h = cv2.boundingRect(cnt)
                contour.pop()
                cv2.rectangle(colourImage,(x,y),(x+w,y+h),(0,255,0),2)

            
            #cv2.imshow("Camera1",colourImage)
            
            #Send image through websocket
            #webImage = cv2.imencode('.png',colourImage)[1]
            #print "color image:"
            #print colourImage
            
            buf = [1,90]
            print webImage
            exit()
            cv2.imencode(".jpg", colourImage, buf)
            #print "print web image:"
            #print colourImage
            base64Image = base64.encodestring(colourImage)
            #print "base64 image"
            #print base64Image
            #ws.send(base64Image)
            self.websocket.send(base64Image)
            sleep(5)
            # Listen for ESC key
            c = cv2.waitKey(7) % 0x100
            if c == 27:
                break

        

