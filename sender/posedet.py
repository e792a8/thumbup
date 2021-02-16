from sender.basesender import BaseSender

class PoseDetSender(BaseSender):

	def configure(self):
		return self

	def processClient(self, client, addr):

		while self.running:	#LOOP
			req = self.recvPack(client, "!q")	#REQ tstp
			tstp, frame = self.seekFrame(req[0])
			# [((box),[pose]),...]
			self.sendPack(client, "!ql", (tstp, len(frame)))	#RESP tstp num

			for i in frame:
				self.sendPack(client, "!4f34f", (*i[0],*(k for j in i[1] for k in j)))	#RESP box pose
