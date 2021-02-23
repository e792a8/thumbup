import cv2 as cv
import time

start = 0.0

def local_video_timer(self):
	global start
	res, frame = self.cap.read()
	if not res:
		self.cap = cv.VideoCapture(self.vpath)
		start = int(time.time()*1000)
		res, frame = self.cap.read()
	while int(time.time()*1000)-start < self.cap.get(cv.CAP_PROP_POS_MSEC):
		pass
	return res, frame

def webcam(self):
	return self.cap.read()

class VideoProvider:

	def __init__(self, arg):
		global start
		self.cap = cv.VideoCapture(arg)
		if type(arg) is int:
			self.feed = webcam
		else:
			start = int(time.time()*1000)
			self.vpath = arg
			self.feed = local_video_timer

	def getFrame(self):
		return self.feed(self)

	def stop(self):
		self.cap.release()
