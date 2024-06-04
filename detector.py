import os
import cv2
import matplotlib.pyplot as plt
import torch
# Darknet object detector imports.
import darknet
from darknet_images import load_images
from darknet_images import image_detection

def detect(inp_img,config,data,weights,threshold,output,network,classnames,classcolors,output_path=''):

  #resizing image to darknet accepted width and height
  w=darknet.network_width(network)
  h=darknet.network_height(network)
  #dummy image to convert to bytes later
  darknet_image = darknet.make_image(w, h, 3)
  img_rgb = cv2.cvtColor(inp_img,cv2.COLOR_BGR2RGB)
  img_resize = cv2.resize(img_rgb,(w, h))

  darknet.copy_image_from_bytes(darknet_image, img_resize.tobytes())
  detect = darknet.detect_image(network, classnames, darknet_image, thresh=threshold)
  darknet.free_image(darknet_image)
  print(detect)
  classes = []
  for i in detect:
    classes.append(i[0])
  print(classes)

  image=darknet.draw_boxes(detect,img_resize,classcolors)

  img=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
  filename=output_path + 'det.jpg'
  cv2.imwrite(os.path.join(output,filename),img)

  #resizing to input image res
  outsize=inp_img.shape[:2]
  insize=img_resize.shape[:2]
  coord, scores = resize(detect,outsize,insize)
  return coord, scores,classes

def resize(detections, outsize,insize):
  coord =[]
  scores=[]

  for det in detections:
    points = list(det[2])
    conf = det[1]

    xmin, ymin, xmax, ymax =  darknet.bbox2points(points)
    y_scale = float(outsize[0]) / insize[0]
    x_scale = float(outsize[1]) / insize[1]
    ymin = int(y_scale * ymin)
    ymax = int(y_scale * ymax)
    xmin = int(x_scale * xmin) if int(x_scale * xmin) > 0 else 0
    xmax = int(x_scale * xmax)

    final_points = [xmin, ymin, xmax-xmin, ymax-ymin]
    scores.append(conf)
    coord.append(final_points)

  return coord, scores

def test_img(img,config,weights,outpath):
  network, cnames,ccolours = darknet.load_network(config,data,weights,batch_size=1)
  ccolours = {'Vehicle_registration_plate': (255,0,0)} 
  bboxes, scores, classes = detect(img,config,data,weights,thresh,outpath,network,cnames,ccolours)
  
  for bbox in bboxes:
    bbox = [bbox[0], bbox[1], bbox[2]- bbox[0], bbox[3] - bbox[1]]
  return bboxes,classes

def License_test(img):
  
  bboxes,classes = test_img(img,config,weights,outpath)
  return bboxes, classes
config='./darknet/cfg/yolov4-obj.cfg'
data = './darknet/data/obj.data'
batch_size = 1
weights = './darknet/yolov4-obj_best.weights'
thresh = 0.6
outpath = ''