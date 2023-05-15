# import torch
# import torchvision

# # MNIST dataset
# train_dataset = torchvision.datasets.MNIST(root='../datasets/',
#                                            train=True, 
#                                            transform=torchvision.transforms.ToTensor(),
#                                            download=True)

# test_dataset = torchvision.datasets.MNIST(root='../datasets/',
#                                           train=False, 
#                                           transform=torchvision.transforms.ToTensor())

# # Data loader
# train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
#                                            batch_size=100, 
#                                            shuffle=True)

# test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
#                                           batch_size=100, 
#                                           shuffle=False)
        

# create a MNIST dataset that are 1D, has img, img_label, cond_img, cond_label, object_label 

from torch.utils.data import Dataset, DataLoader
import torch
import torchvision
import random

class MNIST_Conditional(Dataset):
    
    def __init__(self, data_path='../datasets/', oneD = True):
        """
        A dataloader use to load MNIST training set either in 1D or 2D
        return a dictionary with the keys: org_img, org_label, target_img, target_label, cond_label
        
        """
        train_dataset = torchvision.datasets.MNIST(root=data_path,
                                           train=True, 
                                           transform=torchvision.transforms.ToTensor(),
                                           download=True)
        
        self.data = train_dataset.data
        self.targets = train_dataset.targets
        
        index_list = [i for i in range(len(self.data))]
        # get orginal data
        self.org_data = self.data[index_list]
        self.org_labels = self.targets[index_list]
        
        # get target data 
        random.shuffle(index_list)
        self.tagt_data = self.data[index_list]
        self.tagt_labels = self.targets[index_list]
    
        img_size = len(self.data[0]) # 28 
        
        if oneD:
            self.org_data = self.org_data.view(-1, 1, img_size * img_size)
            self.tagt_data = self.tagt_data.view(-1, 1, img_size * img_size)
        
    def __len__(self):
        return len(self.targets)
        
        
    def __getitem__(self, index):
        # random sample two image in the train_dataset
        ret = {}
        org_img = self.org_data[index]
        org_label = self.org_labels[index]
        target_img = self.tagt_data[index]
        target_label = self.tagt_labels[index]
        
        ret['org_img'] = org_img
        ret['org_label'] = org_label
        ret['target_img'] = target_img
        ret['target_label'] = target_label
        ret['cond_label'] = f'from_{org_label}_to_{target_label}'
        
        
        return ret
    

class MNIST_unconditional(Dataset):
    def __init__(self, data_path='../datasets/', oneD = True):
        """
        A dataloader use to load MNIST training set either in 1D or 2D
        return a dictionary with the keys: org_img, org_label, target_img, target_label, cond_label
        
        """
        train_dataset = torchvision.datasets.MNIST(root=data_path,
                                           train=True, 
                                           transform=torchvision.transforms.ToTensor(),
                                           download=True)
        
        self.data = train_dataset.data
        self.targets = train_dataset.targets
        
        img_size = len(self.data[0]) # 28 
        
        if oneD:
            self.data = self.data.view(-1, 1, img_size * img_size)
            
        
    
    def __len__(self):
        return len(self.targets)
        
    def __getitem__(self, index):
        
        return self.data[index], self.targets[index]