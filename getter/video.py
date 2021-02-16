import socket
import numpy
import cv2 as cv
from getter.basegetter import BaseGetter

class VideoGetter(BaseGetter):

	def configure(self, resol, qual):
		self.resolution = resol
		self.quality = qual
		return self

	def recvData(self, timestamp, req):
		result = self.sendPack("!qlhh",(timestamp,self.quality,self.resolution[0],self.resolution[1]))	#SEND reqtstp quality width height
		info = self.recvPack("!lq")	#RECV length timestamp image
		buffer = self.recvRaw(info[0])
		self.dataframe = (info[1],cv.imdecode(numpy.fromstring(buffer,dtype='uint8'),cv.IMREAD_COLOR))
