import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem,
                             QCheckBox, QLabel, QLineEdit, QSizePolicy, QDialog, QSlider, QSpinBox, QFileDialog,
                             QMessageBox, QMenu,QAction,QComboBox,QTableWidget,QTableWidgetItem,QTabWidget,QToolBar,QTreeWidget,QTreeWidgetItem)
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui import QPixmap, QColor, QImage,QCursor
from PyQt5.QtWidgets import QToolTip,QAbstractItemView
import shutil
import debug
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
import cv2
import os
import utils
import json
#检测是否为arm架构
import platform
if platform.machine() == 'aarch64':
    matplotlib.use('Qt5Agg')

class InfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        v_layout = QVBoxLayout()
        self.label = QLabel('stats info')
        #set in middle
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setStyleSheet("QLabel{background:white;}")
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(3)
        

        # 列宽，每一列的宽度
        for i in range(self.table.columnCount()):
            self.table.setColumnWidth(i, 50)
        
        v_layout.addWidget(self.label)
        v_layout.addWidget(self.table)
        self.setLayout(v_layout)
        # self.setGeometry(400, 800, 800, 200)

    def show_stats(self,stats_info):
        summary = np.array(stats_info)[:,:4]
        res_c = []
        for c in np.unique(summary[:,0]):
            res_c.append([c]+list(summary[summary[:,0]==c,1:].sum(axis=0)))
        classes = []
        total_num = []
        aim_num = []
        other_num = []
        
        
        for _ in res_c:
            classes.append(_[0])
            total_num.append(_[1])
            other_num.append(_[2])
            aim_num.append(_[3])
        
        
        self.table.setRowCount(len(classes))
        self.table.setColumnCount(5)
        
        for i in range(len(classes)):
            self.table.setItem(i,0,QTableWidgetItem(str(total_num[i])))
            self.table.setItem(i,1,QTableWidgetItem(str(aim_num[i])))
            self.table.setItem(i,2,QTableWidgetItem(str(np.round(aim_num[i]/total_num[i],4))[1:]))
            self.table.setItem(i,3,QTableWidgetItem(str(other_num[i])))
            self.table.setItem(i,4,QTableWidgetItem(str(np.round(other_num[i]/total_num[i],4))[1:]))
        
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setHorizontalHeaderLabels(['total','aim','aim_rate','other','other_rate'])
        self.table.setVerticalHeaderLabels(classes)


class LeftTopLeftWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        # create a Vertical Box Layout
        h_layout = QVBoxLayout()
    #
        button1 = QPushButton('add item')
        button_batch_add = QPushButton('add items!')
        
        button_add_label = QPushButton('add label')
        button_batch_add_label = QPushButton('add labels!')
        
        button2 = QPushButton('remove item')

        button3 = QPushButton('predict')
        button4 = QPushButton('finetune')
        button5 = QPushButton('edit label')
        
        button1.clicked.connect(self.add_item)
        button_batch_add.clicked.connect(self.batch_add_item)
        button_add_label.clicked.connect(self.add_label)
        button_batch_add_label.clicked.connect(self.batch_add_label)
        button2.clicked.connect(self.remove_item)


    #     # add buttons to the layout
        h_layout.addWidget(button1)
        h_layout.addWidget(button_batch_add)
        h_layout.addWidget(button_add_label)
        h_layout.addWidget(button_batch_add_label)
        h_layout.addWidget(button2)
        button3.clicked.connect(self.predict)
        button4.clicked.connect(self.finetune)
        button5.clicked.connect(self.edit_label)
    #
    
        
    
    #     # 加一条分割线
        h_layout.addStretch(1)

        h_layout.addWidget(button3)
        h_layout.addWidget(button4)
        h_layout.addWidget(button5)
    #     # set the layout to the widget
        self.setLayout(h_layout)
        self.setGeometry(300, 300, 300, 200)
    #     # self.setWindowTitle('PySide6 Example')

    def add_item(self):
        self.parent().add_item()

    def batch_add_item(self):
        self.parent().batch_add_item()

    def add_label(self):
        self.parent().add_label()

    def batch_add_label(self):
        self.parent().batch_add_label()

    def remove_item(self):
        self.parent().remove_item()

    def predict(self):
        self.parent().predict()

    def finetune(self):
        self.parent().finetune()

    def edit_label(self):
        self.parent().edit_label()


