import numpy
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import cv2
from PIL import Image
import os
import re
import matplotlib.pyplot as plt
import numpy as np
import math
import random



def batch(img, label):
    lbl = []
    name = []
    iml = []
    for val in os.listdir(label):
        if val.endswith('txt'):
            n = val.split('/')[-1][:-4]
            if n.startswith('.'):
                continue
            lbl.append(label + '/' +val)

            name.append(n)
    for val in os.listdir(img):
        if val.endswith('jpg') or val.endswith('tif'):
            n = val.split('/')[-1][:-4]
            if n.startswith('.'):
                continue
            if n in name:
                iml.append(img + '/' +val)
    lbl = sorted(lbl)
    iml = sorted(iml)
    return iml, lbl


def cropimg(img, label):
    img = cv2.imread(img)

    file = open(label, 'r').readlines()
    lb = []
    im = []
    for line in file:
        cls, x, y, w, h = line.split(' ')
        x, y, w, h = float(x), float(y), float(w), float(h.replace('\n', ''))
        w = w * img.shape[1]
        h = h * img.shape[0]
        x = x * img.shape[1]
        y = y * img.shape[0]
        x1 = max(int(x - w / 2), 0)
        y1 = max(int(y - h / 2), 0)
        x2 = min(int(x + w / 2), img.shape[1])
        y2 = min(int(y + h / 2), img.shape[0])
        lb.append(int(cls))
        #         print(x1,x2,y1,y2)
        crop = img[y1:y2, x1:x2, :]
        #         print(crop)
        im.append(crop)
    return im, lb

def croppred(img,pred):
    img = img.squeeze(0)
    img = img.transpose(0,1).transpose(1,2)
    # print(img.shape)
    pred = pred[0]
    im = []
    lbfromyo = []
    conffromyolo = []
    for val in pred:
        # print(val)
        x1, y1, x2, y2, conf, cls = val
        # print(y1,y2)
        x1, y1, x2, y2, = max(int(x1), 0), \
                          max(int(y1), 0), \
                          min(int(x2), img.shape[1]), \
                          min(int(y2), img.shape[0])
        #
        # x1 = x1 * img.shape[1]
        # x2 = x2 * img.shape[1]
        # y1 = y1 * img.shape[0]
        # y2 = y2 * img.shape[0]

        # print(x1,x2,y1,y2)
        #
        # w = w * img.shape[1]
        # h = h * img.shape[0]
        # x = x * img.shape[1]
        # y = y * img.shape[0]
        # x1 = max(int(x - w / 2), 0)
        # y1 = max(int(y - h / 2), 0)
        # x2 = min(int(x + w / 2), img.shape[1])
        # y2 = min(int(y + h / 2), img.shape[0])
        lbfromyo.append(int(cls))
        #         print(x1,x2,y1,y2)
        crop = img[y1:y2, x1:x2, :]



        #         print(crop)
        # print(crop.shape)
        conffromyolo.append(float(conf))
        im.append(crop)
    return im, lbfromyo, conffromyolo


