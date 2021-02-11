from provider.objdet import ObjDetProvider
from sender.objdet import ObjDetSender
from getter.video import VideoGetter
import json
import time

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["objdet"]
with open("config.json","r",encoding="utf8") as f:
	videocfg = json.load(f)["video"]

vgt = VideoGetter(
	(videocfg["location"].split(":")[0],int(videocfg["location"].split(":")[1]))
).configure(
	resol = (
		min(videocfg["max-resolution"][0],config["video-resolution"][0]),
		min(videocfg["max-resolution"][1],config["video-resolution"][1])
	),
	qual = min(config["video-quality"],videocfg["max-quality"])
).start()

ods = ObjDetSender(
	hostport=("",config["location"].split(":")[1])
).configure(
	fullscore = 1000,
	resolution = tuple(config["video-quality"])
).start()

odp = ObjDetProvider(0)

try:
	while 1:
		tstp, img = vgt.pull(-1)
		result = odp.processFrame(img)
		ods.push(tstp,result)
		print(tstp,result)
except Exception as e:
	vgt.stop()
	print(e)
	exit(0)