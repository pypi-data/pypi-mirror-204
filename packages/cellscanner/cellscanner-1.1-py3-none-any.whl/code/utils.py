import json
import os.path
import shutil
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from yolov_res import detect, detect_yocls_01
from labelme_local import __main__ as labelme_main

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsPixmapItem, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor, QPen, QPixmap, QTransform, QImage
from PyQt5.QtCore import Qt, QRectF, QPointF, QRect, QEvent, QMimeData, QUrl, pyqtSignal as Signal, pyqtSlot as Slot, \
	QObject

import json
import os.path

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from yolov_res.model_cls import train as train_res
from yolov_res import detect, detect_yocls_01, train_2step, train_django
from labelme_local import __main__ as labelme_main
import expplot

def Yores_detect(
		source,
		yolo_weight,
		output_dir,
		resnet_weight=None,
		name='cache',
		save_txt=True,
):
	# 只用yolo
	yolo_weight = os.path.abspath(yolo_weight)
	if resnet_weight is not None:
		resnet_weight = os.path.abspath(resnet_weight)
	if resnet_weight is None:
		ROOT = detect.ROOT
		save_dir = detect.run(
			weights=yolo_weight,  # model.pt path(s)
			source=source,  # file/dir/URL/glob, 0 for webcam
			data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
			imgsz=(640, 640),  # inference size (height, width)
			conf_thres=0.4,  # confidence threshold
			iou_thres=0.4,  # NMS IOU threshold
			max_det=1000,  # maximum detections per image
			device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
			view_img=False,  # show results
			save_txt=save_txt,  # save results to *.txt
			save_conf=True,  # save confidences in --save-txt labels
			save_crop=False,  # save cropped prediction boxes
			nosave=True,  # do not save images/videos
			classes=None,  # filter by class: --class 0, or --class 0 2 3
			agnostic_nms=False,  # class-agnostic NMS
			augment=False,  # augmented inference
			visualize=False,  # visualize features
			update=False,  # update all models
			project=output_dir,  # save results to project/name
			name=name,  # save results to project/name
			exist_ok=True,  # existing project/name ok, do not increment
			line_thickness=1,  # bounding box thickness (pixels)
			hide_labels=True,  # hide labels
			hide_conf=False,  # hide confidences
			half=False,  # use FP16 half-precision inference
			dnn=False,  # use OpenCV DNN for ONNX inference
		)
	# both model used
	else:
		ROOT = detect_yocls_01.ROOT
		save_dir = detect_yocls_01.run(
			weight_path=None,
			weights_yolo=yolo_weight,
			source=source,
			weights_cls=resnet_weight,
			data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
			imgsz=(640, 640),  # inference size (height, width)
			conf_thres=0.4,  # confidence threshold
			iou_thres=0.4,  # NMS IOU threshold
			max_det=1000,  # maximum detections per image
			device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
			view_img=False,  # show results
			save_txt=save_txt,  # save results to *.txt
			save_conf=True,  # save confidences in --save-txt labels
			save_crop=False,  # save cropped prediction boxes
			nosave=True,  # do not save images/videos
			classes=None,  # filter by class: --class 0, or --class 0 2 3
			agnostic_nms=False,  # class-agnostic NMS
			augment=False,  # augmented inference
			visualize=False,  # visualize features
			update=False,  # update all models
			project=output_dir,  # save results to project/name
			name=name,  # save results to project/name
			exist_ok=True,  # existing project/name ok, do not increment
			line_thickness=1,  # bounding box thickness (pixels)
			hide_labels=True,  # hide labels
			hide_conf=False,  # hide confidences
			half=False,  # use FP16 half-precision inference
			dnn=False,  # use OpenCV DNN for ONNX inference
			save_summary=False
		)
	return save_dir


# read json file without 'imageData' in it
labelme_test_file_path = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/code/sample0307/cache03 jason/patch_2_23.json'
yolo_test_file_path = '/code/yolov_res/runs/detect/px1_0307_cache032/labels/patch_2_23.txt'


