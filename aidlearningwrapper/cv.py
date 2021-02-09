from cvs import *

class VideoCapture(cvs.VideoCapture):
	def read(self):
		return (True,super().read())

imencode = cv2.imencode

imdecode = cv2.imdecode

IMWRITE_JPEG_QUALITY = cv2.IMWRITE_JPEG_QUALITY

resize = cv2.resize