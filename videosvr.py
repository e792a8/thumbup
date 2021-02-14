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
			tstp = int(1000*time.time())
			vsd.push(tstp, result[1])
			print(tstp)
		time.sleep(0.02)
except KeyboardInterrupt as e:
	print("Keyboard interrupt")
	vpd.stop()
	vsd.stop()
	exit(0)
