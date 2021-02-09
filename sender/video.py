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

		try:
			info = self.recvPack(client, "!lhh")	#RECV quality+911 width height
		except:
			self.killClient(client)
			return
		if info[0] > 911:
			img_quality = min(info[0]-911,self.max_img_quality)
			resolution = (min(info[1],self.max_resolution[0]),min(info[2],self.max_resolution[1]))
			encode_param = [int(cv.IMWRITE_JPEG_QUALITY), img_quality]
		else:
			self.killClient(client)
			return
		self.sendPack(client, "!lhh", (img_quality+911, resolution[0], resolution[1]))	#SEND quality+911 width height

		print("Connection from %s:%d" % (addr[0], addr[1]))
		print("Resolution: %d * %d" % (resolution[0], resolution[1]))
		print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

		while self.running:	#LOOP

			try:
				reqtstp = self.recvPack(client, "!q")[0]	#RECV reqtstp
			except:
				self.killClient(client)
				print("%s:%d disconnected" % (addr[0], addr[1]))
				print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
				return

			while self.running:
				self.mutex.acquire()
				timestamp = self.dataframe[0]
				self.mutex.release()
				if timestamp >= reqtstp:
					break
				time.sleep(min(500, reqtstp-timestamp)/1000)

			self.mutex.acquire()
			timestamp = self.dataframe[0]
			img = self.dataframe[1]
			self.mutex.release()
			img = cv.resize(img, resolution)
			result, imgencode = cv.imencode('.jpg', img, encode_param)
			imgdata = numpy.array(imgencode).tostring()

			try:
				self.sendPack(client, "!lq", (len(imgdata), timestamp))	#SEND length timestamp
				client.send(imgdata)
			except:
				self.killClient(client)
				print("%s:%d disconnected" % (addr[0], addr[1]))
				print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
				return
