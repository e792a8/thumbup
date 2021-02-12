class ObjDetProvider:
	def __init__(self, arg):
		pass
	def processFrame(self, img):
		result = [("testing",0.666,(0.1,0.1,0.5,0.8))]
		return result # [(class, score, (box)), ...]
