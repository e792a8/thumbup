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

def objdetDrawBoxes(frame,lst):
	hgt,wdh,_ = frame.shape
	for i in lst:
		h = hash(i[0])
		blu = (int(i[2][0]*wdh),int(i[2][1]*hgt))
		brd = (int(i[2][2]*wdh),int(i[2][3]*hgt))
		colr = (127+(h%127),255-(h%133),127+(3*h%127))
		cv.rectangle(frame,blu,brd,colr,3)
		cv.putText(frame,i[0]+' '+str(int(1000*i[1])),(blu[0],blu[1]-9),cv.FONT_HERSHEY_SIMPLEX,0.5,colr,2)


tstp = int(time.time()*1000)
print(tstp,"<<<")
try:
	while 1:
		tstp, result = odg.pull(-1)
		result.reverse()
		tstp, frame = vgt.pull(tstp)
		objdetDrawBoxes(frame,result)
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