def read_labelme(filepath):
	with open(filepath, 'r') as f:
		data = json.load(f)
		data.pop('imageData')
		return data


# yolo txt to numpy array
def read_yolo(filepath):
	data = []
	for file in open(filepath):
		data.append([float(_) for _ in file[:-1].split(' ')])
	return data


# tansform polygon shapes in labelme_local data to rectangle
def labelmeshape2rectangle(labelme_shape):
	points = labelme_shape['points']
	x_min = min([_[0] for _ in points])
	x_max = max([_[0] for _ in points])
	y_min = min([_[1] for _ in points])
	y_max = max([_[1] for _ in points])
	labelme_shape['shape_type'] = 'rectangle'
	labelme_shape['points'] = [[x_min, y_min], [x_max, y_max]]
	return labelme_shape


# transform labelme_local data to yolo format
def labelme2yolo(labelme_data, label_list=None):
	# labelme_data = read_labelme(labelme_test_file_path)
	imgshape = [labelme_data['imageHeight'], labelme_data['imageWidth']]
	yolo_data = []
	for shape in labelme_data['shapes']:
		shape = labelmeshape2rectangle(shape)
		shape_type = shape['shape_type']
		points = shape['points']
		if label_list is not None:
			if shape['label'] not in label_list:
				label = '-1'
			else:
				label = str(label_list.index(shape['label']))
		else:
			# label = shape['label']
			label = str(-1)
		if shape_type == 'rectangle':
			# yolo format: x_center, y_center, width, height
			x_center = (points[0][0] + points[1][0]) / 2
			y_center = (points[0][1] + points[1][1]) / 2
			width = points[1][0] - points[0][0]
			height = points[1][1] - points[0][1]
			# refactor x,y from full size to ratio
			x_center /= imgshape[1]
			y_center /= imgshape[0]
			width /= imgshape[1]
			height /= imgshape[0]
			yolo_data.append([label, x_center, y_center, width, height])
	return yolo_data


# refactory yolo data from ratio to full size
def yolo2fullsize(list_data, imgshape=[770, 769]):
	for shape in list_data:
		shape[1] *= imgshape[1]
		shape[2] *= imgshape[0]
		shape[3] *= imgshape[1]
		shape[4] *= imgshape[0]
	return list_data


# transform yolo data to labelme_local format
def yolo2labelme(yolo_data, imgshape=[770, 769], path=None, label_list=None):
	# yolo_data = read_yolo(yolo_test_file_path)
	labelme_data = {}
	labelme_data['version'] = '4.6.0'
	labelme_data['flags'] = {}
	labelme_data['shapes'] = []
	labelme_data['imagePath'] = path
	labelme_data['imageData'] = None
	if path is None:
		path = 'cache.jpg'
		labelme_data['imageHeight'] = imgshape[0]
		labelme_data['imageWidth'] = imgshape[1]
	else:
		img = cv2.imread(path)
		labelme_data['imageHeight'] = img.shape[0]
		labelme_data['imageWidth'] = img.shape[1]
		imgshape = [img.shape[0], img.shape[1]]
	yolo_data = yolo2fullsize(yolo_data, imgshape)
	for yolo_shape in yolo_data:
		if label_list is not None:
			label = label_list[int(yolo_shape[0])]
		else:
			label = str(int(yolo_shape[0]))
		x_center = yolo_shape[1]
		y_center = yolo_shape[2]
		width = yolo_shape[3]
		height = yolo_shape[4]
		x_min = x_center - width / 2
		x_max = x_center + width / 2
		y_min = y_center - height / 2
		y_max = y_center + height / 2
		
		# #refactor x,y from ratio to full size
		# x_min *= imgshape[1]
		# x_max *= imgshape[1]
		# y_min *= imgshape[0]
		# y_max *= imgshape[0]
		#
		labelme_shape = {}
		labelme_shape['label'] = str(label)
		labelme_shape['flags'] = {}
		labelme_shape['group_id'] = None
		labelme_shape['shape_type'] = 'rectangle'
		labelme_shape['points'] = [[x_min, y_min], [x_max, y_max]]
		labelme_data['shapes'].append(labelme_shape)
	return labelme_data


