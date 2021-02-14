from getter.video import VideoGetter
from getter.objdet import ObjDetGetter
from sender.posedet import PoseDetSender
from provider.posedet import PoseDetProvider
import json

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["posedet"]
with open("config.json","r",encoding="utf8") as f:
	videocfg = json.load(f)["video"]
with open("config.json","r",encoding="utf8") as f:
	objdetcfg = json.load(f)["objdet"]

vgt = VideoGetter(
	(videocfg["location"].split(":")[0],int(videocfg["location"].split(":")[1]))
).configure(
	resol = (
		min(videocfg["max-resolution"][0],config["video-resolution"][0]),
		min(videocfg["max-resolution"][1],config["video-resolution"][1])
	),
	qual = min(config["video-quality"],videocfg["max-quality"])
).start()

odg = ObjDetGetter(
	hostport = (objdetcfg["location"].split(":")[0],int(objdetcfg["location"].split(":")[1]))
).configure(
	fullscore = 1000,
	resolution = (640,480)
).start()

pds = PoseDetSender(
	hostport=("",int(config["location"].split(":")[1]))
).start()

pdp = PoseDetProvider(0)

while 1:
	try:
		tstp1, lst = odg.pull(-1)
		tstp2, img = vgt.pull(tstp1)
		boxes = []
		for i in lst:
			if i[0] == "person":
				boxes.append(i[2])
		result = pdp.processFrame(img, boxes)
		pds.push(tstp2,list(zip(boxes,result)))
	except KeyboardInterrupt as e:
		print(e)
		pds.stop()
		vgt.stop()
		odg.stop()
		exit(0)
