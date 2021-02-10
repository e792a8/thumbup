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
		try:
			self.socket.send(data)
		except:
			print("Send failing")
			return False
		return True

	def recvRaw(self, length):
		data = b""
		tmp = length
		try:
			while tmp > 0:
				data += self.socket.recv(tmp)
				tmp = length - len(data)
		except:
			print("Recv failing")
			return False
		return data

	def sendPack(self, format, lst):
		result = self.sendRaw(struct.pack(format, *lst))
		return result

	def recvPack(self, format):
		raw = self.recvRaw(struct.calcsize(format))
		if raw == False:
			return False
		return struct.unpack(format, raw)

	def start(self):
		self.startSocket()
		self.connect()
		return self

	def stop(self):
		self.socket.close()

	def pull(self, timestamp):
		if timestamp == -1:
			self.recvData(-1)
		elif(self.dataframe[0] < timestamp):
			self.recvData(timestamp)
		return self.dataframe

	def configure(self):
		return self
		pass

	def connect(self):
		pass

	def recvData(self, timestamp):
		pass
