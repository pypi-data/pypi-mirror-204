import argparse
import os
import sys
from pathlib import Path
import pandas as pd
import cv2
import torch
import matplotlib

matplotlib.use('TkAgg')
import torch.backends.cudnn as cudnn
from src.yolov_res.model_cls.dataset import  pred2dataset
FILE = Path(__file__).resolve()
from tqdm import tqdm
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
from torch.utils.data import DataLoader
from src.yolov_res.models.common import DetectMultiBackend
from src.yolov_res.utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from src.yolov_res.utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from src.yolov_res.utils.plots import Annotator, colors, save_one_box
from src.yolov_res.utils.torch_utils import select_device, time_sync
from src.yolov_res.model_cls.resnet import resnet18, resnet34, resnet50, resnet101
import  os
import  matplotlib.pyplot as plt
import numpy as np
# 识别模型初始化
model_cls = resnet34()
model_cls.load_state_dict(torch.load('/Volumes/ckw/yolov5-master/model_cls/_saved/weight_2022518/best.pt',map_location=torch.device('cpu')))


def letterbox( im, new_shape=(128,128), color=(114, 114, 114), auto=False, scaleFill=True, scaleup=True,
              stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])

    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)

    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border

    return im, ratio, (dw, dh)
path = '/Volumes/ckw/yolov5-master/runs/detect/exp/crops/dead/'

for val in os.listdir(path):
    if val.endswith('jpg'):
        im = cv2.imread(path + val)
        im = torch.Tensor(im)

        h0, w0 = im.shape[:2]
        r = 128 / max(h0, w0)
        if r != 1:  # if sizes are not equal
            im = cv2.resize(np.array(im), (int(w0 * r), int(h0 * r)),
                            interpolation=cv2.INTER_LINEAR if (True or r > 1) else cv2.INTER_AREA)

        im, _, (_, _) = letterbox(im, new_shape=(128, 128))

        # self.augment_hsv(im)

        # if random.random() < 0.5:
        #     im = np.flipud(im)
        # if random.random() < 0.5:
        #     im = np.fliplr(im)

        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)
        im = torch.Tensor(im)
        im = im.unsqueeze(0)

        pred = model_cls(im)
        pred_cls = torch.max(pred, dim=1)[1]

        img = im.squeeze(0)
        img = img.transpose(0,1).transpose(1,2)

        plt.imshow(img/255)
        plt.title(str(pred_cls))
        plt.show()

        print(pred_cls)

