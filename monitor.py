import time
import json
import cv2 as cv
from getter.video import VideoGetter

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["monitor"]
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

tstp = int(time.time()*1000)
print(tstp,"<<<")
try:
	while 1:
		tstp, frame = vgt.pull(-1)
		print(tstp)
		cv.imshow("video",frame)
		if cv.waitKey(1) == ord('q'):
			break
		time.sleep(0.05)
except KeyboardInterrupt as e:
	print("Keyboard interrupt")
	cv.destroyAllWindows()
	vgt.stop()
	exit(0)
