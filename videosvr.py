from sender.video import VideoSender
from provider.video import VideoProvider
import json
import time

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["video"]

vsd = VideoSender(
	hostport = ("",int(config["location"].split(":")[1]))
).configure(
	maxresol = tuple(config["max-resolution"]),
	maxqual = config["max-quality"]
).start()

try:
	vpd = VideoProvider(0)
	while 1:
		result = vpd.getFrame()
		if result[0]:
			vsd.push(int(1000*time.time()), cv.rotate(result[1],cv.ROTATE_90_COUNTERCLOCKWISE))
		time.sleep(0.005)
except KeyboardInterrupt as e:
	print("Keyboard interrupt")
	vpd.stop()
	vsd.stop()