class FileListItem(QListWidgetItem):
    def __init__(self, file_path,parent=None):
        super().__init__(file_path,parent)
        self.info = {'file_name': file_path.rsplit('/', 1)[-1].rsplit('.', 1)[0],
                     'file_path': file_path,
                     'label_stat': None,
                     'manual_flag': False,
                     'label_path_txt': None,
                     'label_path_json':None}
        self.parent = parent
        #显示parent中的item个数
        self._widget = QWidget()
        self._layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.setText(None)
        # set checkbox 无法更改
        self.checkbox.setEnabled(False)
        
        # label 颜色随label_stat变化
        self.label = QLabel(self.info['file_name'])
        self.label.setAlignment(Qt.AlignLeft)
        self._layout.setContentsMargins(0, 0, 0, 0)
        # 默认白色
        self.label.setStyleSheet("QLabel{color:rgb(255,255,255)}")

        self._layout.addWidget(self.checkbox)
        self._layout.addWidget(self.label)
        self._widget.setLayout(self._layout)
        self.setSizeHint(self._widget.sizeHint())
    
    def switch_manualflag(self, flag=True):
        self.info['manual_flag'] = flag
        self.checkbox.setChecked(self.info['manual_flag'])
    
    def update_label_stat(self, new_stat):
        #原来的stat
        old_stat = self.info['label_stat']
        print(old_stat)
        self.info['label_stat'] = new_stat
        
        # #check if label_path is None
        # if self.info['label_path_txt'] is None and self.info['label_path_json'] is None:
        #     self.switch_manualflag(False)
        #     if self.info['label_stat'] is not 'None':
        #         self.info['label_stat'] = 'error'
        #         self.label.setStyleSheet("QLabel{color:rgb(255,0,0)}")
        #     else:
        #
        #
        # elif self.info['label_path_txt'] is None or self.info['label_path_json'] is None
        if self.info['label_stat'] is None:
            # white
            self.label.setStyleSheet("QLabel{color:rgb(255,255,255)}")
            self.switch_manualflag(False)
            if self.info['label_path_txt'] is not None:
                if os.path.exists(self.info['label_path_txt']):
                    os.remove(self.info['label_path_txt'])
            self.info['label_path_txt'] = None
            if self.info['label_path_json'] is not None:
                if os.path.exists(self.info['label_path_json']):
                    os.remove(self.info['label_path_json'])
            self.info['label_path_json'] = None
        
        elif self.info['label_stat'] == 'labeled':
            # yellow
            self.label.setStyleSheet("QLabel{color:rgb(255,255,0)}")
            if self.info['label_path_txt'] is not None and self.info['label_path_json'] is not None and os.path.exists(self.info['label_path_txt']) and os.path.exists(self.info['label_path_json']):
                self.switch_manualflag(False)
                if old_stat == 'manual_checked':
                    #移动文件到cache文件夹下
                    shutil.move(self.info['label_path_txt'],
                                self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+self.info['label_path_txt'].rsplit('/', 1)[-1])
                    shutil.move(self.info['label_path_json'],
                                self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+self.info['label_path_json'].rsplit('/', 1)[-1])
                    self.info['label_path_txt'] = self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+self.info['label_path_txt'].rsplit('/', 1)[-1]
                    self.info['label_path_json'] = self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+self.info['label_path_json'].rsplit('/', 1)[-1]
            else:
                print('label path is None')
                self.update_label_stat('error')
        
        elif self.info['label_stat'] == 'manual_checked':
            # green
            if self.info['label_path_json'] is not None and self.info['label_path_txt'] is not None and os.path.exists(self.info['label_path_json']) and os.path.exists(self.info['label_path_txt']):
                self.label.setStyleSheet("QLabel{color:rgb(0,255,0)}")
                self.switch_manualflag(True)
                if old_stat == 'labeled' or old_stat == 'error':
                    #移动到checkpoint文件夹下
                    print(self.info['label_path_txt'], self.info['label_path_json'])
                    shutil.move(self.info['label_path_txt'],
                                self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['save_path']+self.info['label_path_txt'].rsplit('/', 1)[-1])
                    shutil.move(self.info['label_path_json'],
                                self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['save_path']+self.info['label_path_json'].rsplit('/', 1)[-1])
                    self.info['label_path_txt'] = self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['save_path']+self.info['label_path_txt'].rsplit('/', 1)[-1]
                    self.info['label_path_json'] = self.parent.parent().parent().left_bottom_widget.left_bottom_widget.settings['save_path']+self.info['label_path_json'].rsplit('/', 1)[-1]
            else:
                print('json label is None')
                self.update_label_stat('error')
        
        else:
            # red
            self.label.setStyleSheet("QLabel{color:rgb(255,0,0)}")
            self.switch_manualflag(False)


