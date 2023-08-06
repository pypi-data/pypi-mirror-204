import torch
from tqdm import tqdm
import sys
import torch.optim as optim
from code.yolov_res.model_cls.dataset import ImageDataset
from torch.utils.data import DataLoader
import numpy as np
import warnings
from code.yolov_res.model_cls.resnet import resnet34

warnings.filterwarnings("ignore")
import datetime
cls = ['cell', 'dead']


def train_one_epoch(model, optimizer, data_loader, device, epoch):
    model.train()

    loss_function = torch.nn.CrossEntropyLoss()
    loss_function.to(device)

    accu_loss = torch.zeros(1).to(device)  # 累计损失
    accu_num = torch.zeros(1).to(device)  # 累计预测正确的样本数
    optimizer.zero_grad()

    sample_num = 0
    data_loader = tqdm(data_loader, file=sys.stdout)
    for step, data in enumerate(data_loader):
        # print(step)
        images, label = data
        # print(label)
        sample_num += images.shape[0]
        label = torch.tensor(label, dtype=torch.long)
        pred = model(images.to(torch.float32).to(device))
        pred_classes = torch.max(pred, dim=1)[1]
        # print(pred_classes)
        accu_num += torch.eq(pred_classes, label.to(device)).sum()
        loss = loss_function(pred, label.to(device))
        loss.backward()
        accu_loss += loss.detach()
        data_loader.desc = "[train epoch {}] loss: {:.3f}, acc: {:.3f}".format(epoch,
                                                                               accu_loss.item() / (step + 1),
                                                                               accu_num.item() / sample_num)
        optimizer.step()
        optimizer.zero_grad()
        
    pred_cell = [cls[i] for i in list(np.array(torch.Tensor.cpu(pred_classes)))]

    # print("True:", label)
    # print("Pred:", pred_cell)

    return accu_loss.item() / (step + 1), accu_num.item() / sample_num



@torch.no_grad()
def evaluate(model, data_loader, device, epoch):
    model.eval()
    loss_function = torch.nn.CrossEntropyLoss()
    loss_function.to(device)
    accu_num = torch.zeros(1).to(device)  # 累计预测正确的样本数
    accu_loss = torch.zeros(1).to(device)  # 累计损失

    sample_num = 0
    data_loader = tqdm(data_loader, file=sys.stdout)
    for step, data in enumerate(data_loader):
        images, label = data
        sample_num += images.shape[0]
        label = torch.tensor(label, dtype=torch.long)
        pred = model(images.to(torch.float32).to(device))

        pred_classes = torch.max(pred, dim=1)[1]
        accu_num += torch.eq(pred_classes, label.to(device)).sum()

        loss = loss_function(pred, label.to(device))
        accu_loss += loss

        data_loader.desc = "[valid epoch {}] loss: {:.3f}, acc: {:.3f}".format(epoch,
                                                                               accu_loss.item() / (step + 1),
                                                                               accu_num.item() / sample_num)

    pred_cell = [cls[i] for i in list(np.array(torch.Tensor.cpu(pred_classes)))]
    # print("  True:", label)
    # print("  Pred:", pred_cell)
    # print()
    return accu_loss.item() / (step + 1), accu_num.item() / sample_num

# def main(train_pic_path,train_label_path,valid_pic_path,valid_label_path,output_path,weight = None,lr = 0.001,freeze = True):
def main(data_yaml, output_path, name, weight=None, lr=0.001,
             freeze=True,epoch = 10):
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # prefix = str(datetime.datetime.now().year) + \
    #          str(datetime.datetime.now().day) + \
    #          str(datetime.datetime.now().hour)
    # if not os.path.exists(f'F:/yolov5-master/model_cls/_saved/weight_{prefix}/'):
    #     os.makedirs(f'F:/yolov5-master/model_cls/_saved//weight_{prefix}/')
    # if not os.path.exists(f'F:/yolov5-master/model_cls/_saved/lossandacc_{prefix}/'):
    #     os.makedirs(f'F:/yolov5-master/model_cls/_saved/lossandacc_{prefix}/')



    train_data_list = data_yaml['train']
    valid_data_list = data_yaml['val']
    
    train_dataset = ImageDataset(train_data_list,prefix='train')
    valid_dataset = ImageDataset(valid_data_list,prefix='valid')
    
    batch_size = 32
    epochs = epoch
    period = 5


    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(valid_dataset, batch_size=batch_size, shuffle=False)
    
    print('train data size: ', len(train_dataset))
    print('valid data size: ', len(valid_dataset))
    
    model = resnet34()
    if weight!= None:
        model.load_state_dict(torch.load(weight, map_location=device))
        print('load weight: ', weight)
        
    if freeze:
        # print('Train resnet: Freezing layers')
        for i, (k, v) in enumerate(model.named_parameters()):
            if i <= 86:
                v.requires_grad = False
                print('Freeze layer: ', k)
                
    model.to(device)

    train_loss_list = {}
    train_acc_list = {}

    valid_loss_list = {}
    valid_acc_list = {}


        
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = optim.Adam(params, lr=lr)

    best_loss =np.inf

    for epoch in range(1, epochs + 1):
        train_loss, train_acc = train_one_epoch(model=model,
                                                optimizer=optimizer,
                                                data_loader=train_loader,
                                                device=device,
                                                epoch=epoch)

        train_loss_list[epoch] = train_loss
        train_acc_list[epoch] = train_acc

        valid_loss, valid_acc = evaluate(model=model,
                                         data_loader=valid_loader,
                                         device = device,
                                         epoch = epoch)
        valid_loss_list[epoch] = valid_loss
        valid_acc_list[epoch] = valid_acc

        if valid_loss < best_loss:
            torch.save(model.state_dict(),output_path+f"res_{name}")
            out_path = output_path+f"res_{name}"
            print('save weight: ', output_path+f"res_{name}")
    return out_path
        # if epoch % period  ==0:
        #     torch.save(model.state_dict(), f"F:/yolov5-master/model_cls/_saved/weight_{prefix}/model-{epoch}.pth")

    # torch.save(model.state_dict(), f"F:/yolov5-master/model_cls/_saved/weight_{prefix}/last.pt")

    # ep = np.array(list(train_loss_list.keys()))
    # trainloss = np.array(list(train_loss_list.values()))
    # trainacc = np.array(list(train_acc_list.values()))
    # validloss = np.array(list(valid_loss_list.values()))
    # validacc = np.array(list(valid_acc_list.values()))


    # pd.DataFrame({'epoch':ep,
    #               'train_loss':trainloss,
    #               'train_acc':trainacc,
    #               'valid_loss':validloss,
    #               'valid_acc':validacc}).to_csv(f'F:/yolov5-master/model_cls/_saved/lossandacc_{prefix}/{prefix}_result.csv', index=None, sep='\t')
    # plot.plot_res_curve(f'F:/yolov5-master/model_cls/_saved//lossandacc_{prefix}/{prefix}_result.csv' , f'F:/yolov5-master/model_cls/_saved//lossandacc_{prefix}/')
if __name__ == '__main__':
    main()






