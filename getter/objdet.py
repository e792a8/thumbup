import socket
from getter.basegetter import BaseGetter

class ObjDetGetter(BaseGetter):

	def configure(self, fullscore = 1000, resolution = (640,480)):
		return self

	def connect(self):
		self.sendRaw(b"!hhh")	#SEND handshake
		resp = self.recvRaw(4)	#RECV handshake

	def recvData(self, timestamp):
		result = self.sendPack("!q", (timestamp,))	#SEND reqtstp
		info = self.recvPack("!ql")	#RECV timestamp number
		tstp = info[0]
		num = info[1]
		buffer = []
		for i in range(num):
			data = self.recvPack("!fffffh")	#RECV score (box) len(name)
			name = self.recvRaw(data[5]).decode("utf8")	#RECV name
			buffer.append((name,data[0],data[1:5]))
		self.dataframe = (tstp,buffer)