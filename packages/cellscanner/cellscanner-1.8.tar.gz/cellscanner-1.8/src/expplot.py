import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# from CellDetect import settings
import numpy as np
import cv2
from matplotlib.pyplot import MultipleLocator
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def extract_info_from_path(dir_path):
    summary_info = []
    file_in_dir = [os.path.join(dir_path,_) for _ in os.listdir(dir_path) if not _.startswith('.')]
    for f in file_in_dir:
        info = extract_info_from_txt(f,dir_path.split('/')[-2])
        summary_info.append(info)
    return summary_info

def extract_info_from_dict(dict_x):
    summary_info = []
    for k in dict_x.keys():
        v = dict_x[k]
        for f in v:
            info = extract_info_from_txt(f,k)
            summary_info.append(info)
    return summary_info

def extract_info_from_txt(file_path,exp_name,aim_class = 1,radius_list = [2,4,6,8],sep = ' '):
    result = []

    result.append(exp_name)
    summary_data = []
    for line in open(file_path):
        if line[0]=='x':
            continue
        else:
            a = [float(_) for _ in line[:-1].split(sep=sep)]
            h_t,w_t = 640,640
            #补丁2 上面分割符如果是yolo直接用‘ ’
            #             a = sbckw2yolo_patch(a,h_t,w_t)
            summary_data.append(a)
    summary_data = np.array(summary_data)
    #计算细胞个数 和指定类别个数

    #细胞总个数
    result.append(summary_data.shape[0])

    norm_data = summary_data[summary_data[:,0]!=aim_class]
    aim_data = summary_data[summary_data[:,0]==aim_class]

    #细胞个数
    result.append(norm_data.shape[0])
    result.append(aim_data.shape[0])

    #细胞大小
    result.append(list(norm_data[:,3]*norm_data[:,4]))
    if aim_data.shape[0]!=0:
        result.append(list(aim_data[:,3]*aim_data[:,4]))

        #有效分数
        mean_radius_aim = (aim_data[:,3].mean()+aim_data[:,4].mean())/4
        distance_matrix = L2_dist_1(norm_data[:,1:3], aim_data[:,1:3])
        min_dis_tok = np.argmin(distance_matrix,axis = 1)
        effective_score = {}
        for effect_radius in radius_list:#针对目标多少倍半径内计算
            es = 0
            for i in range(len(min_dis_tok)):
                if distance_matrix[i,min_dis_tok[i]] < effect_radius*mean_radius_aim:
                    #有效分数连接线
                    es +=1
            effective_score[str(effect_radius)]=es/aim_data.shape[0]
        result.append(effective_score)
    else:
        result.append(-1)
        result.append(-1)
    return result
    #返回一个nparry


def sbckw2yolo_patch(label_info,h_t,w_t):
    _=[]
    _.append(label_info[5])
    _.append((label_info[0]+label_info[2])/(2*w_t))
    _.append((label_info[1]+label_info[3])/(2*h_t))
    _.append((label_info[2]-label_info[0])/w_t)
    _.append((label_info[3]-label_info[1])/h_t)
    _.append(label_info[-1])
    return _


def ckwpicresize_patch(pic_mat):
    pic_mat = cv2.resize(pic_mat,(640,640))
    return pic_mat,640,640


def get_effective_score(summary_data,aim_class):
    aim_cell = aim_class #针对的目标类别
    aim_data = summary_data[summary_data[:,0]==aim_cell]
    rest_data = summary_data[summary_data[:,0]!=aim_cell]

    mean_radius_aim = (aim_data[:,3].mean()+aim_data[:,4].mean())/4
    distance_matrix = L2_dist_1(rest_data[:,1:3], aim_data[:,1:3])
    min_dis_tok = np.argmin(distance_matrix,axis = 1)
    effective_score = {}
    for effect_radius in [2,4,6,8]:#针对目标多少倍半径内计算
        es = 0
        for i in range(len(min_dis_tok)):
            if distance_matrix[i,min_dis_tok[i]] < effect_radius*mean_radius_aim:
                #有效分数连接线
                es +=1
        effective_score[str(effect_radius)]=es/aim_data.shape[0]
    return effective_score


def L2_dist_1(cloud1, cloud2):
    m, n = len(cloud1), len(cloud2)
    cloud1 = np.repeat(cloud1, n, axis=0)
    cloud1 = np.reshape(cloud1, (m, n, -1))
    dist = np.sqrt(np.sum((cloud1 - cloud2)**2, axis=2))
    return dist


def draw_score_line(result,ax_,radius_list = [2,4,6,8]):
    c = {}
    result_ = result[result[:,-1]!=-1]
    for lab in np.unique(result_[:,0]):
        data_lab = result_[result_[:,0]==lab,6]

        v_ = []
        h_ = []
        l_ = []
        x_ = []
        m_ = []
        for samp in data_lab:
            for k in samp.keys():
                v_.append([int(k),samp[k]])
        v_ = np.array(v_)
        for k in radius_list:
            h_.append(np.max(v_[v_[:,0]==k,1]))
            l_.append(np.min(v_[v_[:,0]==k,1]))
            m_.append(np.mean(v_[v_[:,0]==k,1]))

        l = ax_.plot(radius_list,m_,marker = 'o',linestyle = '--',label=lab)
        c[lab]=l[0].get_color()
        ax_.fill_between(radius_list,l_,h_, alpha=0.05)
        ax_.legend(loc = 'upper left')
        ax_.set_xlabel('times of radius',fontsize = 15)
        ax_.set_ylabel('Effective Score',fontsize = 15)
    if c == {}:
        return False
    else:
        return c


