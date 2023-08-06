import train_django
from model_cls import train
import yaml
import shutil
import os
#yolo param


ROOT = 'yolov_res/'

class parse_opt():
	def __init__(self, weight_path,data_yaml,epochs = 5):
		self.weights = weight_path
		self.cfg = ROOT + 'models/yolov5l.yaml'
		self.data = data_yaml
		self.hyp = ROOT + 'data/hyps/hyp.yaml'
		self.epochs = epochs
		self.batch_size = 4
		self.imgsz = 640
		self.rect = False
		self.resume = False
		self.nosave = False
		self.noval = False
		self.noautoanchor = False
		self.noplots = True
		self.evolve = False
		self.bucket = ''
		self.cache = 'ram'
		self.image_weights = False
		self.device = ''
		self.multi_scale = False
		self.single_cls = True
		self.optimizer = 'Adam'
		self.sync_bn = False
		self.workers = 1
		self.project = ROOT + 'runs/train'
		self.name = 'exp'
		self.exist_ok = False
		self.quad = False
		self.cos_lr = False
		self.label_smoothing = 0
		self.patience = 3
		self.freeze = [10]
		self.save_period = 1000
		self.local_rank = -1
		
		# Weights & Biases arguments
		self.entity = None
		self.upload_dataset = False
		self.bbox_interval = -1
		self.artifact_alias = 'latest'

# def operation(data_yolo_path,user_new_txt_path, user_new_jpg_path, default_pt_path, output_pt_path):
def finetune_2step(default_weight_file,yolo_data_yaml,outputpath):
	#loaddata
	model_yolo_path = default_weight_file+'yolo.pt'
	model_resnet_path = default_weight_file + 'res.pt'

	#train yolobackbone
	opt_0 = parse_opt(model_yolo_path,yolo_data_yaml)
	yolo_save_dir = train_django.main(opt_0)
	
	#copy model & remove dir
	
	
	#train resnet
	yml = yaml.load(open(yolo_data_yaml, 'r'), Loader=yaml.FullLoader)
	train.main(yml['train'], yml['train'].replace('images', 'labels'), yml['val'], yml['val'].replace('images', 'labels'), yolo_save_dir, model_resnet_path)
	
	#save model
	if not os.path.isdir(outputpath):
		os.mkdir(outputpath)
	shutil.copy(yolo_save_dir+'/weights/best.pt',outputpath+'/yolo.pt')
	shutil.copy(yolo_save_dir+'/weights/best_res.pt',outputpath+'/res.pt')

if __name__ == '__main__':
	weightpath = '/Users/zhuhanwen/Desktop/project/Celldetectproject/b_Celldetect/Celldetect/yolov5/models/weight/default_model/'
	yolo_data_yaml ='/Users/zhuhanwen/Desktop/project/Celldetectproject/b_Celldetect/Celldetect/yolov5/mydata2/data.yaml'
	finetune_2step(weightpath,yolo_data_yaml
	               ,'/Users/zhuhanwen/Desktop/project/Celldetectproject/b_Celldetect/Celldetect/yolov5/models/weight/tune_1/')
	