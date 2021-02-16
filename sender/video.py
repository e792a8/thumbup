import socket
import threading
import struct
import cv2 as cv
import time
import os
import numpy
from sender.basesender import BaseSender

class VideoSender(BaseSender):

	def configure(self, maxresol, maxqual):
		self.max_resolution = maxresol
		self.max_img_quality = maxqual
		return self

	def processClient(self, client, addr):
		encode_param = [int(cv.IMWRITE_JPEG_QUALITY), self.max_img_quality]

		while self.running:	#LOOP

			request = self.recvPack(client, "!qlhh")	#RECV reqtstp quality width height
			reqtstp = request[0]
			encode_param[1] = min(request[1],self.max_img_quality)
			resolution = (min(request[2],self.max_resolution[0]),min(request[3],self.max_resolution[1]))

			timestamp, img = self.seekFrame(reqtstp)
			img = cv.resize(img, resolution)
			result, imgencode = cv.imencode('.jpg', img, encode_param)
			imgdata = numpy.array(imgencode).tostring()

			self.sendPack(client, "!lq", (len(imgdata), timestamp))	#SEND length timestamp image
			self.sendRaw(client, imgdata)
