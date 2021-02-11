import socket
from getter.basegetter import BaseGetter

class ObjDetGetter(BaseGetter):

	def configure(self, fullscore = 1000, resolution = (640,480)):
		self.fullscore = fullscore
		self.resolution = resolution
		return self

	def connect(self):
		self.sendPack("!hhh", (self.fullscore,*self.resolution))	#SEND fullscore w h
		resp = self.recvPack("!hhh")	#RECV fullscore w h
		self.fullscore = resp[0]
		self.resolution = resp[1:3]

	def recvData(self, timestamp):
		result = self.sendPack("!q", (timestamp,))	#SEND reqtstp
		info = self.recvPack("!ql")	#RECV timestamp number
		tstp = info[0]
		num = info[1]
		buffer = []
		for i in range(num):
			data = self.recvPack("!hhhhhh")	#RECV score (box) len(name)
			name = self.recvRaw(data[5]).decode("utf8")	#RECV name
			buffer.append((name,data[0],data[1:5]))
		self.dataframe = (tstp,buffer)