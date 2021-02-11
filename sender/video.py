import socket
import threading
import struct
import time
import os
import numpy
from sender.basesender import BaseSender

try:
	from aidlearningwrapper import cv
except ImportError:
	import cv2 as cv

class VideoSender(BaseSender):

	def configure(self, maxresol, maxqual):
		self.max_resolution = maxresol
		self.max_img_quality = maxqual
		return self

	def processClient(self, client, addr):

		info = self.recvPack(client, "!lhh")	#RECV quality width height
		if info == False:
			self.killClient(client)
			return
		img_quality = min(info[0],self.max_img_quality)
		resolution = (min(info[1],self.max_resolution[0]),min(info[2],self.max_resolution[1]))
		encode_param = [int(cv.IMWRITE_JPEG_QUALITY), img_quality]
		self.sendPack(client, "!lhh", (img_quality, resolution[0], resolution[1]))	#SEND quality width height

		print("Connection from %s:%d" % (addr[0], addr[1]))
		print("Resolution: %d * %d" % (resolution[0], resolution[1]))
		print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

		while self.running:	#LOOP

			request = self.recvPack(client, "!q")	#RECV reqtstp
			if request == False:
				self.killClient(client)
				return
			reqtstp = request[0]

			timestamp, img = self.seekFrame(reqtstp)
			img = cv.resize(img, resolution)
			result, imgencode = cv.imencode('.jpg', img, encode_param)
			imgdata = numpy.array(imgencode).tostring()

			if (
				False == self.sendPack(client, "!lq", (len(imgdata), timestamp))	#SEND length timestamp image
				or False == self.sendRaw(client, imgdata)
			):
				self.killClient(client)
				return
