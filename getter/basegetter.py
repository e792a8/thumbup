import socket
import struct
import time

class BaseGetter:

	def __init__(self, hostport = ("127.0.0.1",7778)):
		self.hostport = hostport
		self.dataframe = (-1,None)
		self.running = False

	def startSocket(self):
		self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.connect(self.hostport)

	def sendRaw(self, data):
		self.socket.send(data)

	def recvRaw(self, length):
		data = b""
		tmp = length
		while tmp > 0:
			data += self.socket.recv(tmp)
			tmp = length - len(data)
		return data

	def sendPack(self, format, lst):
		self.socket.send(struct.pack(format, *lst))

	def recvPack(self, format):
		return struct.unpack(format, self.socket.recv(struct.calcsize(format)))

	def start(self):
		self.startSocket()
		self.connect()
		return self

	def stop(self):
		self.socket.close()

	def pull(self, timestamp):
		if(self.dataframe[0] >= timestamp):
			return self.dataframe
		self.recvData(timestamp)

	def configure(self):
		return self
		pass

	def connect(self):
		pass

	def recvData(self, timestamp):
		pass
