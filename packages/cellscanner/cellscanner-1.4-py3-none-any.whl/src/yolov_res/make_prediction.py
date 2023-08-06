import os
import sys
import pandas as pd
from pathlib import Path
import detect
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
from utils.general import (check_requirements)
def get_summary(path):
    pic_id_list = os.listdir(path+'/labels/')
    summary = []
    for pic_id in pic_id_list:
        d_pic = pd.read_csv(path + '/labels/' +pic_id,header = None,sep = ' ')
        n_detect = d_pic.shape[0]
        dead_cell_num = sum(d_pic.iloc[:,0])
        normal_cell_num = n_detect - dead_cell_num
        dead_rate = dead_cell_num/n_detect
        summary.append([pic_id,n_detect,normal_cell_num,dead_cell_num,dead_rate])
    summary = pd.DataFrame(summary)
    summary.columns = ['pic_id','n_cells','n_normal','n_dead','dead_rate']
    summary.to_csv(path+'summary.csv',index = None)
    return

def getprediction(source,weight_path,output_path = ROOT / 'runs/detect'):
    check_requirements(exclude=('tensorboard', 'thop'))
    save_dir = detect.run(
        weights=weight_path,
        source=source,  # file/dir/URL/glob, 0 for webcam
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.4,  # confidence threshold
        iou_thres=0.4,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=True,  # save results to *.txt
        save_conf=True,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=True,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=output_path,  # save results to project/name
        name='predict',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False
    )
    return save_dir

if __name__ == '__main__':
    a = getprediction('../../data/cache/','models/pt16kft4k.pt','../../data/detectresult/')
    print(a)