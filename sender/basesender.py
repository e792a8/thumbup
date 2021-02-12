import threading
import struct
import time
import socket

class BaseSender:

	def __init__(self, hostport=("",7778), cachesize = 100):
		self.hostport = hostport
		self.setSocket(self.hostport)
		self.framecache = []
		self.cachesize = cachesize
		self.mutex = threading.Lock()
		self.running = False

	def seekFrame(self, timestamp):
		self.mutex.acquire()
		if timestamp == -1:
			result = self.framecache[-1]
			self.mutex.release()
			return result
		if timestamp > self.framecache[-1][0]:
			latest = self.framecache[-1][0]
			while self.running:
				self.mutex.release()
				time.sleep((timestamp-latest)/1000)
				self.mutex.acquire()
				latest = self.framecache[-1][0]
				if latest >= timestamp:
					result = self.dataframe[-1]
					self.mutex.release()
					return result
		l = 0
		r = len(self.framecache)-1
		while l < r:
			m = (l+r)//2
			if timestamp > self.framecache[m][0]:
				l = m + 1
			else:
				r = m
		result = self.framecache[m]
		self.mutex.release()
		return result

	def push(self, timestamp, frame):
		self.mutex.acquire()
		if len(self.framecache) >= self.cachesize:
			del self.framecache[0]
		self.framecache.append((timestamp, frame))
		self.mutex.release()

	def setSocket(self, host):
		self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listeningSocket.bind(self.hostport)
		self.listeningSocket.listen(5)
		print("Server running on port %d" % host[1])

	def recvRaw(self, client, length):
		data = b""
		tmp = length
		while tmp > 0:
			data += client.recv(tmp)
			tmp = length - len(data)
		return data

	def sendRaw(self, client, data):
		client.sendall(data)

	def recvPack(self, client, format):
		raw = self.recvRaw(client, struct.calcsize(format))
		return struct.unpack(format, raw)

	def sendPack(self, client, format, lst):
		self.sendRaw(client, struct.pack(format, *lst))

	def killClient(self, client):
		client.close()

	def _clientDaemon(self, client, addr):
		print("Connection from",addr)
		try:
			self.processClient(client, addr)
		except BaseException as e:
			print("Exception occured on client",addr)
			print(e)
		self.killClient(client)
		print(addr,"disconnected")
		return

	def _processListening(self):
		while self.running:
			try:
				client, addr = self.listeningSocket.accept()
				clientThread = threading.Thread(target=self._clientDaemon, args=(client, addr))
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
		self.listeningSocket.close()

	def configure(self):
		return self
		pass

	def processClient(self, client, addr):
		pass
