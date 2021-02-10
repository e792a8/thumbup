import cv2 as cv

class VideoProvider:

	def __init__(self, arg):
		self.cap = cv.VideoCapture(arg)

	def getFrame(self):
		return self.cap.read()

	def stop(self):
		self.cap.release()
