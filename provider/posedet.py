import cv2
import tensorflow as tf
import numpy as np

imageSize = 257
width = imageSize
height = imageSize

def load_model(PATH_TO_CKPT):
	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.compat.v1.GraphDef()
		with open(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')
	return detection_graph

tf.compat.v1.disable_eager_execution()
detection_graph = load_model("provider/posedet_frozen_model.pb")
detection_graph.as_default()
sess = tf.compat.v1.Session(graph=detection_graph)
image = detection_graph.get_tensor_by_name('image:0')
heatmaps=detection_graph.get_tensor_by_name('heatmap:0')
offsets=detection_graph.get_tensor_by_name('offset_2:0')
displacementFwd=detection_graph.get_tensor_by_name('displacement_fwd_2:0')
displacementBwd=detection_graph.get_tensor_by_name('displacement_bwd_2:0')

def adapt_img(img, width, height):

	img = cv2.resize(img, (width,height))
	img = img.astype(float)
	img = img*2.0/255.0-1.0
	return img

def detect_single(img):
	input_image = adapt_img(img,width,height)
	input_image = np.array(input_image,dtype=np.float32)
	input_image = input_image.reshape(1,width,height,3)
	heatmaps_result,offsets_result,displacementFwd_result,displacementBwd_result = sess.run(
			[heatmaps,offsets,displacementFwd,displacementBwd], feed_dict={ image: input_image } )
	heatmaps_result = heatmaps_result[0]
	offsets_result=offsets_result[0]
	aaaa= np.transpose(heatmaps_result,(2, 0, 1))
	bbb= np.transpose(offsets_result,(2, 0, 1))
	keypoint = []
	for k in range(17):
		heatmaps_result=aaaa[k]
		maxheat=np.max(heatmaps_result)
		re=np.where(heatmaps_result==maxheat)
		ry=re[0][0]
		rx=re[1][0]
		offsets_resulty=bbb[0+k]
		offsets_resultx=bbb[17+k]
		ofx=int(offsets_resultx[ry][rx]+0.5)
		ofy=int(offsets_resulty[ry][rx]+0.5)
		px=((rx)*16+ofx)/width
		py=((ry)*16+ofy)/height
		if maxheat>0.7:
			keypoint.append((px,py))
		else:
			keypoint.append((-1.0,-1.0))

	return keypoint
	# [0:nose 1:leye 2:reye 3:lear 4:rear 5:lshoulder 6:rshoulder 7:lelbow 8:relbow
	#  9:lwrist 10:rwrist 11:lwaist 12:rwaist 13:lknee 14:rknee 15:lankle 16:rankle]

class PoseDetProvider:
	def __init__(self,arg):
		pass
	def processFrame(self,img,boxes):
		h,w,_ = img.shape
		res = []
		for i in boxes:
			res.append(detect_single(img[int(h*i[1]):int(h*i[3]),int(w*i[0]):int(w*i[2])]))
		return res
		# [0:nose 1:leye 2:reye 3:lear 4:rear 5:lshoulder 6:rshoulder 7:lelbow 8:relbow
		#  9:lwrist 10:rwrist 11:lwaist 12:rwaist 13:lknee 14:rknee 15:lankle 16:rankle]
