import time
import json
import cv2 as cv
from getter.video import VideoGetter
from getter.objdet import ObjDetGetter

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["monitor"]
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

tstp = int(time.time()*1000)
print(tstp,"<<<")
try:
	while 1:
		tstp, result = odg.pull(-1)
		tstp, frame = vgt.pull(tstp)
		print(tstp,result)
		cv.imshow("video",frame)
		if cv.waitKey(1) == ord('q'):
			break
		time.sleep(0.05)
except KeyboardInterrupt as e:
	print("Keyboard interrupt")
	cv.destroyAllWindows()
	vgt.stop()
	odg.stop()
	exit(0)
