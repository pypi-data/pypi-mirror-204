import os
import time
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QDialog, QComboBox, QSizePolicy,QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
# import utils  # Assuming you have a utils module with the required functions
from src.widgets  import LeftTopLeftWidget,LeftTopRightWidget,LeftBottomWidget,ImageWidget,LeftBottomTabWidget,InfoWidget
import utils
import shutil
from src.labelme_local.wind import labelme_subwindow
from src.labelme_local import app as labelme_app
import random
import sys
from PyQt5.QtWidgets import QApplication
class MainWindow(QWidget):
    sub_window_closed = pyqtSignal()
    def __init__(self):
        super().__init__()
        self._info = 'mainwindow'
        # self.subwindow = labelme_subwindow()
        self.initUI()
        self.labelme_mainwindow = labelme_app.MainWindow
        
    def initUI(self):
        # 创建左上左部分的窗口
        self.left_top_left_widget = LeftTopLeftWidget(self)
        #指定大小100*500
        self.left_top_left_widget.setFixedSize(150, 400)

        # # 创建左上右部分的窗口
        self.left_top_right_widget = LeftTopRightWidget(self)
        #固定大小100*500
        self.left_top_right_widget.setFixedSize(250, 400)
        #可以有拖动条
        self.left_top_right_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        
        #
        # # 创建左上侧整体布局
        self.left_top_layout = QHBoxLayout()
        self.left_top_layout.addWidget(self.left_top_left_widget)
        self.left_top_layout.addWidget(self.left_top_right_widget)
        
        #左中布局
        self.info_table = InfoWidget()
        
        # # 左下侧布局
        # self.left_bottom_widget = LeftBottomWidget()
        self.left_bottom_widget = LeftBottomTabWidget()
        self.left_bottom_widget.setFixedSize(400, 300)
        
        
        # 左侧整体布局
        self.left_layout = QVBoxLayout()
        self.left_layout.addLayout(self.left_top_layout)
        self.left_layout.addWidget(self.info_table)
        self.left_layout.addWidget(self.left_bottom_widget)
        
        # 创建右侧窗口
        self.right_widget = ImageWidget()
        self.right_widget.setMinimumSize(200, 200)
        # self.right_widget.setBaseSize(400, 400)
        self.main_scene = utils.main_scene()
        self.right_widget = utils.canvas_view(self.main_scene)
        self.right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 创建整体布局
        
        self.main_h_layout = QHBoxLayout()
        
        self.main_h_layout.addLayout(self.left_layout)
        self.main_h_layout.addWidget(self.right_widget)
        
        #大小900*600
        self.resize(1440, 900)
        self.setWindowTitle("Cell Scanner")
        self.setLayout(self.main_h_layout)
        
    def openfile(self):
        self.subwindow.show()

    def add_item(self):
        # 选择文件路径
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "./", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.left_top_right_widget.add_item(file_path)
        else:
            pass
        
    def batch_add_item(self):
        # 选择文件路径
        file_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if file_path:
            # 遍历所有文件夹内的图片，获取绝对路径
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # if file is a picture file such as jpg, png, tif, etc.
                    if file_path.endswith(('.jpg', '.png', '.tif')):
                        self.left_top_right_widget.add_item(file_path)
        else:
            pass
        
    def add_label(self):
        # Qdialog窗口包含两个选项labeled和manual_checked
        dialog = QDialog()
        dialog.setWindowTitle("选择标注方式")
        dialog.resize(300, 100)
        layout = QVBoxLayout()
        # Qcombobox选择标注方式
        combo = QComboBox()
        combo.addItem("labeled")
        combo.addItem("manual_checked")
        layout.addWidget(combo)
        # Qpushbutton确定
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.setLayout(layout)
        label_type =None
        # 确认返回选择的标注方式
        if dialog.exec():
            label_type = combo.currentText()
        if label_type == None:
            return
        # 选择json或txt文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "./", "All Files (*);;Text Files (*.txt)")
        #判断是否选中文件
        if file_path:
            self.left_top_right_widget.add_label(file_path, label_type)
        else:
            pass

    def batch_add_label(self):
        # Qdialog窗口包含两个选项labeled和manual_checked
        dialog = QDialog()
        dialog.setWindowTitle("选择标注方式")
        dialog.resize(300, 100)
        layout = QVBoxLayout()
        # Qcombobox选择标注方式
        combo = QComboBox()
        combo.addItem("labeled")
        combo.addItem("manual_checked")
        layout.addWidget(combo)
        # Qpushbutton确定
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.setLayout(layout)
        label_type = None
        # 确认返回选择的标注方式
        if dialog.exec():
            label_type = combo.currentText()
        if label_type == None:
            return
        # 选择文件路径
        file_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if file_path:
            # 遍历所有文件夹内的图片，获取绝对路径
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # if file is a picture file such as jpg, png, tif, etc.
                    if file_path.endswith(('.json', '.txt')):
                        self.left_top_right_widget.add_label(file_path, label_type)
        else:
            pass
        
    def remove_item(self):
        self.left_top_right_widget.remove_item()
    
    def remove_all_item(self):
        self.left_top_right_widget.remove_all_item()
        
    def predict(self):
        # 获取listwidget中的当前选中项
        current_item = self.left_top_right_widget.list_widget.currentItem()
        if current_item is None:
            print('current_item is None')
            return

        if self.left_bottom_widget.left_bottom_widget.settings['yolo_path'] is None:
            print('yolo_path is None')
            return
        else:
            if self.left_bottom_widget.left_bottom_widget.settings['res_path'] is None:
                print('res_path is None, use yolo only')
            print(current_item.info)
            save_dir = utils.Yores_detect(source=current_item.info['file_path'],
                                          yolo_weight=self.left_bottom_widget.left_bottom_widget.settings['yolo_path'],
                                          resnet_weight=self.left_bottom_widget.left_bottom_widget.settings['res_path'],
                                          # resnet_weight=None,
                                          name=current_item.info['file_name'],
                                          output_dir=self.left_bottom_widget.left_bottom_widget.settings['save_path'], )
            # 更新listwidget中的当前选中项
            # 绝对路径
            save_dir = os.path.abspath('./' + str(save_dir) + f'/labels/{current_item.info["file_name"]}.txt')
            #复制savedir到item的labelpathtxt,覆盖原来的文件
            #如果原来有txtlabel
            if current_item.info['label_path_txt'] is not None:
                shutil.copy(save_dir, current_item.info['label_path_txt'])
            else:
                shutil.copy(save_dir,self.left_bottom_widget.left_bottom_widget.settings['label_saved_path'] + save_dir.rsplit('/', 1)[-1])
                current_item.info['label_path_txt'] = self.left_bottom_widget.left_bottom_widget.settings['label_saved_path'] + save_dir.rsplit('/', 1)[-1]
                
            #删除预测生成的文件夹
            shutil.rmtree(save_dir.rsplit('/', 2)[0])
            #更新json文件
            self.left_top_right_widget.update_both_label(current_item,from_='txt')
            current_item.update_label_stat('labeled')
            # 再保存一个json文件
            # utils.save_labelme(utils.yolo2labelme(utils.read_yolo(current_item.info['label_path']),
            #                                       path=current_item.info['file_path']),
            #                    current_item.info['label_path'][:-4] + '.json')
            # current_item.info['label_path'] = current_item.info['label_path'][:-4] + '.json'
            # item_fig = utils.visuallize_label_file_on_image(current_item.info['label_path_json'],
            #                                                 current_item.info['file_path'])
            # self.right_widget.show_image(item_fig)
            self.left_top_right_widget.click_on_file_list_item(current_item)
            
    def finetune(self):
        print('害在开发中')
        finetune_config = {
            'seperate_rate' : 1 ,
            'batch_size' : self.left_bottom_widget.left_bottom_widget.settings['batch_size'],
            'epochs' : self.left_bottom_widget.left_bottom_widget.settings['epoch'],
            'lr': self.left_bottom_widget.left_bottom_widget.settings['lr'],

        }
        
        #显示listwidget中的所有item
        # print(self.left_top_right_widget.list_widget.count())
        # utils.train_YoRes(yolo_weight_path=self.left_bottom_widget.settings['yolo_path'],
        #                   data_yaml_path='/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/codepyqt5/code/yolov_res/DataSummary/data.yaml')
        
        # #删除 setting['cache_path']下的所有文件, 重新建立cache_path
        # if os.path.exists(self.left_bottom_widget.settings['cache_path']):
        #     shutil.rmtree(self.left_bottom_widget.settings['cache_path'])
        # os.mkdir(self.left_bottom_widget.settings['cache_path'])
        #
        manual_count = 0    #人工标注的个数
        #
        # #建立训练格式数据集目录
        # os.makedirs(os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/train/'), exist_ok=True)
        # os.makedirs(os.path.join(self.left_bottom_widget.settings['cache_path'], 'labels/train/'), exist_ok=True)
        # os.makedirs(os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/val/'), exist_ok=True)
        # os.makedirs(os.path.join(self.left_bottom_widget.settings['cache_path'], 'labels/val/'), exist_ok=True)
        #
        tune_item = []
        # 获取listwidget中所有manual_checked的项
        for i in range(self.left_top_right_widget.list_widget.count()):
            item = self.left_top_right_widget.list_widget.item(i)
            if item.info['label_stat'] == 'manual_checked':
                manual_count += 1
                tune_item.append({'image_path':item.info['file_path'],
                                  'label_path':item.info['label_path_txt']})
        #         #将这些项的image copy到cache_path/images
        #         shutil.copy(item.info['file_path'], os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/train/'+ item.info['file_path'].rsplit('/', 1)[-1]))
        #         #将这些项的label copy到cache_path/labels
        #         shutil.copy(item.info['label_path'], os.path.join(self.left_bottom_widget.settings['cache_path'], 'labels/train/'+ item.info['label_path'].rsplit('/', 1)[-1]))
        #

        if manual_count == 0:
            print('no manual_checked item')
            return
            # 弹窗填写模型名称
        dialog = QDialog()
        dialog.setWindowTitle("输入模型名称")
        dialog.resize(300, 100)
        layout = QVBoxLayout()
        # Qcombobox选择标注方式
        lineedit = QLineEdit()
        layout.addWidget(lineedit)
        # Qpushbutton确定
        button = QPushButton("确定")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.setLayout(layout)
        # 确认返回选择的标注方式
        if dialog.exec():
            model_name = lineedit.text()

        # 分割train和val
        n = len(tune_item)
        random.shuffle(tune_item)
        train_item = tune_item[:int(n*finetune_config['seperate_rate'])]
        val_item = tune_item[int(n*finetune_config['seperate_rate']):]
        if val_item == []:
            val_item = train_item
        # for file in os.listdir(os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/train/')):
        #     if random.random() < 0.2:
        #         shutil.move(os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/train/', file), os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/val/', file))
        #         shutil.move(os.path.join(self.left_bottom_widget.settings['cache_path'], 'labels/train/', file.rsplit('.',1)[0]+'.txt'),
        #                     os.path.join(self.left_bottom_widget.settings['cache_path'], 'labels/val/', file.rsplit('.',1)[0]+'.txt'))
        #
        
        tune_config_dict = {
            'train':train_item,
            'val':val_item,
            'nc':len(self.left_bottom_widget.left_bottom_widget.settings['label_list']),
            'names':self.left_bottom_widget.left_bottom_widget.settings['label_list'],
        }
        model_name = model_name if model_name.endswith('.pt') else model_name + '.pt'
        new_yolo_model_path,new_res_model_path = utils.train_YoRes(yolo_weight_path=self.left_bottom_widget.left_bottom_widget.settings['yolo_path'],
                          data_yaml = tune_config_dict,
                          yolo_model_save_path=self.left_bottom_widget.left_bottom_widget.settings['yolo_model_saved_path'],
                          res_model_save_path = self.left_bottom_widget.left_bottom_widget.settings['res_model_saved_path'],
                          model_name = model_name,
                          epoch=finetune_config['epochs'],
                          res_weight_path=self.left_bottom_widget.left_bottom_widget.settings['res_path'],
                          lr = finetune_config['lr'])
        
        self.left_bottom_widget.left_bottom_widget.add_yolo_path(new_yolo_model_path)
        self.left_bottom_widget.left_bottom_widget.add_res_path(new_res_model_path)
        # #建立yolo的data.yaml文件
        # path_image_train = os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/train/')
        # path_image_val = os.path.join(self.left_bottom_widget.settings['cache_path'], 'images/val/')
        # yaml_path = os.path.join(self.left_bottom_widget.settings['cache_path'], 'data.yaml')
        # with open(yaml_path, 'w') as f:
        #     f.write(f'train: {path_image_train}\n')
        #     f.write(f'val: {path_image_val}\n')
        #     f.write(f'nc: {2}\n')
        #     f.write(f"names: ['dead','normal]")
        
        #准备yolo config文件
        
        
        #训练模型并获取保存路径
        
        
        #将模型权重move到setting['save_path']下
        
        
        #将新模型加入left_bottom_widget的combobox中
        
        
        #将新模型设为当前模型
        
        
        #删除yolo运行保存路径下的所有文件
        
        
        #删除setting['cache_path']下的所有文件
        # time.sleep(10)
        # if os.path.exists(self.left_bottom_widget.settings['cache_path']):
        #     shutil.rmtree(self.left_bottom_widget.settings['cache_path'])

    def edit_label(self):
        print('start edit')
        # 获取listwidget中的当前选中项
        current_item = self.left_top_right_widget.list_widget.currentItem()
        #获取config参数
        config = self.left_bottom_widget.left_bottom_widget.settings
        
        #如果没选中就结束
        if current_item is None:
            print('current_item is None')
            return
        
        # 获取当前选中项的标注文件路径
        label_path = current_item.info['label_path_txt']
        
        
        
        output_path = os.path.join(config['save_path'], current_item.info['file_name'] + '.json')
        #如果没有标注文件
        if label_path is None:
            print('label_path is None')
            #image input
            filepath = current_item.info['file_path']
            output_path = os.path.join(config['save_path'], current_item.info['file_name'] + '.json')
            
        #如果有标注文件
        elif label_path.endswith('.txt'):
            # 在原路径下创建一个cache.json文件，转换yolo为labelme格式
            if os.path.exists(label_path.rsplit('/', 1)[0] + '/cache.json'):
                os.remove(label_path.rsplit('/', 1)[0] + '/cache.json')
            img_path = current_item.info['file_path']
            utils.save_labelme(utils.yolo2labelme(utils.read_yolo(label_path),path=img_path), label_path.rsplit('/', 1)[0] + '/cache.json')
            label_path = label_path.rsplit('/', 1)[0] + '/cache.json'
            #json input
            filepath = utils.edit_label(img_path, label_path)
            output_path = os.path.join(config['save_path'], current_item.info['file_name'] + '.json')
        # elif label_path.endswith('.json'):
        #     #json input
        #     filepath = label_path
        #     output_path = os.path.join(config['save_path'], current_item.info['file_name'] + '.json')
        
        config,filename,output_file,output_dir = labelme_subwindow(filepath,output_place = output_path)
        
        self.win2 = self.labelme_mainwindow(
                    config=config,
                    filename=filename,
                    output_file=output_file,
                    output_dir=output_dir,
                )
        self.win2.sub_window_closed.connect(self.subwindowClosed)
        # win2.sub_window_closed.connect(self.subwin_postprocess)
        self.win2.show()
        # #win2打开时锁定主窗口
        self.setDisabled(True)
    
    #subwin关闭后的处理
    def subwindowClosed(self):
        #获取listwidget中的当前选中项
        current_item = self.left_top_right_widget.list_widget.currentItem()
        current_img_path = current_item.info['file_path']
        # current_label_path = current_img_path.rsplit('.', 1)[0] + '.json'
        default_label_path = current_img_path.rsplit('.', 1)[0] + '.json'
        
        if not os.path.isfile(default_label_path):
            #就是没有改动，没有产生新的文件;且如果图片和标注文件在同一文件夹下，那么就不会产生新的文件，但也不可能不存在
            if current_item.info['label_path_txt'] == None:
                self.setDisabled(False)
                return
            default_label_path = current_item.info['label_path_txt'].rsplit('/', 1)[0] + '/cache.json'
        else:
            #删除cache
            if current_item.info['label_path_txt'] != None:
                if os.path.exists(current_item.info['label_path_txt'].rsplit('/', 1)[0] + '/cache.json'):
                    os.remove(current_item.info['label_path_txt'].rsplit('/', 1)[0] + '/cache.json')
            else:
                assert (current_item.info['label_path_txt']==None)
                assert (current_item.info['label_path_json'] == None)
                current_item.info['label_path_txt'] = \
                    self.left_bottom_widget.left_bottom_widget.settings['label_saved_path']+current_item.info['file_name']+'.txt'
                
                
                current_item.info['label_path_json'] = \
                    self.left_bottom_widget.left_bottom_widget.settings['label_saved_path'] + current_item.info['file_name']+'.json'
        #转换labelme数据中的token为label
        data = utils.read_labelme(default_label_path)
        for shape in data['shapes']:
            shape['label'] = self.left_bottom_widget.left_bottom_widget.settings['label_list'][int(shape['label'])]
            
        utils.save_labelme(data, default_label_path)
        #转换为yolo格式
        utils.savelabelme2yolo(default_label_path, current_item.info['label_path_txt'], self.left_bottom_widget.left_bottom_widget.settings['label_list'])
        #default_label_path文件覆盖原来的label_path
        shutil.move(default_label_path, current_item.info['label_path_json'])
        
        # new_label_path = os.path.join(self.left_bottom_widget.settings['save_path'],current_label_path.rsplit('/', 1)[1])
        # #move到settings中的save_path
        # shutil.move(current_label_path, new_label_path)
        # current_item.info['label_path'] = new_label_path
        current_item.update_label_stat('manual_checked')
        #更新右侧显示
        self.left_top_right_widget.select_on_file_list_item()
        #解锁主窗口
        self.setDisabled(False)

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":

    main()
