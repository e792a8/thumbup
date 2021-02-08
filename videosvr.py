from sender import video
import cv2 as cv
import json
import time

config = {}
with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)

vsd = video.VideoSender(
	port=int(config["video.location"].split(":")[1]),
	maxresol=tuple(config["video.max-resolution"]),
	maxqual = config["video.max-quality"]
).start()

cap = cv.VideoCapture(0)
while 1:
	result = cap.read()
	if result[0]:
		vsd.push(int(1000*time.time()), result[1])
