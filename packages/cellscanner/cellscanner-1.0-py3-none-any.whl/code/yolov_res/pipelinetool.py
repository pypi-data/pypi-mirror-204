import json
import matplotlib.pyplot as plt
import numpy as np
import os
from make_prediction import getprediction
import pandas as pd
from labelme import Main

def YoloPoint2LabelmePoint(H,W,x,y,w,h):
    #xywh比例转化为定值
    w_ = float(w) * float(W)
    h_ = float(h) * float(H)
    x_ = float(x) * float(W)
    y_ = float(y) * float(H)
    #中心点换左上角(lefttop)
    x_lt = x_ - w_ / 2
    y_lt = y_ - h_ / 2
    # 中心点换右下角(rightbottom)
    x_rb = x_ + w_ / 2
    y_rb = y_ + h_ / 2

    return [float(int(x_lt)),float(int(y_lt))],[float(int(x_rb)),float(int(y_rb))]

def YoloPrediction2Labelme(tiffile,txtfile,outputfile = None):
    '''
    labelme_local 左上为0,0

    '''
    d = {
    "version": "4.6.0",
    "flags": {}
    }

    shape = []
    imageHeight,imageWidth = plt.imread(tiffile).shape[:2]

    for file in open(txtfile):
        shape_i = {}
        info_i = file[:-1].split(sep = ' ')

        pointLT, pointRb = YoloPoint2LabelmePoint(imageHeight,imageWidth,*info_i[1:5])
        shape_i['label'] = info_i[0]
        shape_i['points'] = [pointLT,pointRb]
        shape_i["group_id"] = None
        shape_i["shape_type"] = "rectangle"
        shape_i["flags"] = {}
        shape.append(shape_i)

    d['shapes'] = shape
    d["imagePath"]= tiffile
    d["imageData"]= None
    d["imageHeight"]= imageHeight
    d[ "imageWidth"]=imageWidth

    if outputfile != None:
        with open(outputfile, 'w', encoding='utf-8') as fw:
            json.dump(d, fw, indent=2, ensure_ascii=False)
        # print('transform success')
    else:
        print('no outout file given')

def GetSummaryFromJson(jsonpath):
    labels_ = []
    with open(jsonpath,'r') as f_:
        d_ = json.load(f_)
        for point_ in d_['shapes']:
            labels_.append(int(point_['label']))

    n_norm = labels_.count(0)
    n_dead = labels_.count(1)
    n_total = n_norm + n_dead
    norm_rate = np.round(n_norm/n_total,3)
    dead_rate = np.round(n_dead/n_total,3)
    return [n_norm,norm_rate,n_dead,dead_rate,n_total]

class CellDetect:
    def __init__(self,pic_path = None,output_path = None,label_path = None,model_pt_path = None,summary_dir = None):
        self.pic_path = pic_path
        self.output_path = output_path
        self.label_path = label_path
        self.model_pt_path = model_pt_path
        self.summary_dir = summary_dir


    def predict(self,model_pt_path = None,output_path = None,pic_path = None):
        if output_path == None:
            if self.output_path == None:
                print('No output path !')
                return
        else:
            self.output_path = output_path

        if pic_path == None:
            if self.pic_path == None:
                print('No pic path !')
                return
        else:
            self.pic_path = pic_path

        if model_pt_path == None:
            if self.model_pt_path == None:
                print('No model.pt path !')
                return
        else:
            self.model_pt_path = model_pt_path

        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        self.label_path = getprediction(self.pic_path, self.model_pt_path, output_path=self.output_path)
        self.label_path = os.path.join(self.output_path, self.label_path.split('\\')[-1]) +'\labels\\'


    def transfer_label(self,type,label_path = None,pic_path = None):
        if label_path == None:
            if self.label_path == None:
                print('No label path !')
                return
        else:
            self.label_path = label_path

        if pic_path == None:
            if self.pic_path == None:
                print('No pic path !')
                return
        else:
            self.pic_path = pic_path

        if type == 'yolo2labelme':
            files = [_[:-4] for _ in os.listdir(self.label_path) if _.endswith('.txt')]
            for file in files:
                YoloPrediction2Labelme(self.pic_path+file+'.tif',self.label_path+file+'.txt',self.label_path+file+'.json')
            print('Transfer to json(for labelme_local)')
        else:
            print('transfer type not supported')


    def rectify_predicts(self,label_path = None,pic_path = None):
        if label_path == None:
            if self.label_path == None:
                print('no label path given')
                return
        else:
            self.label_path = label_path

        if pic_path == None:
            if self.pic_path == None:
                print('No pic path !')
                return
        else:
            self.pic_path = pic_path

        Main.main(self.pic_path, self.label_path)


    def get_summary_file(self,summary_dir = None,label_path = None):
        if label_path == None:
            if self.label_path == None:
                print('no label path given')
                return
        else:
            self.label_path = label_path

        if summary_dir == None:
            if self.summary_dir == None:
                self.summary_dir = self.label_path+'summary.csv'
                print('summary will save at label path')
        else:
            self.summary_dir = summary_dir

        summary = []
        summary_index = []
        files = [_[:-4] for _ in os.listdir(self.label_path) if _.endswith('.txt')]

        for file in files:
            summary.append(GetSummaryFromJson(self.label_path+file+'.json'))
            summary_index.append(file)

        summary = pd.DataFrame(summary)
        summary.columns = ['n_norm','norm rate','n_dead','dead rate','n_total']
        summary.index = summary_index
        summary.to_csv(self.summary_dir)
        print('Summary file saved at '+self.summary_dir)

if __name__ == '__main__':
    t = GetSummaryFromJson('Y:/work/untitled/test/results/Image013_ch00.json')
    print(t)
