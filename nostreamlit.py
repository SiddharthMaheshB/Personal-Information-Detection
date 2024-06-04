import checks
import ocr
import cv2
import numpy as np
import imgedit
import time

file = cv2.imread('image.jpg')
img = file
start = time.time()
text,ocrResults = ocr.Read_Image(img)

flagsList,darknetCoords,info = checks.main_check(text,img)
coordList = ocr.get_coords(flagsList,ocrResults)

blurImg = imgedit.blur_image(img,coordList,darknetCoords)
blurImg = cv2.cvtColor(blurImg,cv2.COLOR_BGR2RGB)

imgedit.highlight_flags(img,coordList,darknetCoords)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
end = time.time()

print((end-start)," s")
