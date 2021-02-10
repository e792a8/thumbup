import socket
import numpy
import cv2 as cv
from getter.basegetter import BaseGetter

class VideoGetter(BaseGetter):

	def configure(self, resol, qual):
		self.resolution = resol
		self.quality = qual
		return self

	def connect(self):
		self.sendPack("!lhh",(self.quality,self.resolution[0],self.resolution[1]))	#SEND quality width height
		resp = self.recvPack("!lhh")	#RECV quality width height
		self.quality = resp[0]
		self.resolution = (resp[1],resp[2])
		return self

	def recvData(self, timestamp):
		result = self.sendPack("!q",(timestamp,))	#SEND reqtstp
		info = self.recvPack("!lq")	#RECV length timestamp image
		buffer = self.recvRaw(info[0])
		self.dataframe = (info[1],cv.imdecode(numpy.fromstring(buffer,dtype='uint8'),cv.IMREAD_COLOR))
