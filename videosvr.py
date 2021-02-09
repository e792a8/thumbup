from sender import video
import cv2 as cv
import json
import time

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["video"]

vsd = video.VideoSender(
	hostport = ("",int(config["location"].split(":")[1]))
).configure(
	maxresol = tuple(config["max-resolution"]),
	maxqual = config["max-quality"]
).start()

try:
	cap = cv.VideoCapture(0)
	while 1:
		result = cap.read()
		if result[0]:
			vsd.push(int(1000*time.time()), result[1])
		time.sleep(0.005)
except KeyboardInterrupt as e:
	print("Keyboard interruption")
	cap.release()
	vsd.stop()