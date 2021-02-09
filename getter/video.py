import socket
import numpy
import cv2 as cv
from getter.basegetter import BaseGetter

class VideoGetter(BaseGetter):

	def configure(self, resol, qual):
		self.resolution = resol
		self.quality = qual
		return self

	def connect(self):
		self.sendPack("!lhh",(self.quality+911,self.resolution[0],self.resolution[1]))	#SEND quality+911 width height
		resp = self.recvPack("!lhh")	#RECV quality+911 width height
		if resp[0] > 911:
			self.quality = resp[0]-911
			self.resolution = (resp[1],resp[2])
		else:
			raise Exception("Not a valid server")
		return self

	def recvData(self, timestamp):
		self.sendPack("!q",(timestamp,))	#SEND reqtstp
		info = self.recvPack("!lq")	#RECV length timestamp image
		buffer = self.recvRaw(info[0])
		self.dataframe = (info[1],cv.imdecode(numpy.fromstring(buffer,dtype='uint8'),cv.IMREAD_COLOR))

	def pull(self, timestamp):
		while self.dataframe[0] < timestamp:
			self.recvData(timestamp)
		return self.dataframe

'''
	def getData(self, interval):
		showThread=threading.Thread(target=self._processImage);
		showThread.start();
	def setWindowName(self, name):
		self.name = name;
	def setRemoteAddress(self, remoteAddress):
		self.remoteAddress = remoteAddress;
	def _savePicToLocal(self, interval):
		while(1):
			try:
				self.mutex.acquire();
				path=os.getcwd() + "\\" + "savePic";
				if not os.path.exists(path):
					os.mkdir(path);
				cv.imwrite(path + "\\" + time.strftime("%Y%m%d-%H%M%S",
						time.localtime(time.time())) + ".jpg",self.image)
			except:
				pass;
			finally:
				self.mutex.release();
				time.sleep(interval);
	def check_config(self):
		path=os.getcwd()
		print(path)
		if os.path.isfile(r'%s\video_config.txt'%path) is False:
			f = open("video_config.txt", 'w+')
			print("w = %d,h = %d" %(self.resolution[0],self.resolution[1]),file=f)
			print("IP is %s:%d" %(self.remoteAddress[0],self.remoteAddress[1]),file=f)
			print("Save pic flag:%d" %(self.interval),file=f)
			print("image's quality is:%d,range(0~95)"%(self.img_quality),file=f)
			f.close()
			print("初始化配置");
		else:
			f = open("video_config.txt", 'r+')
			tmp_data=f.readline(50)#1 resolution
			num_list=re.findall(r"\d+",tmp_data)
			self.resolution[0]=int(num_list[0])
			self.resolution[1]=int(num_list[1])
			tmp_data=f.readline(50)#2 ip,port
			num_list=re.findall(r"\d+",tmp_data)
			str_tmp="%d.%d.%d.%d"%(int(num_list[0]),int(num_list[1]),int(num_list[2]),int(num_list[3]))
			self.remoteAddress=(str_tmp,int(num_list[4]))
			tmp_data=f.readline(50)#3 savedata_flag
			self.interval=int(re.findall(r"\d",tmp_data)[0])
			tmp_data=f.readline(50)#3 savedata_flag
			#print(tmp_data)
			self.img_quality=int(re.findall(r"\d+",tmp_data)[0])
			#print(self.img_quality)
			self.src=911+self.img_quality
			f.close()
			print("读取配置")
def main():
	print("创建连接...")
	cam = webCamConnect();
	cam.check_config()
	print("像素为:%d * %d"%(cam.resolution[0],cam.resolution[1]))
	print("目标ip为%s:%d"%(cam.remoteAddress[0],cam.remoteAddress[1]))
	cam.connect();
	cam.getData(cam.interval);
if __name__ == "__main__":
	main();
'''
