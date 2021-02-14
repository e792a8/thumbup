import time, sys
import cv2
import os
import time
import numpy as np
import tensorflow as tf


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
		out.append((i[1],i[0],i[3],i[2])) # l u r d
	return out


class_names = read_classes('provider/objdet_coco_classes.txt')
model_path="provider/objdet_ssdlite_mobilenet_v3.tflite"
inShape =[1 * 300 * 300 *3,]
outShape= [1 * 10*4*4,1*10*4,1*10*4,1*4]
input_shape=[300,300]

tflite = tf.lite.Interpreter(model_path = model_path)
tflite.allocate_tensors()
output_details = tflite.get_output_details()
print(str(output_details))

def run_detection(image):
	tflite.set_tensor(175,image)
	tflite.invoke()
	classes = tflite.get_tensor(168)
	scores = tflite.get_tensor(169)
	num = tflite.get_tensor(170)
	box = tflite.get_tensor(167).reshape((10,4)) # u l d r
	box, scores, classes = np.squeeze(box), np.squeeze(scores), np.squeeze(classes + 1).astype(np.int32)
	out_scores, out_boxes, out_classes = non_max_suppression(scores, box, classes)
	out_classes = [class_names[i] for i in out_classes]
	return out_scores, out_boxes, out_classes

def once_object_detection(frame):
	h,w,_ = frame.shape
	image_data = preprocess_image_for_tflite_uint8(frame, model_image_size=300)
	out_scores, out_boxes, out_classes = run_detection(image_data)
	out_boxes = box_reshape(out_boxes,h,w)
	preresult = list(zip(out_classes, out_scores, out_boxes))
	result = []
	for i in preresult:
		x = list(i[2])
		if x[0]<x[2] and x[1]<x[3]:
			for j in range(4):
				if x[j]<0.0:
					x[j] = 0.0
				elif x[j]>1.0:
					x[j] = 1.0
			result.append((i[0],i[1],tuple(x)))
	return result

class ObjDetProvider:
	def __init__(self, arg):
		pass
	def processFrame(self, img):
		result = once_object_detection(img)
		return result # [(class, score, (box)), ...]

if __name__ == "__main__":
	cap = cv2.VideoCapture(0)
	try:
		while 1:
			print(once_object_detection(cap.read()[1]))
	except:
		cap.release()