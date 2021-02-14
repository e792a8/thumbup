import time
import json
import cv2 as cv
from getter.video import VideoGetter
from getter.objdet import ObjDetGetter
from getter.posedet import PoseDetGetter

with open("config.json","r",encoding="utf8") as f:
	config = json.load(f)["monitor"]
with open("config.json","r",encoding="utf8") as f:
	videocfg = json.load(f)["video"]
with open("config.json","r",encoding="utf8") as f:
	objdetcfg = json.load(f)["objdet"]
with open("config.json","r",encoding="utf8") as f:
	posedetcfg = json.load(f)["posedet"]

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

pdg = PoseDetGetter(
	hostport = (posedetcfg["location"].split(":")[0],int(posedetcfg["location"].split(":")[1]))
).configure().start()

def objdetDrawBoxes(frame,lst):
	hgt,wdh,_ = frame.shape
	for i in lst:
		h = hash(i[0])
		blu = (int(i[2][0]*wdh),int(i[2][1]*hgt))
		brd = (int(i[2][2]*wdh),int(i[2][3]*hgt))
		colr = (127+(h%127),255-(h%133),127+(3*h%127))
		cv.rectangle(frame,blu,brd,colr,3)
		cv.putText(frame,i[0]+' '+str(int(1000*i[1])),(blu[0],blu[1]-9),cv.FONT_HERSHEY_SIMPLEX,0.5,colr,2)

def posedetDrawLines(frame,poses):
	fullh,fullw,_ = frame.shape
	colors = [[255, 0, 0], [255, 170, 0], [255, 170, 0],[255, 255, 0], [255, 255, 0], [170, 255, 0], [170, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 170], [0, 255, 170], [0, 170, 255], [0, 170, 255], [0, 0, 255], [0, 0, 255], [255, 0, 255], [255, 0, 255]]
	for i in poses:
		boxw = (i[0][2]-i[0][0])*fullw
		boxh = (i[0][3]-i[0][1])*fullh
		for k in range(17):
			if i[1][k][0] < 0:
				continue
			point = (int(fullw*i[0][0]+boxw*i[1][k][0]),int(fullh*i[0][1]+boxh*i[1][k][1]))
			cv.circle(frame, point, 3, colors[k], -1)

tstp = int(time.time()*1000)
print(tstp,"<<<")
try:
	while 1:
		tstp, presult = pdg.pull(-1)
		tstp, oresult = odg.pull(tstp)
		tstp, frame = vgt.pull(tstp)
		oresult.reverse()
		objdetDrawBoxes(frame,oresult)
		posedetDrawLines(frame,presult)
		cv.imshow("video",frame)
		if cv.waitKey(1) == ord('q'):
			break
		time.sleep(0.05)
except BaseException as e:
	print(e)
	cv.destroyAllWindows()
	vgt.stop()
	odg.stop()
	pdg.stop()
	exit(0)
