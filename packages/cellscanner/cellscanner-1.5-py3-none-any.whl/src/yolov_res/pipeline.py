from labelme import Main
from pipelinetool import CellDetect
from make_prediction import getprediction

import os
import pandas as pd

# class CellDetect:
#     def __init__(self,pic_path = None,output_path = None,label_path = None,model_pt_path = None,summary_dir = None):
#         self.pic_path = pic_path
#         self.output_path = output_path
#         self.label_path = label_path
#         self.model_pt_path = model_pt_path
#         self.summary_dir = summary_dir
#
#
#     def predict(self,model_pt_path = None,output_path = None,pic_path = None):
#         if output_path == None:
#             if self.output_path == None:
#                 print('No output path !')
#                 return
#         else:
#             self.output_path = output_path
#
#         if pic_path == None:
#             if self.pic_path == None:
#                 print('No pic path !')
#                 return
#         else:
#             self.pic_path = pic_path
#
#         if model_pt_path == None:
#             if self.model_pt_path == None:
#                 print('No model.pt path !')
#                 return
#         else:
#             self.model_pt_path = model_pt_path
#
#         if not os.path.isdir(self.output_path):
#             os.mkdir(self.output_path)
#
#         self.label_path = getprediction(self.pic_path, self.model_pt_path, output_path=self.output_path)
#         self.label_path = os.path.join(self.output_path, self.label_path.split('\\')[-1]) +'\labels\\'
#
#
#     def transfer_label(self,type,label_path = None,pic_path = None):
#         if label_path == None:
#             if self.label_path == None:
#                 print('No label path !')
#                 return
#         else:
#             self.label_path = label_path
#
#         if pic_path == None:
#             if self.pic_path == None:
#                 print('No pic path !')
#                 return
#         else:
#             self.pic_path = pic_path
#
#         if type == 'yolo2labelme':
#             files = [_[:-4] for _ in os.listdir(self.label_path) if _.endswith('.txt')]
#             for file in files:
#                 YoloPrediction2Labelme(self.pic_path+file+'.tif',self.label_path+file+'.txt',self.label_path+file+'.json')
#             print('Transfer to json(for labelme_local)')
#         else:
#             print('transfer type not supported')
#
#
#     def rectify_predicts(self,label_path = None,pic_path = None):
#         if label_path == None:
#             if self.label_path == None:
#                 print('no label path given')
#                 return
#         else:
#             self.label_path = label_path
#
#         if pic_path == None:
#             if self.pic_path == None:
#                 print('No pic path !')
#                 return
#         else:
#             self.pic_path = pic_path
#
#         Main.main(self.pic_path, self.label_path)
#
#
#     def get_summary_file(self,summary_dir = None,label_path = None):
#         if label_path == None:
#             if self.label_path == None:
#                 print('no label path given')
#                 return
#         else:
#             self.label_path = label_path
#
#         if summary_dir == None:
#             if self.summary_dir == None:
#                 self.summary_dir = self.label_path+'summary.csv'
#                 print('summary will save at label path')
#         else:
#             self.summary_dir = summary_dir
#
#         summary = []
#         summary_index = []
#         files = [_[:-4] for _ in os.listdir(self.label_path) if _.endswith('.txt')]
#
#         for file in files:
#             summary.append(GetSummaryFromJson(self.label_path+file+'.json'))
#             summary_index.append(file)
#
#         summary = pd.DataFrame(summary)
#         summary.columns = ['n_norm','norm rate','n_dead','dead rate','n_total']
#         summary.index = summary_index
#         summary.to_csv(self.summary_dir)
#         print('Summary file saved at '+self.summary_dir)


if __name__ == '__main__':
    CD = CellDetect()

    CD.predict(model_pt_path = 'Y:\\work\\YOLO\\yolov5\\models\\pt16kft4k.pt',
               output_path = 'Y:\\work\\YOLO\\yolov5\\testresult\\',
               pic_path = 'Y:\\work\\YOLO\\yolov5\\testset\\',
               )

    CD.transfer_label(type = 'yolo2labelme',
                      # label_path = 'Y:/work/YOLO/yolov5/testresult/predict3/labels/',
                      # pic_path = 'Y:/work/YOLO/yolov5/testset/',
                      )

    # CD.rectify_predicts(
    #     label_path='Y:/work/YOLO/yolov5/testresult/predict3/labels/',
    #     pic_path='Y:/work/YOLO/yolov5/testset/',
    # )

    # CD.get_summary_file(
    #     summary_dir = './test1.csv',
    #     label_path='Y:/work/YOLO/yolov5/testresult/predict3/labels/',
    #     )