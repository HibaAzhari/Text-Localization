# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 18:07:04 2019

@author: Hiba Azhari, Nimue Wafiya
"""

import numpy as np
import cv2
from matplotlib import pyplot as pt


##  STAGE 1 : DILATION

test = cv2.imread("academic_journal_8.jpg",0)
[nrow,ncol] = test.shape
bi_img = np.zeros((nrow,ncol), dtype=np.uint8)

#cv2.imshow("Test",test)
#cv2.waitKey()
#cv2.destroyAllWindows()

hist = cv2.calcHist([test],[0],None,[256],[0,256])

threshold = 200
for x in range (0,nrow):
    for y in range( 0,ncol):
        if test[x,y] >= threshold:
            bi_img[x,y] = 0
        else:
            bi_img[x,y] = 255

sE = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
sE = sE.astype(np.uint8)

rSE=np.rot90(sE,2)

dilation_output = cv2.dilate(bi_img, rSE, iterations=4)

#fill gaps
sE_Two = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
sE_Two = sE_Two.astype(np.uint8)
closing_output = cv2.morphologyEx(dilation_output,cv2.MORPH_CLOSE,sE_Two)

#Display Outcome:

pt.figure
pt.subplot(121)
pt.title("Histogram of Grayscale Text Document")
pt.plot(hist)
pt.xlim([0,256])
pt.subplot(122)
pt.title("Binary Image After Performing Thresholding")
pt.imshow(bi_img,cmap="gray")
pt.show()



pt.figure()
pt.subplot(221)
pt.imshow(test, cmap="gray")
pt.title("Original Image")
pt.subplot(222)
pt.title("Grayscale Histogram of Test Image")
pt.xlabel("Bins")
pt.ylabel("Number of Pixels")
pt.plot(hist)
pt.xlim([0,256])
pt.subplot(223)
pt.imshow(bi_img, cmap="gray")
pt.title("After Threshold Test Image")
pt.subplot(224)
pt.imshow(closing_output , cmap="gray")
pt.title("Test Image After Dilation and Removing Noise")
pt.show()



##  STAGE 2 : LOCATION

#Initializing
top = 0 #represents top of text block
bottom = 0 #represents bottom of text block
coordinate_list = [] #2D list containing (top, bottom, left, right) edges of each block of text
lim = 5 #threshold number of empty pixels below block to determine that block has ended



def getCoordinates(top, bot):
    #Function takes topmost and bottommost edges of text block
    #Locates leftmost and rightmost edges of text block
    left = 0 # y coordinate of left edge of text block
    right = 0 # y coordinate of right edge of text block
    edge = 0 # temporary holder for right edge value
    for row in range(top,bot):
        if edge > right:
            right = edge
        edge = 0
        for col in range(ncol):
            if (left == 0): #if the block has not yet been reached
                if (closing_output[row,col] == 255): #if we find a white pixel
                    left = col
                    continue
            elif (closing_output[row,col] == 255): #if we find a white pixel after the first one
                edge = col #assign it edge value temporarily
                continue
            elif (closing_output[row,col] == 0) and col == ncol: #if we reach the edge of the page
                break
       
    return [top,bot,left,right]

##Get top and bottom of all paragraphs
c = 0
for row in range (nrow):
    for col in range (ncol):
        if (closing_output[row,col] == 255) and (top == 0):
            top = row
            break
        elif (top != 0):
            if (closing_output[row,col] == 255): 
                bottom = row 
                break 
            elif (c != lim) and (col == ncol-1):
                c += 1 
            elif (c == lim):
                coordinate_list.append(getCoordinates(top,bottom))
                top = 0
                bottom = 0
                c = 0
print(coordinate_list)

##Draw lines to demonstrate outcome
        
final = test.copy()
for i in range(len(coordinate_list)):
    top = coordinate_list[i][0]
    bot = coordinate_list[i][1]
    left = coordinate_list[i][2]
    right = coordinate_list[i][3]
    
    final[top,left:right] = 0
    final[bot,left:right] = 0
    final[top:bot,left] = 0
    final[top:bot,right] = 0
    
            
pt.figure()
pt.imshow(final, cmap = "gray")