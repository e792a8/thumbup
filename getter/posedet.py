from getter.basegetter import BaseGetter

class PoseDetGetter(BaseGetter):
	
	def configure(self):
		return self

	def connect(self):
		self.sendRaw(b"!hhh")	#REQ handshake
		resp = self.recvRaw(4)	#RESP handshake

	def recvData(self, timestamp):
		self.sendPack("!q",(timestamp,))	#REQ tstp
		resp = self.recvPack("!ql")	#RESP tstp num
		tstp = resp[0]
		num = resp[1]
		buffer = []

		for i in range(num):
			resp = self.recvPack("!4f34f")	#RESP box pose
			lst = resp[4:]
			buffer.append((tuple(resp[0:4]),[(lst[x],lst[x+1]) for x in range(0,34,2)]))
		self.dataframe = (tstp, buffer)
