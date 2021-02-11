import time, sys
from cvs import *
import os
import time
import numpy as np
import tflite_gpu
tflite=tflite_gpu.tflite()


def read_classes(classes_path):
	with open(classes_path) as f:
		class_names = f.readlines()
	class_names = [c.strip() for c in class_names]
	return class_names
def preprocess_image_for_tflite_uint8(image, model_image_size=300):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image = cv2.resize(image, (model_image_size, model_image_size))
	image = np.expand_dims(image, axis=0)
	return image
def non_max_suppression(scores, boxes, classes, max_boxes=10, min_score_thresh=0.5):
	out_boxes = []
	out_scores = []
	out_classes = []
	if not max_boxes:
		max_boxes = boxes.shape[0]
	for i in range(min(max_boxes, boxes.shape[0])):
		if scores is None or scores[i] > min_score_thresh:
			out_boxes.append(boxes[i])
			out_scores.append(scores[i])
			out_classes.append(classes[i])
	out_boxes = np.array(out_boxes)
	out_scores = np.array(out_scores)
	out_classes = np.array(out_classes)
	return out_scores, out_boxes, out_classes
def box_reshape(boxes,h,w):
	out = []
	for i in boxes:
		out.append((int(i[1]*w),int(i[0]*h),int(i[3]*w),int(i[2]*h))) # l u r d
	return out


class_names = read_classes('provider/objdet_coco_classes.txt')
model_path="provider/objdet_ssdlite_mobilenet_v3.tflite"
inShape =[1 * 300 * 300 *3,]
outShape= [1 * 10*4*4,1*10*4,1*10*4,1*4]
print('gpu:',tflite.NNModel(model_path,inShape,outShape,4,0))
input_shape=[300,300]


def run_detection(image):
	tflite.setTensor_Int8(image,input_shape[0],input_shape[1])
	tflite.invoke()
	classes = tflite.getTensor_Fp32(1)
	scores = tflite.getTensor_Fp32(2)
	num = tflite.getTensor_Fp32(3)
	box = tflite.getTensor_Fp32(0).reshape((10,4)) # u l d r
	box, scores, classes = np.squeeze(box), np.squeeze(scores), np.squeeze(classes + 1).astype(np.int32)
	out_scores, out_boxes, out_classes = non_max_suppression(scores, box, classes)
	out_scores = [int(i*1000) for i in out_scores]
	out_classes = [class_names[i] for i in out_classes]
	return out_scores, out_boxes, out_classes

def once_object_detection(frame):
	h,w,_ = frame.shape
	image_data = preprocess_image_for_tflite_uint8(frame, model_image_size=300)
	out_scores, out_boxes, out_classes = run_detection(image_data)
	out_boxes = box_reshape(out_boxes,h,w)
	return list(zip(out_classes, out_scores, out_boxes))


class ObjDetProvider:
	def __init__(self, arg):
		pass
	def processFrame(self, img):
		result = once_object_detection(img)
		return result # [(class, score, (box)), ...]