# save labelme_local data to json file
def save_labelme(labelme_data, save_path):
	# check whether imageData in labelme_data
	if 'imageData' not in labelme_data.keys():
		labelme_data['imageData'] = None
	
	with open(save_path, 'w') as f:
		json.dump(labelme_data, f, indent=2)


def visualize_box_on_image(box_array, imgpath, label_list=None, show=False):
	'''

    Args:
        box_array: numpy array format [[label,x_start,y_start,width,height,...],...]
        imgpath:str, image path

    Returns:

    '''
	img = cv2.imread(imgpath)
	img_height, img_width = img.shape[:2]
	
	# refactoring yolo data
	data = yolo2fullsize(box_array, [img_height, img_width])
	fig = plt.figure(figsize=(10, 10))
	# change rgb chanel
	plt.imshow(img[:, :, [2, 1, 0]])
	# plot box on image
	color_list = ['g', 'b', 'c', 'm', 'y', 'k', 'w', 'r', 'pink']
	label2color = {}
	for shape in data:
		label = shape[0]
		if label not in label2color.keys():
			label2color[label] = color_list.pop()
			color = label2color[label]
		else:
			color = label2color[label]
		x_center = shape[1]
		y_center = shape[2]
		width = shape[3]
		height = shape[4]
		x_min = int(x_center - width / 2)
		x_max = int(x_center + width / 2)
		y_min = int(y_center - height / 2)
		y_max = int(y_center + height / 2)
		# add rectangle on image
		plt.gca().add_patch(
			# patches.Rectangle((x_min, y_min), width, height, linewidth=1, edgecolor='r', facecolor='none'))
			patches.Rectangle((x_min, y_min), width, height, linewidth=3, edgecolor=color, facecolor='none'))
		# 框内部左上角显示标签
		if label_list is None:
			plt.text(x_min, y_min, label, fontsize=10)
		else:
			if int(label) >= len(label_list):
				print('label index out of range')
				label = 'unknown'
			if int(label) == -1:
				label = 'unknown'
			else:
				label = label_list[int(label)]
			plt.text(x_min, y_min, label, fontsize=10)
	# remove axis
	# plt.axis('off')
	# remove margin
	# plt.margins(0, 0)
	# 去除白边
	plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
	if show:
		plt.show()
	return fig


# visualize labelme_local data or yolo data on image
def visuallize_label_file_on_image(data_path, imgpath, label_list=None, show=False):
	# load image
	img = cv2.imread(imgpath)
	img_height, img_width = img.shape[:2]
	# load labelme_local data
	if data_path.endswith('.json'):
		labelme_data = read_labelme(data_path)
		for shape in labelme_data['shapes']:
			shape = labelmeshape2rectangle(shape)
		# turn labelme_local data into yolo data
		data = labelme2yolo(labelme_data, label_list=label_list)
	
	# load yolo data
	elif data_path.endswith('.txt'):
		data = read_yolo(data_path)
	fig = visualize_box_on_image(data, imgpath, show=show, label_list=label_list)
	return fig


class main_scene(QGraphicsScene):
	def __init__(self):
		super(main_scene, self).__init__()
		self._width = 2000
		self._height = 2000
		self.setSceneRect(-self._width / 2, -self._height / 2, self._width, self._height)
		self.setBackgroundBrush(QBrush(QColor(Qt.black)))


