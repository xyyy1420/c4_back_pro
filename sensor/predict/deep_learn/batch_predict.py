import os
from .dataprocess import KddData
import torch
from PIL import Image
from torch.utils.data import DataLoader
from .vit_model import vit_base_patch16_224_in21k as create_model
import sys
import json
import logging

from data_sender.data_send import data_send
# from msg_send.post_send import DataSend


class DataAnalysis(object):

    def __init__(self, path):

        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu")

        self.dataset = KddData(path)

        self.test_loder = torch.utils.data.DataLoader(
            self.dataset.test_dataset)

        self.model = create_model(
            num_classes=2, has_logits=False).to(self.device)

        weights_path = "sensor/predict/deep_learn/VIT_weights3.pth"

        assert os.path.exists(
            weights_path), f"file: '{weights_path}' dose not exist."

        self.model.load_state_dict(torch.load(
            weights_path, map_location=self.device))

        # self.sender = DataSend()

        # prediction
        self.model.eval()
        # batch_size = 8  # 每次预测时将多少张图片打包成一个batch

    def run_module(self):

        with torch.no_grad():
            #        for i,data in enumerate(test_loder):
            for data_set_v, data in zip(self.dataset.data_deal_set, self.test_loder):
                # predict class
                data = torch.stack(data, dim=1)
                data = torch.squeeze(data, 1)
    #            print(data.shape)
                output = self.model(data.to(self.device))
                # predict = torch.softmax(output, dim=1)
                probs, classes = torch.max(output, dim=1)

                info_dict = {"src_ip": data_set_v[1], "dst_ip": data_set_v[2], "src_port": data_set_v[3],
                             "dst_port": data_set_v[4], "timestamp": data_set_v[6], "attack": classes[0].item()}

                # print(classes)
                logging.warn(info_dict)
                # self.sender.send_data(info_dict)  # TODO:完成msg调试填入

                # print(data_set_v[1],probs,classes)


# def main(path):
#    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#    print(device)
#    dataset=KddData(path)
#
#    test_loder=torch.utils.data.DataLoader(dataset.test_dataset)
#    # print(test_loder.shape)
#
#    # create model
#    model = create_model(num_classes=2,has_logits=False).to(device)
#
#    # load model weights
#    weights_path = "./VIT_weights3.pth"
#    assert os.path.exists(weights_path), f"file: '{weights_path}' dose not exist."
#    model.load_state_dict(torch.load(weights_path, map_location=device))
#
#    # prediction
#    model.eval()
#    # batch_size = 8  # 每次预测时将多少张图片打包成一个batch
#    with torch.no_grad():
# for i,data in enumerate(test_loder):
#        for data_set_v,data in zip(dataset.data_deal_set,test_loder):
#            # predict class
#
#            data = torch.stack(data, dim=1)
#            data=torch.squeeze(data,1)
# print(data.shape)
#            output = model(data.to(device))
#            # predict = torch.softmax(output, dim=1)
#            probs, classes = torch.max(output, dim=1)
#
#            print(data_set_v[1],probs,classes)
#
#
#
# DONE：在这里删除下面的测试部分 ，已注释
# if __name__ == '__main__':
#     path=sys.argv[1]
#     data=DataAnalysis(path)
#     data.run_module()
# #    main(path)
