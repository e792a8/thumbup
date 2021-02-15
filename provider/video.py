try:
	from aidlearningwrapper import cv
except ImportError:
	import cv2 as cv

class VideoProvider:

	def __init__(self, arg):
		self.cap = cv.VideoCapture(arg)

	def getFrame(self):
		return cv.rotate(self.cap.read(),cv.ROTATE_90_COUNTERCLOCKWISE)

	def stop(self):
		self.cap.release()
