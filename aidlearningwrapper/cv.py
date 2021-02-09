from cvs import *

class VideoCapture:
	def __init__(self, arg):
		self.realcap = cvs.VideoCapture(arg)
	def read(self):
		return (True, self.realcap.read())
	def release(self):
		pass

imencode = cv2.imencode

imdecode = cv2.imdecode

IMWRITE_JPEG_QUALITY = cv2.IMWRITE_JPEG_QUALITY

resize = cv2.resize