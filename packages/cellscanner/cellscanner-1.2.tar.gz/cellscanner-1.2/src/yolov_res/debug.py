from detect_yocls import run
import objgraph
import time
import train

ROOT = train.ROOT
class parse_opt():
    def __init__(self,data_yaml_path):
        print(ROOT)
        self.weights = ROOT / 'models/weight/default_model/yolo.pt'
        self.cfg = ROOT / 'models/yolov5l.yaml'
        self.data =  ROOT/ 'DataSummary/data.yaml'
        self.hyp = ROOT / 'data/hyps/hyp.yaml'
        self.epochs = 5
        self.batch_size = 1
        self.imgsz = 640
        self.rect = False
        self.resume = False
        self.nosave = False
        self.noval = False
        self.noautoanchor = False
        self.noplots = False
        self.evolve = False
        self.bucket = ''
        self.cache = 'ram'
        self.image_weights = False
        self.device = ''
        self.multi_scale = False
        self.single_cls = True
        self.optimizer = 'SGD'
        self.sync_bn = False
        self.workers = 1
        self.project = ROOT / 'runs/train'
        self.name = 'exp'
        self.exist_ok = False
        self.quad = False
        self.cos_lr = False
        self.label_smoothing = 0
        self.patience = 20
        self.freeze = [10] #default 0
        self.save_period = 1000
        self.local_rank = -1

        # Weights & Biases arguments
        self.entity = None
        self.upload_dataset = False
        self.bbox_interval = -1
        self.artifact_alias = 'latest'

if __name__ == '__main__':
	opt = parse_opt(ROOT / 'DataSummary/data.yaml')
	print(opt)