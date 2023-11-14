import cv2
import numpy as np
import streamlit as st

def blur_image(img,coords,darknetCoords = []):
    rect = img
    blurredImg = cv2.blur(rect, (21,21))
    mask = np.zeros(img.shape,dtype=np.uint8)
    for i in coords:
        cv2.rectangle(mask, [int(i[0][0]),int(i[0][1])],[int(i[2][0]),int(i[2][1])],(255,255,255),-1)

    for i in darknetCoords:
        cv2.rectangle(mask, [int(i[0]),int(i[1]),int(i[2]),int(i[3])],(255,255,255),-1)

    out = np.where(mask == (255,255,255),blurredImg, img)
    return out

def highlight_flags(img,coordList,darknetCoords):
    for i in coordList:
        cv2.rectangle(img, [int(i[0][0]),int(i[0][1])],[int(i[2][0]),int(i[2][1])],(0,0,255),3)
    for i in darknetCoords:
        cv2.rectangle(img, [int(i[0]),int(i[1]),int(i[2]),int(i[3])],(0,0,255),3)   
    #return highlightedImg
