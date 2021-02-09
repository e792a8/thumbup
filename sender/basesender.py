import threading
import struct
import time
import socket

class BaseSender:

	def __init__(self, hostport=("",7778)):
		self.hostport = hostport
		self.setSocket(self.hostport)
		self.dataframe = (-1,None)
		self.mutex = threading.Lock()
		self.running = False

	def configure(self):
		return self
		pass

	def push(self, timestamp, frame):
		self.mutex.acquire()
		self.dataframe = (timestamp, frame)
		self.mutex.release()

	def setSocket(self, host):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(self.hostport)
		self.socket.listen(5)
		print("Server running on port %d" % host[1])

	def recvPack(self, client, format):
		return struct.unpack(format, client.recv(struct.calcsize(format)))

	def sendPack(self, client, format, lst):
		client.send(struct.pack(format, *lst))

	def killClient(self, client):
		client.close()

	def processClient(self, client, addr):
		client.close()
		pass

	def _processListening(self):
		while self.running:
			try:
				client, addr = self.socket.accept()
				clientThread = threading.Thread(target=self.processClient, args=(client, addr))
				clientThread.start()
			except:
				if self.running:
					print("Listening failure")

	def start(self):
		self.running = True
		self.listeningThread = threading.Thread(target=self._processListening)
		self.listeningThread.start()
		return self

	def stop(self):
		self.running = False
		self.socket.close()