class ImageDataset(Dataset):
    def __init__(self, imagePath, labelPath, cache_path='./', prefix='train',balance =True):
        super(ImageDataset, self).__init__()
        self.img_size = 128
        self.imagePath = imagePath
        self.labelPath = labelPath

        p_im, p_lb = batch(self.imagePath, self.labelPath)
        # 配对
        img_list, lb_list = [], []
        # if os.path.exists(cache_path + prefix + '.npy'):
        if False:
            cache = np.load(cache_path + prefix + '.npy', allow_pickle=True).item()
            self.img_list = cache['img']
            self.lb_list = cache['lb']
            print(cache_path + prefix + '.npy')
        else:
            cachex = {}
            for i, j in zip(p_im, p_lb):
                x, y = cropimg(i, j)
                for m, n in zip(x, y):
                    img_list.append(m)
                    lb_list.append(np.absolute(int(n)))
            
            if balance:
                lb_total = list(set(lb_list))
                print('Dataloader: total label ',lb_total,'')
                lb = np.array(lb_list)
                img = np.array(img_list)
                min_lb_num = len(lb_list)
                for lb_ in lb_total:
                    lb_n_ = (lb==lb_).sum()
                    if lb_n_<min_lb_num:
                        min_lb_num = lb_n_
                    print('Dataloader: label_{}'.format(lb_),'\t',lb_n_)
                print('Dataloader: balancing each label to {}'.format(min_lb_num))

                new_img_list = []
                new_lb_list = []
                
                for lb_ in lb_total:
                    lb_n_ = (lb == lb_).sum()
                    lb_index_ = np.arange(0,lb.shape[0])[lb == lb_]
                    for _idx in np.random.choice(lb_index_,min_lb_num,replace=False):
                        new_img_list.append(img_list[_idx])
                        new_lb_list.append(lb_list[_idx])
                cachex['img'] = new_img_list
                cachex['lb'] = new_lb_list
                np.save(cache_path + prefix + '.npy', cachex)
                
            self.img_list = new_img_list
            self.lb_list = new_lb_list
            
    def __getitem__(self, idx):
        im = self.img_list[idx]
        lb = self.lb_list[idx]
        lb = np.array(lb)

        h0, w0 = im.shape[:2]
        r = self.img_size / max(h0, w0)

        if r != 1:  # if sizes are not equal
            im = cv2.resize(im, (int(w0 * r), int(h0 * r)),
                            interpolation=cv2.INTER_LINEAR if (True or r > 1) else cv2.INTER_AREA)

        im, _, (_, _) = self.letterbox(im, new_shape=(self.img_size, self.img_size))

        self.augment_hsv(im)

        if random.random() < 0.5:
            im = np.flipud(im)
        if random.random() < 0.5:
            im = np.fliplr(im)

        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)

        return torch.from_numpy(im), lb

    def __len__(self):
        return len(self.img_list)

    def letterbox(self, im, new_shape=(96, 96), color=(114, 114, 114), auto=False, scaleFill=True, scaleup=True,
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

    def augment_hsv(self, im, hgain=0.7, sgain=0.7, vgain=0.7):
        # HSV color-space augmentation
        if hgain or sgain or vgain:
            r = np.random.uniform(-1, 1, 3) * [hgain, sgain, vgain] + 1  # random gains
            hue, sat, val = cv2.split(cv2.cvtColor(im, cv2.COLOR_BGR2HSV))
            dtype = im.dtype  # uint8

            x = np.arange(0, 256, dtype=r.dtype)
            lut_hue = ((x * r[0]) % 180).astype(dtype)
            lut_sat = np.clip(x * r[1], 0, 255).astype(dtype)
            lut_val = np.clip(x * r[2], 0, 255).astype(dtype)

            im_hsv = cv2.merge((cv2.LUT(hue, lut_hue), cv2.LUT(sat, lut_sat), cv2.LUT(val, lut_val)))
            cv2.cvtColor(im_hsv, cv2.COLOR_HSV2BGR, dst=im)  # no return needed


class pred2dataset(Dataset):
    def __init__(self, pred, raw_image):
        super(pred2dataset, self).__init__()
        self.img_size = 128
        self.pred = pred
        self.raw_image = raw_image
        self.img_list, self.yololb, self.conffromyolo = croppred(raw_image, pred)


    def __len__(self):
        return len(self.pred)

    def __getitem__(self, idx):

        fail_anchor = []
        for i in range(len(self.img_list)):
            im  = self.img_list[i]
            im = np.ascontiguousarray(torch.Tensor.cpu(im))
            # print(im.shape)
            h0, w0 = im.shape[:2]
            r = self.img_size / max(h0, w0)
            if r != 1:  # if sizes are not equal
                # im = cv2.resize(np.array(im), (int(w0 * r), int(h0 * r)),
                #                 interpolation=cv2.INTER_LINEAR if (True or r > 1) else cv2.INTER_AREA)
                try:
                    im = cv2.resize(im, (int(w0 * r), int(h0 * r)),
                                    interpolation=cv2.INTER_LINEAR if (True or r > 1) else cv2.INTER_AREA)
                except:
                    # print(self.pred[0][torch.arange(self.pred[0].size(0)) != i ])
                    print(im.shape)

                    print('youcuod')
                    continue
            im, _, (_, _) = self.letterbox(im, new_shape=(self.img_size, self.img_size))
            # self.augment_hsv(im)

            # if random.random() < 0.5:
            #     im = np.flipud(im)
            # if random.random() < 0.5:
            #     im = np.fliplr(im)

            im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
            im = np.ascontiguousarray(im)
            im = list(im)

            self.img_list[i] = im

        im = np.array(self.img_list)
        # print(type(im))
        im = torch.Tensor(im)
        # print(type(im))
        lb = self.yololb
        cf = self.conffromyolo

        return im, lb, cf, self.pred

    def letterbox(self, im, new_shape=(96, 96), color=(114, 114, 114), auto=False, scaleFill=True, scaleup=True,
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
    
if __name__ == '__main__':
    ImageDataset('/Users/zhuhanwen/Desktop/project/Celldetectproject/b_celldetect/CellDetect/yolov5/mydata2/images/valid',
                 '/Users/zhuhanwen/Desktop/project/Celldetectproject/b_celldetect/CellDetect/yolov5/mydata2/labels/valid')