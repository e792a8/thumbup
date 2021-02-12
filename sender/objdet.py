import socket
import threading
import struct
import time
from sender.basesender import BaseSender

class ObjDetSender(BaseSender):

	def configure(self, fullscore = 1000, resolution = (640,480)):
		return self

	def processClient(self, client, addr):
		result = self.recvRaw(client, 4)	#RECV fullscore w h
		self.sendRaw(client, b"!hhh")	#SEND fullscore w h
		
		while self.running:	#LOOP

			result = self.recvPack(client, "!q")	#RECV reqtstp
			timestamp, frame = self.seekFrame(result[0])
			num = len(frame)
			self.sendPack(client, "!ql", (timestamp, num))	#SEND timestamp number

			for i in frame:
				name = i[0].encode("utf8")
				self.sendPack(client, "!fffffh", (i[1], *i[2], len(name)))	#SEND score (box) len(name)
				self.sendRaw(client, name)	#SEND name