class canvas_view(QGraphicsView):
	def __init__(self, scene):
		super(canvas_view, self).__init__()
		self._scene = scene
		self.setScene(self._scene)
		
		self.showing_pic = None
		# scale
		self._zoom_clamp = [0.5, 5]
		self._zoom_factor = 1.05
		self._view_scale = 1.0
	
	def zoom_in(self):
		self._view_scale *= self._zoom_factor
		if self._view_scale > self._zoom_clamp[1]:
			self._view_scale = self._zoom_clamp[1]
			self.scale(1, 1)
		else:
			self.scale(self._zoom_factor, self._zoom_factor)
	
	def zoom_out(self):
		self._view_scale *= 1 / self._zoom_factor
		if self._view_scale < self._zoom_clamp[0]:
			self._view_scale = self._zoom_clamp[0]
			self.scale(1, 1)
		else:
			self.scale(1 / self._zoom_factor, 1 / self._zoom_factor)
	
	def default_scale(self):
		self.fitInView(self.showing_pic, Qt.KeepAspectRatio)
	
	def show_file_img(self, imgpath):
		pix_ = QImage(imgpath)
		_w, _h = pix_.rect().width(), pix_.rect().height()
		
		# 清空并绘制
		self._scene.clear()
		# 调整大小
		self._scene.setSceneRect(0, 0, _w, _h)
		self.showing_pic = self._scene.addPixmap(QPixmap(pix_))
		self.default_scale()
	
	def show_image(self, image_item):
		if isinstance(image_item, str):
			pixmap = QPixmap(image_item)
			# 避免windows下的bug
			if pixmap.isNull():
				pixmap = QPixmap(image_item.replace('/', '\\'))
				# 如果还读取不出来就plt读取变成fig
				if pixmap.isNull():
					fig = plt.figure()
					image_item = plt.imread(image_item)
					# 去除边框和坐标
					plt.axis('off')
					plt.imshow(image_item)
					# 去除白边
					plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
					image_item = fig
					image_item.canvas.draw()
					qimage = QImage(image_item.canvas.buffer_rgba(), image_item.canvas.buffer_rgba().shape[1],
					                image_item.canvas.buffer_rgba().shape[0], QImage.Format_RGBA8888)
					pixmap = QPixmap.fromImage(qimage)
		else:
			# convert figure to pixmap
			image_item.canvas.draw()
			qimage = QImage(image_item.canvas.buffer_rgba(), image_item.canvas.buffer_rgba().shape[1],
			                image_item.canvas.buffer_rgba().shape[0], QImage.Format_RGBA8888)
			pixmap = QPixmap.fromImage(qimage)
		# pixmap.fromImage(image_item.canvas.tostring_rgb(), -1)
		_w, _h = pixmap.rect().width(), pixmap.rect().height()
		# 清空并绘制
		self._scene.clear()
		self._scene.setSceneRect(0, 0, _w, _h)
		self.showing_pic = self._scene.addPixmap(pixmap)
		self.default_scale()


def save_yolo(data, savepath):
	with open(savepath, 'w+') as f:
		for line in data:
			f.write(' '.join([str(_) for _ in line]) + '\n')


def savelabelme2yolo(inputpath, savepath, label_list=None):
	# load labelme_local data
	labelme_data = read_labelme(inputpath)
	# turn labelme_local data into yolo data
	data = labelme2yolo(labelme_data, label_list=label_list)
	# save yolo data
	save_yolo(data, savepath)


def saveyolo2labelme(inputpath, savepath, imgpath=None, label_list=None):
	# load yolo data
	yolo_data = read_yolo(inputpath)
	# turn yolo data into labelme_local data
	if imgpath is not None:
		img = cv2.imread(imgpath)
		img_height, img_width = img.shape[:2]
		# 判断绝对路径
		if not os.path.isabs(imgpath):
			imgpath = os.path.abspath(imgpath)
		data = yolo2labelme(yolo_data, [img_width, img_height], imgpath, label_list)
	else:
		data = yolo2labelme(yolo_data, label_list)
	# save labelme_local data
	save_labelme(data, savepath)


