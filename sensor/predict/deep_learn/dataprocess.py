import numpy as np
import pandas as pd
from collections import Counter
import torch
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
# path="./flow.csv"
class KddData(object):

    def __init__(self,path):
        self.data = pd.read_csv(path,header=0)
        # _,length=data.shape
        # # # print(length)
        # data = data.iloc[:, 0:length]
        self.deal_data=self.data.drop(['src_ip', 'dst_ip','src_port',"protocol","timestamp"],axis=1)
       # data= data.drop(['src_ip', 'dst_ip','src_port',"protocol","timestamp"],axis=1)
       # data.dropna()
#        data = np.array(data)
        self.deal_data = np.array(self.deal_data)
        # print(data)

        self.test_data = self.__encode_data(self.deal_data)
        self.test_dataset =self.data_to_tensoer(self.test_data)
        self.data_deal_set=self.data_to_dict(self.data)

    def get_data(self):
        pass


    # """将数据中字符串部分转换为数字，并将输入的78维特征转换为9*9的矩阵"""
    def __encode_data(self, data_X):
        data_X = np.pad(data_X, ((0, 0), (0, 81 - len(data_X[0]))), 'constant').reshape(-1, 1, 9, 9)
        return data_X

    def data_to_tensoer(self,data_X):
        tensoer = TensorDataset(
            torch.from_numpy(data_X.astype(np.float32)),
        )
        return tensoer

    def data_to_dict(self,data_X):
        data_rel=data_X.itertuples()
        return data_rel

# kdd=KddData()