class LeftTopRightWidget(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # create a Vertical Box Layout
        h_layout = QVBoxLayout()
        # create a list widget
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.click_on_file_list_item)
        #选中目标改变时触发
        self.list_widget.itemSelectionChanged.connect(self.select_on_file_list_item)
        
        # listitem右键菜单
        self.list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_right_menu)
        
        h_layout.addWidget(self.list_widget)

        # self.info_table = InfoWidget(self)
        # h_layout.addWidget(self.info_table)
        # set the layout to the widget
        self.setLayout(h_layout)
        self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('PySide6 Example')
    
    def add_item(self, path):
        item = FileListItem(path,self.list_widget)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, item._widget)
    
    def  add_label(self, path, stat):
        # 获取path的文件名
        file_name = path.rsplit('/', 1)[-1]
        file_name = file_name.rsplit('.',1)[0]
        # 遍历list_widget中的item，如果item的文件名与path的文件名相同，则将item的label_path设置为path
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.info['file_name'] == file_name:
                if path.endswith('.txt'):
                    if not os.path.exists(self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']):
                        os.makedirs(self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path'])
                    shutil.copy(path, self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+path.rsplit('/', 1)[-1])
                    item.info['label_path_txt'] = self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+path.rsplit('/', 1)[-1]
                    self.update_both_label(item,from_ = 'txt')
                    item.update_label_stat('labeled')
                    item.update_label_stat(stat)
                elif path.endswith('.json'):
                    if not os.path.exists(self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']):
                        os.makedirs(self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path'])
                    shutil.copy(path, self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+path.rsplit('/', 1)[-1])
                    item.info['label_path_json'] = self.parent().left_bottom_widget.left_bottom_widget.settings['label_saved_path']+path.rsplit('/', 1)[-1]
                    self.update_both_label(item,from_ = 'json')
                    item.update_label_stat('labeled')
                    item.update_label_stat(stat)
                else:
                    print('label file format error')
                    return
                break
    
    def remove_item(self):
        # get selected item
        item = self.list_widget.currentItem()
        # check if any item is selected
        if item:
            # get the row number of the selected item
            row = self.list_widget.row(item)
            #remove cache label file
            if item.info['label_path_txt'] is not None:
                os.remove(item.info['label_path_txt'])
            if item.info['label_path_json'] is not None:
                os.remove(item.info['label_path_json'])
            # remove the item
            self.list_widget.takeItem(row)
        else:
            print('no item selected')
    
    def remove_item_all(self):
        self.list_widget.clear()
        
    def select_on_file_list_item(self):
        item = self.list_widget.currentItem()
        self.click_on_file_list_item(item)
        
    def click_on_file_list_item(self, item):
        if item!=None:
            if item.info['label_stat'] is None or item.info['label_stat'] == 'error':
                self.parent().right_widget.show_image(item.info['file_path'])
            else:
                if item.info['label_path_json'] is not None:
                    if os.path.exists(item.info['label_path_json']):
                        item_fig = utils.visuallize_label_file_on_image(item.info['label_path_json'],
                                                                        item.info['file_path'], label_list=
                                                                        self.parent().left_bottom_widget.left_bottom_widget.settings[
                                                                            'label_list'])
                        self.parent().right_widget.show_image(item_fig)
                    if not os.path.exists(item.info['label_path_json']):
                        print('label file not exist')
                        item.update_label_stat('error')
                        self.click_on_file_list_item(item)
    
    def show_right_menu(self, pos):
        # 获取鼠标点击的位置
        global_pos = self.list_widget.mapToGlobal(pos)
        # 获取点击的item
        item = self.list_widget.itemAt(pos)
        if item:
            menu = QMenu()
            # 添加文件
            addfile_action = QAction('addfile')
            addfile_submenu = QMenu('addfile')
            submenu_additem = addfile_submenu.addAction('add item')
            submenu_additem.triggered.connect(lambda: self.parent().add_item())
            submenu_batch_additem = addfile_submenu.addAction('add items')
            submenu_batch_additem.triggered.connect(lambda: self.parent().batch_add_item())
            addfile_action.setMenu(addfile_submenu)
            menu.addAction(addfile_action)
            
            
            state_action = QAction('label_state')
            state_submenu = QMenu('label_state')
            
            # 修改label_state
            set_state_None = state_submenu.addAction('None:rm label')
            set_state_None.triggered.connect(lambda: item.update_label_stat(None))
            set_state_labeled = state_submenu.addAction('labeled')
            set_state_labeled.triggered.connect(lambda: item.update_label_stat('labeled'))
            set_state_check = state_submenu.addAction('manual_checked')
            set_state_check.triggered.connect(lambda: item.update_label_stat('manual_checked'))
            set_state_error = state_submenu.addAction('error')
            set_state_error.triggered.connect(lambda: item.update_label_stat('error'))
            state_action.setMenu(state_submenu)
            menu.addAction(state_action)

            if item.info['label_path_txt'] is not None:
                #加入文件夹
                move_to_folder_action = QAction('move to folder')
                move_to_folder_submenu = QMenu('move to folder')
                submenu_move_to_folder_item_list = []

                file_groups = self.parent().left_bottom_widget.tab1_tree.get_groups()
    
                for group_item in file_groups:
                    submenu_move_to_folder_item_list.append(move_to_folder_submenu.addAction(group_item.info['group_name']))
                for i in range(len(submenu_move_to_folder_item_list)):
                    submenu_move_to_folder_item_list[i].triggered.connect(lambda state, group = file_groups[i]: self.move_to_folder(item, group))
                move_to_folder_action.setMenu(move_to_folder_submenu)
                menu.addAction(move_to_folder_action)
            
            # 删除文件
            menu.addAction('remove', self.remove_item)
            menu.addAction('remove all', self.remove_item_all)
            menu.exec(global_pos)
        #
        else:
            menu = QMenu()
            
            addfile_action = QAction('addfile')
            addfile_submenu = QMenu('addfile')
            submenu_additem = addfile_submenu.addAction('add item')
            submenu_additem.triggered.connect(lambda: self.parent().add_item())
            submenu_batch_additem = addfile_submenu.addAction('add items')
            submenu_batch_additem.triggered.connect(lambda: self.parent().batch_add_item())
            addfile_action.setMenu(addfile_submenu)
            menu.addAction(addfile_action)
            
            menu.addAction('remove', self.remove_item)
            menu.addAction('remove all', self.remove_item_all)

            menu.exec(global_pos)
    
    def move_to_folder(self, item, group):
        child_item = TreeWidgetChild(group,item)
        group.addChild(child_item)
    
    def update_both_label(self,item,from_):
        if from_ == 'txt':
            new_json = self.shift_label_file(item.info['label_path_txt'],item.info['file_path'])
            item.info['label_path_json'] = new_json
        elif from_ == 'json':
            new_txt = self.shift_label_file(item.info['label_path_json'],item.info['file_path'])
            item.info['label_path_txt'] = new_txt
        else:
            print('up date error')
            return
        
    # def check_both_label(self,item):
    #     if item.info['label_path_txt'] is not None and item.info['label_path_json'] is not None:
    #         return True
    #     elif item.info['label_path_txt'] is not None and item.info['label_path_json'] is None:
    #         new_json = self.shift_label_file(item.info['label_path_txt'],item.info['file_path'])
    #         item.info['label_path_json'] = new_json
    #     elif item.info['label_path_txt'] is None and item.info['label_path_json'] is not None:
    #         new_txt = self.shift_label_file(item.info['label_path_json'],item.info['file_path'])
    #         item.info['label_path_txt'] = new_txt
    #     else:
    #         print('no label file')
    #         return False
            
    def shift_label_file(self,path,img_path):
        '''
        
        :param path:label cache path copy from raw label
        :return: another form of label file in label cache path fill all type of label
        '''
        
        #check whether path endwith txt or json
        if path.endswith('.txt'):
            output_cache_label = path.replace('.txt','.json')
            utils.saveyolo2labelme(path,output_cache_label,img_path,label_list=self.parent().left_bottom_widget.left_bottom_widget.settings['label_list'])
            return output_cache_label
        elif path.endswith('.json'):
            output_cache_label = path.replace('.json','.txt')
            utils.savelabelme2yolo(path,output_cache_label,label_list=self.parent().left_bottom_widget.left_bottom_widget.settings['label_list'])
            return output_cache_label
        else:
            print('label file format error')
            return
        
        
class LeftBottomTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        self.info = 'left bottom tab widget'
        
        #分组作图tab
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        # 工具栏
        self.Leftbottomtoolbar = LeftBottomTabWidget_BottomSubwidget(self)
        # treewidget
        self.tab1_tree = LeftBottomWidget_Treewidget(self)
        #当前选中的item，触发函数
        self.tab1_tree.itemClicked.connect(self.tab1_tree.top_item_click)
        

        self.tab1_layout.addWidget(self.Leftbottomtoolbar)
        self.tab1_layout.addWidget(self.tab1_tree)
        self.tab1.setLayout(self.tab1_layout)

        #tab2
        self.left_bottom_widget = LeftBottomWidget()
        
        self.addTab(self.tab1, 'explore')
        self.addTab(self.left_bottom_widget, 'Train cfg')

 
class LeftBottomTabWidget_BottomSubwidget(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.info = 'left bottom tab widget bottom subwidget'
        
        self.parent = parent
        #一个工具栏
        self.toolbar = QToolBar()
        #加一个按钮
        self.toolbar.addAction('Create_Group', self.add_group)
        self.toolbar.addAction('Summary_Checked',self.group_summary)
        #一个布局
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.toolbar)
        
        self.setLayout(self.layout)
        
    def add_group(self):
        self.parent.tab1_tree.add_group()
  
    def group_summary(self):
        self.parent.tab1_tree.batch_status()
  
  
class LeftBottomWidget_Treewidget(QTreeWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.parent = parent
        self.setColumnCount(1)
        self.setHeaderLabels(['label'])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.setAlternatingRowColors(True)
        self.setAnimated(True)
        
        #右键菜单
        self.customContextMenuRequested.connect(self.right_menu)
        # self.itemClicked.connect(self.item_click)
        #黑色背景
        self.setStyleSheet("background-color:rgb(0,0,0)")
        # classA = QTreeWidgetItem(self, ["Class A"])
        # for i in range(5):
        #     item = QTreeWidgetItem(classA, ["Class A Item {}".format(i+1)])
        #     classA.addChild(item)
    
    def get_groups(self):
        count = self.topLevelItemCount()
        groups = []
        i_tem = []
        for i in range(count):
            item = self.topLevelItem(i)
            i_tem.append(item)
            groups.append(item.info['group_name'])
        return i_tem
        
    def add_group(self):
        print('add group')
        g_name = 'None'
        #弹窗填写group名字
        dialog = QDialog()
        dialog.setWindowTitle('group name')
        dialog.resize(300, 100)
        layout = QVBoxLayout()
        label = QLabel('group name')
        line_edit = QLineEdit()
        button = QPushButton('ok')
        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)
        dialog.setLayout(layout)
        button.clicked.connect(lambda:dialog.close())
        dialog.exec_()
        g_name = line_edit.text()
        if g_name != '':
            item = TreeWidgetItem(self, {'group_name': g_name})
        
    def test(self):
        #显示当前所有的item
        count = self.topLevelItemCount()
        for i in range(count):
            item = self.topLevelItem(i)
            print(item.info['group_name'])
            # 处理 item
            
    def del_group(self,item):
        #移除当前选中item
        self.takeTopLevelItem(self.indexOfTopLevelItem(item))
    
    def del_item(self,item):
        #从item的父节点中移除item
        item.parent().removeChild(item)
    
    def right_menu(self,pos):
        global_pos = self.mapToGlobal(pos)
        #获取当前选中的item
        item = self.itemAt(pos)
        if item is None:
            print('no item')
        else:
            #右键菜单
            if self.check_top_item(item):
                menu = QMenu()
                del_group = menu.addAction('del group')
                del_group.triggered.connect(lambda:self.del_group(item))
                menu.exec_(QCursor.pos())
            else:
                menu = QMenu()
                del_group = menu.addAction('del item')
                del_group.triggered.connect(lambda: self.del_item(item))
                menu.exec_(QCursor.pos())
                
    def top_item_click(self,item):
        #判断item是否为top item
        if self.check_top_item(item):
            #获取当前选中的item的所有子item
            count = item.childCount()
            if count == 0:
                print('no child')
            else:
                dict_stat = self.get_dict_item([item])
                fig,res_df = utils.stat_summary(dict_stat)
                if fig:
                    self.parent.parent().info_table.show_stats(res_df)
                    self.parent.parent().right_widget.show_image(fig)
                
        else:
            dict_stat = {}
            dict_stat[item.parent().info['group_name']] = [item.info['label_path_txt']]
            fig,res_df = utils.stat_summary(dict_stat)
            if fig:
                self.parent.parent().info_table.show_stats(res_df)
                self.parent.parent().right_widget.show_image(fig)

    def batch_status(self):
        # 所有checkbox的状态
        count = self.topLevelItemCount()
        check_list = []
        for i in range(count):
            item = self.topLevelItem(i)
            if item.checkbox.isChecked():
                # 处理 item
                check_list.append(item)
        if len(check_list) == 0:
            print('no checked')
            return
        dict_stat = self.get_dict_item(check_list)
        fig,res_df = utils.stat_summary(dict_stat)
        if fig:
            self.parent.parent().info_table.show_stats(res_df)
            self.parent.parent().right_widget.show_image(fig)
    
    def get_dict_item(self,list_item):
        d_out = {}
        for item in list_item:
            k = item.info['group_name']
            n = item.childCount()
            v = []
            if n == 0:
                print('no child')
                continue
            else:
                for i in range(n):
                    child = item.child(i)
                    v.append(child.info['label_path_txt'])
                d_out[k] = v
        return d_out
    
    def check_top_item(self,item):
        #判断item是否为top item
        if item.parent() is None:
            return True
        else:
            return False
   
            
class TreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, info):
        super().__init__(parent)
        
        self.info = info
        #定义treewidgetitem的layout
        self.layout = QHBoxLayout()
        #定义treewidgetitem的widget
        self.widget = QWidget()
        #定义treewidgetitem的label,双击可以编辑
        self.label = QLabel(self.info['group_name'])
        
        # self.label.setFixedHeight(30)
        # self.label.setFixedWidth(200)
        self.label.setAlignment(Qt.AlignCenter)
        
        #加入一个checkbox
        self.checkbox = QCheckBox()
        #固定大小
        self.checkbox.setFixedSize(30,30)
        
        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.label)
        #最右边加一个空白
        self.layout.addStretch()
        
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        
        self.setSizeHint(0, QSize(0, 30))
        self.treeWidget().setItemWidget(self, 0, self.widget)
        
        
    def add_item(self, item):
        item = QTreeWidgetItem(self, item)
        #点击item时触发
        item.clicked.connect(self.parent().sub_item_click)
        self.addChild(item)
        
        
class TreeWidgetChild(QTreeWidgetItem):
    def __init__(self, parent, item):
        super().__init__(parent)
        self.item_ = item
        self.info = self.item_.info
        #设置label
        self.setText(0, self.info['file_name'])
    
    
class LeftBottomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.settings = {
            'yolo_path': './yolov_res/models/weight/default_model/yolo.pt',
            'res_path': './yolov_res/models/weight/default_model/res.pt',
            'pretrain_path': './yolov_res/models/weight/pretrain_X.pt',
            'epoch': 10,
            'lr': 0.0001,
            'batch_size': 32,
            'num_workers': 4,
            'save_interval': 10,
            'save_path': './checkpoints/',
            'cache_path': './yolov_res/cache/',
            'label_saved_path': './label_cache/',
            'yolo_model_saved_path': './model_cache/yolo_weights/',
            'res_model_saved_path': './model_cache/res_weights/',
            'label_list': ['cell','dead','test','test1']
            }
        
        #清空cache
        print(os.path.abspath(self.settings['cache_path']))
        if os.path.exists(self.settings['cache_path']):
            shutil.rmtree(self.settings['cache_path'])
        os.mkdir(self.settings['cache_path'])
        if os.path.exists(self.settings['label_saved_path']):
            shutil.rmtree(self.settings['label_saved_path'])
        os.mkdir(self.settings['label_saved_path'])
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create title label
        title_label = QLabel('Trainning Parameters', self)
        # 好看一点的title
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)
        
        #一个widget，左边有加减两个小按钮右边是一个combobox
        yolo_select_widget = QWidget()
        yolo_select_layout = QHBoxLayout()
        yolo_select_widget.setLayout(yolo_select_layout)
        yolo_select_layout.addWidget(QLabel('Yolo.pt:'))
        
        #button设置最小值且没有间距
        yolo_select_button_1 = QPushButton('+')
        yolo_select_button_1.setFixedWidth(30)
        yolo_select_button_1.clicked.connect(self.select_yolo_path_add)
        
        yolo_select_button_2 = QPushButton('-')
        yolo_select_button_2.setFixedWidth(30)
        yolo_select_button_2.clicked.connect(self.select_yolo_path_sub)
        
        self.yolo_select_combobox = QComboBox()
        
        #设置默认值
        self.yolo_select_combobox.addItem('None')
        self.yolo_select_combobox.addItem(self.settings['yolo_path'])
        self.yolo_select_combobox.addItem(self.settings['pretrain_path'])
        self.yolo_select_combobox.setCurrentIndex(1)
        #从后显示
        # self.yolo_select_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.yolo_select_combobox.setMaxVisibleItems(10)
        # self.yolo_select_combobox.setInsertPolicy(QComboBox.InsertAtBottom)
        self.yolo_select_combobox.setEditable(True)
        self.yolo_select_combobox.lineEdit().setReadOnly(True)
        self.yolo_select_combobox.lineEdit().setAlignment(Qt.AlignRight)
        #combobox选中的值改变时触发
        self.yolo_select_combobox.currentIndexChanged.connect(self.yolo_select_combobox_changed)
        #combobox占2/3
        yolo_select_layout.addWidget(self.yolo_select_combobox,9)
        yolo_select_layout.addWidget(yolo_select_button_1)
        yolo_select_layout.addWidget(yolo_select_button_2)
        
        #加入model_saved_path中的模型路径
        for file in os.listdir(self.settings['yolo_model_saved_path']):
            if file.endswith('.pt'):
                self.add_yolo_path(self.settings['yolo_model_saved_path']+file,set_current = True)
                
        layout.addWidget(yolo_select_widget)
        
        '''res.pt selectwidget'''
        # 一个widget，左边有加减两个小按钮右边是一个combobox
        res_select_widget = QWidget()
        res_select_layout = QHBoxLayout()
        res_select_widget.setLayout(res_select_layout)
        res_select_layout.addWidget(QLabel('Res.pt:'))

        # button设置最小值且没有间距
        res_select_button_1 = QPushButton('+')
        res_select_button_1.setFixedWidth(30)
        res_select_button_1.clicked.connect(self.select_res_path_add)

        res_select_button_2 = QPushButton('-')
        res_select_button_2.setFixedWidth(30)
        res_select_button_2.clicked.connect(self.select_res_path_sub)

        self.res_select_combobox = QComboBox()

        # 设置默认值
        self.res_select_combobox.addItem('None')
        #设置默认为self.settings['res_path']
        self.res_select_combobox.addItem(self.settings['res_path'])
        #默认选中respath
        self.res_select_combobox.setCurrentIndex(1)
        # 从后显示
        # self.yolo_select_combobox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.res_select_combobox.setMaxVisibleItems(10)
        # self.yolo_select_combobox.setInsertPolicy(QComboBox.InsertAtBottom)
        self.res_select_combobox.setEditable(True)
        self.res_select_combobox.lineEdit().setReadOnly(True)
        self.res_select_combobox.lineEdit().setAlignment(Qt.AlignRight)
        # combobox选中的值改变时触发
        self.res_select_combobox.currentIndexChanged.connect(self.res_select_combobox_changed)
        for file in os.listdir(self.settings['res_model_saved_path']):
            if file.endswith('.pt'):
                self.add_res_path(self.settings['res_model_saved_path']+file,set_current = True)

        # combobox占2/3
        res_select_layout.addWidget(self.res_select_combobox, 9)
        res_select_layout.addWidget(res_select_button_1)
        res_select_layout.addWidget(res_select_button_2)

        layout.addWidget(res_select_widget)
        '''好了'''
        

        # 一个button开启一个新的窗口，修改其他的参数
        button_config = QPushButton('Config')
        button_config.clicked.connect(self.open_config_window)
        self.config_info = QLabel('Config Info')
        self.update_config_info()
        # layout.addWidget(button_yolo)
        layout.addWidget(button_config)
        layout.addWidget(self.config_info)
        self.setLayout(layout)
    
    def get_trainning_config(self):
        return self.settings
    
    def select_res_path_add(self):
        # 选择本地模型路径
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if file_path:
            self.settings['res_path'] = file_path
            # combobox加入并选中新的路径
            self.res_select_combobox.addItem(self.settings['res_path'])
            self.res_select_combobox.setCurrentIndex(self.res_select_combobox.count()-1)
            
    def add_res_path(self,path,set_current=True):
        self.settings['res_path'] = path
        # combobox加入并选中新的路径
        self.res_select_combobox.addItem(path)
        if not set_current:
            self.res_select_combobox.setCurrentIndex(self.res_select_combobox.count()-1)
            
    def select_res_path_sub(self):
        #判断是否有当前路径
        if self.settings['res_path'] in self.res_select_combobox.currentText():
            #判断路径是否='None'
            if self.res_select_combobox.currentText()!='None':
                #判断是否只有一个路径
                if self.res_select_combobox.count()>1:
                    #删除当前路径
                    self.res_select_combobox.removeItem(self.res_select_combobox.currentIndex())
                    #若删除的是最后一个路径，设置当前路径为倒数第二个路径
                    if self.res_select_combobox.currentIndex()==self.res_select_combobox.count():
                        self.res_select_combobox.setCurrentIndex(self.res_select_combobox.count()-1)
                    #若删除的是第一个路径，设置当前路径为第二个路径
                    elif self.res_select_combobox.currentIndex()==0:
                        self.res_select_combobox.setCurrentIndex(0)
                        #若删除的是中间路径，设置当前路径为删除路径的下一个路径
                    else:
                        self.res_select_combobox.setCurrentIndex(self.res_select_combobox.currentIndex())
                else:
                    QMessageBox.warning(self, 'Warning', 'No other path')
            else:
                QMessageBox.warning(self, 'Warning', 'No path')
                
    def res_select_combobox_changed(self):
        if self.res_select_combobox.currentText()=='None':
            self.settings['res_path']=None
        else:
            self.settings['res_path'] = self.res_select_combobox.currentText()
        print(self.settings['res_path'])
        
    def yolo_select_combobox_changed(self):
        if self.yolo_select_combobox.currentText()=='None':
            self.settings['yolo_path']=None
        else:
            self.settings['yolo_path'] = self.yolo_select_combobox.currentText()
        print(self.settings['yolo_path'])
        
    def select_yolo_path_add(self):
        # 选择本地模型路径
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if file_path:
            self.settings['yolo_path'] = file_path
            # combobox加入并选中新的路径
            self.yolo_select_combobox.addItem(self.settings['yolo_path'])
            self.yolo_select_combobox.setCurrentIndex(self.yolo_select_combobox.count()-1)
    
    def add_yolo_path(self,path,set_current=True):
        self.settings['yolo_path'] = path
        # combobox加入并选中新的路径
        self.yolo_select_combobox.addItem(path)
        if not set_current:
            self.yolo_select_combobox.setCurrentIndex(self.yolo_select_combobox.count()-1)
        
    def select_yolo_path_sub(self):
        #判断路径是否='None'
        if self.yolo_select_combobox.currentText()!='None':
            #判断是否有当前路径
            if self.settings['yolo_path'] in self.yolo_select_combobox.currentText():
                #判断是否只有一个路径
                if self.yolo_select_combobox.count()>1:
                    #删除当前路径
                    self.yolo_select_combobox.removeItem(self.yolo_select_combobox.currentIndex())
                    #若删除的是最后一个路径，设置当前路径为倒数第二个路径
                    if self.yolo_select_combobox.currentIndex()==self.yolo_select_combobox.count():
                        self.yolo_select_combobox.setCurrentIndex(self.yolo_select_combobox.count()-1)
                    #若删除的是第一个路径，设置当前路径为第二个路径
                    elif self.yolo_select_combobox.currentIndex()==0:
                        self.yolo_select_combobox.setCurrentIndex(0)
                        #若删除的是中间路径，设置当前路径为删除路径的下一个路径
                    else:
                        self.yolo_select_combobox.setCurrentIndex(self.yolo_select_combobox.currentIndex())
                else:
                    QMessageBox.warning(self, 'Warning', 'No other path')
        else:
            QMessageBox.warning(self, 'Warning', 'No path')
            
    def update_config_info(self):
        # 好看一点的label
        self.config_info.setText(f'Epoch         \t: {self.settings["epoch"]} \n'
                                 f'Learning Rate\t: {self.settings["lr"]} \n'
                                 f'Batch Size\t: {self.settings["batch_size"]} \n'
                                 f'Save Path\t: {self.settings["save_path"]} \n'
                                 )
        
        self.config_info.setStyleSheet("font-size: 15px; font-weight: bold;")
    
    def open_config_window(self):
        # 开启一个Qdialog
        dialog = QDialog(self)
        
        # dialog中展示所有setting参数
        layout = QVBoxLayout()

        # 固定间隔拖拽条选择epoch
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(1000)
        slider.setValue(self.settings['epoch'])
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(100)
        slider.valueChanged.connect(self.change_epoch)
        layout_epoch = QHBoxLayout()
        label_txt = QLabel('Epoch: ')
        layout_epoch.addWidget(label_txt)
        # 展示当前数值随着slider的变化而变化
        label = QLabel(str(self.settings['epoch']))
        layout_epoch.addWidget(label)
        # 设置label的数值随着slider的变化而变化
        slider.valueChanged.connect(label.setNum)

        # 手动输入lr，左边为label，右边为lineedit
        layout_lr = QHBoxLayout()
        label_txt = QLabel('Learning Rate: ')
        layout_lr.addWidget(label_txt)
        lineedit = QLineEdit()
        lineedit.setText(str(self.settings['lr']))
        layout_lr.addWidget(lineedit)
        # 修改lr时，更新settings
        #如果输入的不是float，就不更新
        # lineedit.textChanged.connect(lambda: self.settings.update({'lr': lineedit.text()}))
        lineedit.textChanged.connect(lambda: self.settings.update({'lr': float(lineedit.text())}) if lineedit.text().replace('.', '', 1).isdigit() else 0.001)

        # spinbox选择batch_size
        layout_batch = QHBoxLayout()
        label_txt = QLabel('Batch Size: ')
        layout_batch.addWidget(label_txt)
        spinbox = QSpinBox()
        spinbox.setMinimum(1)
        spinbox.setMaximum(1000)
        spinbox.setValue(self.settings['batch_size'])
        layout_batch.addWidget(spinbox)
        # 修改batch_size时，更新settings
        #如果是数字就修改不然不修改
        spinbox.valueChanged.connect(lambda: self.settings.update({'batch_size': spinbox.value()}) if spinbox.text().isdigit() else self.settings['batch_size'])
        # 垂直布局，上面为label，下面为Qpushbutton选择文件夹
        layout_savepath = QHBoxLayout()
        label_txt = QLabel('Save Path')
        layout_savepath.addWidget(label_txt)
        button = QPushButton(self.settings['save_path'])
        layout_savepath.addWidget(button)
        # 修改save_path时，更新settings,同时更新button的显示
        button.clicked.connect(lambda: self.settings.update({'save_path': QFileDialog.getExistingDirectory()}))
        button.clicked.connect(lambda: button.setText(self.settings['save_path']))
        
        layout.addLayout(layout_epoch)
        layout.addWidget(slider)
        layout.addLayout(layout_lr)
        layout.addLayout(layout_batch)
        layout.addLayout(layout_savepath)
        
        config_layout_right = QVBoxLayout()
        table = label_list_table(dialog)
        #右键打开menu
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(table.show_menu)

        config_layout_right.addWidget(table)
        
        config_main_layout = QHBoxLayout()
        config_main_layout.addLayout(layout)
        config_main_layout.addLayout(config_layout_right)
        dialog.setLayout(config_main_layout)
        dialog.exec_()
        print(self.settings)
        self.update_config_info()
        
    def change_epoch(self, value):
        self.settings['epoch'] = value

    def label_pair_modified(self, item):
        # 修改label时，更新settings
        print(item.row(), item.column())
        if item.column() == 0:
            print('先别改,没写完呢')
        else:
            #判断token是否是数字
            if item.text().isdigit():
                #判断token是否已经存在
                if int(item.text()) in self.settings['label_pairs'].values():
                    #弹窗提示token已经存在，询问是否需要合并label
                    reply = QMessageBox.question(self, 'Message', 'token already exists, do you want to merge labels?',
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        print(1)
                    else:
                        self.settings['label_pairs'][item.tableWidget().item(item.row(), 0).text()] = int(item.text())
            else:
                #弹窗提示token必须是数字
                QMessageBox.warning(self, 'Warning', 'token must be a number')
                item.setText(str(self.settings['label_pairs'][item.tableWidget().item(item.row(), 0).text()]))
        print(self.settings['label_pairs'])


class label_list_table(QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setRowCount(parent.parent().settings['label_list'].__len__())
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(['label'])
        self.default_height = 50

        self.horizontalHeader().setVisible(True)
        self.verticalHeader().setVisible(True)
        self.verticalHeader().setDefaultSectionSize(self.default_height)

        # 启用拖放功能
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        
        for i, label in enumerate(parent.parent().settings['label_list']):
            item = QTableWidgetItem(label)
            # item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.setItem(i, 0, item)
            
    def show_menu(self, pos):
        global_pos = self.mapToGlobal(pos)
        menu = QMenu(self.parent)
        item = self.itemAt(pos)
        if item:
            menu.addAction('Delete', lambda: self.delete_row(item))
            menu.addAction('Add', lambda: self.add_row(item))
            menu.addAction('Edit', lambda: self.edit_row(item))
        else:
            menu.addAction('Add', lambda: self.add_row(None))

        menu.exec(global_pos)
        
    def edit_row(self, item):
        row = item.row()
        dialog = QDialog()
        dialog.setWindowTitle('Edit Label')
        dialog.resize(300, 100)
        layout = QVBoxLayout()
        lineedit = QLineEdit()
        lineedit.setText(item.text())
        layout.addWidget(lineedit)
        button = QPushButton('OK')
        layout.addWidget(button)
        dialog.setLayout(layout)
        button.clicked.connect(lambda: item.setText(lineedit.text()))
        button.clicked.connect(lambda: self.parent.parent().settings['label_list'].pop(row))
        button.clicked.connect(lambda: self.parent.parent().settings['label_list'].insert(row, lineedit.text()))
        button.clicked.connect(dialog.close)
        dialog.exec_()
        
    def delete_row(self, item):
        row = item.row()
        self.removeRow(row)
        self.parent.parent().settings['label_list'].pop(row)
        print(self.parent.parent().settings['label_list'])
        
    def add_row(self, item):
        if item is None:
            row = 0
        else:
            row = item.row()
        self.insertRow(row)
        new_item = QTableWidgetItem('new_label')
        self.setItem(row, 0, new_item)
        self.parent.parent().settings['label_list'].insert(row, 'new_label')
        print(self.parent.parent().settings['label_list'])
        
        
    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        pos = event.pos()
        index = self.indexAt(pos)
        row = index.row() if not index.isValid() else index.row() + 1
        if row == -1:
            return
        else:
            # 获取拖拽的行号
            source_row = event.source().currentRow()
            # 获取row与row-1的rowViewportPosition
            start = self.rowViewportPosition(row - 1)
            # 获取每个row的高度
            end = start + self.default_height
            # 判断放置位置
            if pos.y() < 0.5 * (start + end):
                row -= 1
                # 移动行
            self.insertRow(row)
            if source_row > row:
                source_row += 1
            for col in range(self.columnCount()):
                item = self.takeItem(source_row, col)
                self.setItem(row, col, item)
            self.removeRow(source_row)
            
            #获取当前label_list_table的顺序
            label_list = []
            for i in range(self.rowCount()):
                label_list.append(self.item(i, 0).text())
            self.parent.parent().settings['label_list'] = label_list
            print(self.parent.parent().settings['label_list'])


class ImageWidget(QWidget):
    def __init__(self, path=None, parent=None):
        super().__init__(parent)
        # Create black background
        pixmap = QPixmap(self.size())
        pixmap.fill(QColor("black"))
        # If path is given, load image
        if path:
            pixmap = QPixmap(path)
        # Create label and set pixmap
        self.label = QLabel(self)
        self.label.setPixmap(pixmap)
        # Create layout and add label
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        # Set layout
        self.setLayout(layout)

    def show_image(self, image_item):
        '''
        show image by matplotlib figure or by path
        Args:
            image_item: str or matplotlib figure
            eg. image_item = 'path/to/image' or image_item = plt.figure()

        Returns:
            nothing XD!
        '''
        # show image by matplotlib figure or by path
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

        # Create label and set pixmap
        self.label.setPixmap(pixmap)
        # change image size to the widget size
        self.label.setScaledContents(True)
        # self.label.resize(self.size())
        # self.label.adjustSize()