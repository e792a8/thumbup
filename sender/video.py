import socket
import threading
import struct
import cv2 as cv
import time
import os
import numpy


class VideoSender:

	def __init__(self, port=7778, maxresol=(640, 480), maxqual = 30):
		self.max_resolution = maxresol
		self.max_img_quality = maxqual
		self.host = ("", port)
		self.setSocket(self.host)
		self.framebuffer = (-1,None)
		self.mutex = threading.Lock()
		self.running = False

	def push(self, timestamp, frame):
		self.mutex.acquire()
		self.framedata = (timestamp, frame)
		self.mutex.release()

	def setSocket(self, host):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.host)
		self.socket.listen(5)
		print("Server running on port %d" % host[1])

	def _processConnection(self, client, addr):

		try:
			info = struct.unpack("!lhh", client.recv(struct.calcsize("!lhh")))	#RECV quality+911 width height
		except:
			client.close()
			return
		if info[0] > 911:
			img_quality = min(info[0]-911,self.max_img_quality)
			resolution = tuple(min(info[1],self.max_resolution[0]),min(info[2],self.max_resolution[1]))
			encode_param = [int(cv.IMWRITE_JPEG_QUALITY), img_quality]
		else:
			client.close()
			return
		client.send(struct.pack("!lhh", img_quality+911, resolution[0], resolution[1]))	#SEND quality+911 width height

		print("Connection from %s:%d" % (addr[0], addr[1]))
		print("Resolution: %d * %d" % (resolution[0], resolution[1]))
		print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

		while self.running:	#LOOP

			try:
				request = client.recv(struct.calcsize("!q"))	#RECV reqtstp
			except:
				client.close()
				print("%s:%d disconnected" % (addr[0], addr[1]))
				print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
				return
			reqtstp = struct.unpack("!q",request)[0]

			while self.running:
				self.mutex.acquire()
				timestamp = self.framedata[0]
				self.mutex.release()
				if timestamp >= reqtstp:
					break
				time.sleep((reqtstp-timestamp)/1000)

			self.mutex.acquire()
			timestamp = self.framedata[0]
			img = self.framedata[1]
			self.mutex.release()
			img = cv.resize(img, resolution)
			result, imgencode = cv.imencode('.jpg', img, encode_param)
			imgdata = numpy.array(imgencode).tostring()

			try:
				client.send(struct.pack("!lq", len(imgdata), timestamp) + imgdata)	#SEND length timestamp data
			except:
				client.close()
				print("%s:%d disconnected" % (addr[0], addr[1]))
				print("At %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
				return

	def _processListening(self):
		while self.running:
			try:
				client, addr = self.socket.accept()
				clientThread = threading.Thread(target=self._processConnection, args=(client, addr))
				clientThread.start()
			except:
				print("Listening failure")

	def start(self):
		self.running = True
		self.listeningThread = threading.Thread(target=self._processListening)
		self.listeningThread.start()
		return self

	def stop(self):
		self.running = False
		self.socket.close()

'''
def main():
	cam = Sender()
	cam.run()


if __name__ == "__main__":
	main()
'''