import time
import json
import cv2 as cv
from getter.video import VideoGetter

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["video"]

vgt = VideoGetter(
	(config["location"].split(":")[0],int(config["location"].split(":")[1]))
).configure(
	resol = (640,480),
	qual = 15
).start()

tstp = -1
try:
	while 1:
		tstp += 1
		tstp, frame = vgt.pull(tstp)
		cv.imshow("video",frame)
		time.sleep(1)
except KeyboardInterrupt as e:
	print("Keyboard interrupt")
	cv.destroyAllWindows()
	vgt.stop()