def edit_label(img_path, label_path):
	# 如果label_path 是以txt结尾的，就转换成json
	# 检查是否为绝对路径
	if not os.path.isabs(img_path):
		img_path = os.path.abspath(img_path)
	if not os.path.isabs(label_path):
		label_path = os.path.abspath(label_path)
	
	# 如果是txt转换为json
	if label_path.endswith('.txt'):
		saveyolo2labelme(label_path, label_path.replace('.txt', '.json'), img_path)
		label_path = label_path.replace('.txt', '.json')
	# 打开labelme
	return label_path


def train_YoRes(yolo_weight_path, data_yaml, yolo_model_save_path,res_model_save_path, model_name, epoch, res_weight_path, lr):
	
	# train yolo first
	opt = train_2step.parse_opt(weight_path=yolo_weight_path, data_yaml=data_yaml, epochs=epoch)
	yolo_save_path = train_django.main(opt)
	# 移动yolo的权重到save文件夹下
	best_yolo_weight_path = os.path.join(yolo_save_path, 'weights/best.pt')
	if not os.path.exists(yolo_model_save_path):
		os.makedirs(yolo_model_save_path)
	shutil.move(best_yolo_weight_path, yolo_model_save_path + '/' + 'yolo_' + model_name)
	# 删除yolo_save_path下的文件
	shutil.rmtree(yolo_save_path)
	
	new_res_path = train_res.main(
		weight=res_weight_path,
		output_path=res_model_save_path,
		data_yaml=data_yaml,
		name=model_name,
		epoch=epoch,
		lr=lr,
		freeze=True
	)
	
	return yolo_model_save_path + '/' + 'yolo_' + model_name,new_res_path


def stat_summary(label_dict):
	dict_info = expplot.extract_info_from_dict(label_dict)
	dict_info = np.array(dict_info, dtype=object)
	fig = plt.figure(figsize=(10, 8))
	ax1 = plt.subplot(2, 2, 1)
	ax2 = plt.subplot(2, 2, 3)
	ax3 = plt.subplot(1, 2, 2)
	
	
	c = expplot.draw_score_line(dict_info, ax2)
	if not c:
		#完全没有标记细胞
		return False,False
	else:
		expplot.draw_cell_fraction(dict_info, ax3, c)
		test = expplot.draw_cell_size(dict_info, ax1, c)
		plt.tight_layout()
		return fig,dict_info

if __name__ == '__main__':
	# txt_file = '/code/yolov_res/runs/detect/px1_0307_cache032/labels/patch_2_23.txt'
	# yolo_data = read_yolo(txt_file)
	# labelme_data = yolo2labelme(yolo_data)
	# save_labelme(labelme_data, '/code/yolov_res/runs/detect/px1_0307_cache032/labels/patch_2_23.json')
	#
	img = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/codepyqt5/code/checkpoints/CP2.5_Image002_ch02.tif'
	json_ = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/codepyqt5/code/checkpoints/CP2.5_Image002_ch02.json'
	# txt = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/codepyqt5/code/checkpoints/CP2.5_Image002_ch02.txt'
	txt = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/codepyqt5/code/checkpoints/CP2.5_Image002_ch02.txt'
	# json_ = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/data/sample0307/cache03 jason/patch_9_25.json'
	# img = '/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/data/sample0307/cache03/patch_9_25.jpg'
	# yolo_data = read_yolo(txt_file)
	# labelme_data = read_labelme(json_file)
	# yolo_data = labelme2yolo(labelme_data)
	# visualize_box_on_image(json,img)
	# fig = visuallize_label_file_on_image(json_, img)
	# fig.canvas.draw()
	# savelabelme2yolo(json_, txt)
	# saveyolo2labelme(txt, './test2.json', img,['cell','dead'])
	# savelabelme2yolo(json_, txt, ['cell', 'dead'])
	visuallize_label_file_on_image(txt, img, show=True)