def draw_cell_fraction(result_,ax_,c_):
    box_lab = []
    pos = []
    p = 0
    for lab in np.unique(result_[:,0]):
        box_val = []
        data_lab = result_[result_[:,0]==lab,1:4]
        pyro_rate = data_lab[:,2]/data_lab[:,0]
        box_val.append(list(pyro_rate))
        box_ = ax_.boxplot(box_val,positions = [p],boxprops={'color':c_[lab],'linewidth':2}
                           ,medianprops={'linestyle':':','linewidth':1,'color':'black'},
                           capprops={'color':c_[lab],'linewidth':2})
                           # capprops={'linewidth':2})
        
        #         for patch in box_['boxes']:
        #             patch.set_facecolor(c_[lab],alpha = 0.1)
        box_lab.append(lab)
        pos.append(p)
        p+=1
    ax_.set_xticklabels(box_lab,fontsize = 15,rotation=45,rotation_mode='default')
    ax_.set_ylabel('Proportion : pyro / norm',fontsize = 15)


def draw_cell_size(result_,ax_,c_):
    p = 0
    vio_lab =[]
    result_ = result_[result_[:,5]!=-1,:]
    for lab in np.unique(result_[:,0]):
        data_lab = result_[result_[:,0]==lab,4:6]
        data_n = []
        for _ in data_lab[:,0]:
            data_n+=_

        data_p = []
        for _ in data_lab[:,1]:
            data_p+=_
        mean_norm = np.mean(data_n)
        violin_n = ax_.violinplot(data_n/mean_norm,positions = [1.5*p-0.25])
        for patch in violin_n['bodies']:
            patch.set_facecolor('gray')
            patch.set_edgecolor('black')
        violin_n['cbars'].set_color('black')
        violin_n['cbars'].set_lw(1)
        violin_n['cbars'].set_ls('--')
        violin_n['cmaxes'].set_color('black')
        violin_n['cmaxes'].set_lw(1)
        violin_n['cmins'].set_color('black')
        violin_n['cmins'].set_lw(1)

        violin_p = ax_.violinplot(data_p/mean_norm,positions = [1.5*p+0.25])
        for patch in violin_p['bodies']:
            patch.set_facecolor(c_[lab])
            patch.set_edgecolor('black')

        violin_p['cbars'].set_color(c_[lab])
        violin_p['cbars'].set_lw(1)
        violin_p['cbars'].set_ls('--')
        violin_p['cmaxes'].set_color(c_[lab])
        violin_p['cmaxes'].set_lw(1)
        violin_p['cmins'].set_color(c_[lab])
        violin_p['cmins'].set_lw(1)
        p+=1
        vio_lab.append(lab)
    x = MultipleLocator(1.5)    # x轴每10一个刻度
    ax_.set_xticks([1.5*_ for _ in range(len(vio_lab))])
    ax_.set_xticklabels(vio_lab,fontsize = 15,rotation=45,rotation_mode='default')
    ax_.set_ylabel('Cell Size',fontsize = 15)


def plot_by_exp(exp_list, output_dir=None, radius_list = [2,4,6,8]):
    if isinstance(exp_list,str):
        exp_list = [exp_list+_+'/' for _ in os.listdir(exp_list) if not _.startswith('.')]
        print('get exp data from files dir')
    # elif isinstance(exp_root,list):
    #     print('exp root already list type')
    for exp_path in exp_list:
        try:
            result_all+=extract_info_from_path(exp_path)
        except:
            result_all = extract_info_from_path(exp_path)
    result_all = np.array(result_all,dtype=object)
    plt.figure(figsize = (18,8))
    ax1 = plt.subplot(2,2,1)
    ax2 = plt.subplot(2,2,3)
    c = draw_score_line(result_all,ax2)
    ax3 = plt.subplot(1,2,2)

    draw_cell_fraction(result_all,ax3,c)
    test = draw_cell_size(result_all,ax1,c)
    plt.tight_layout()
    if output_dir!=None:
        plt.savefig(output_dir,transparent=True)


# exp_root = 'Y:/work/c_celldetect/test_plot_data/txt/'
# exp_root = settings.MEDIA_ROOT + "/" + os.path.join("user") + "/"
# exp_list = [exp_root+_+'/' for _ in os.listdir(exp_root) if not _.startswith('.')]
# exp_list= []
# exp_list.append(exp_root)

# plot_by_exp('Y:/work/c_celldetect/test_plot_data/txt/')
# plot_by_exp(settings.MEDIA_ROOT + "/" + os.path.join("user") + "/", "./output.png")
# plot_by_exp(exp_list, "./output.png")


# exp_root = 'Y:/work/c_celldetect/test_plot_data/txt/'
# exp_list = [exp_root+_+'/' for _ in os.listdir(exp_root) if not _.startswith('.')]
# plot_by_exp(exp_list)

# print(extract_info_from_txt('/Users/zhuhanwen/Desktop/project/Celldetectproject/cdplus/codepyqt5/code/labels123/CP2.5_Image002_ch02.txt','test',aim_class = 1,radius_list = [2,4,6,8],sep = ' '))