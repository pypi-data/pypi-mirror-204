import os
import torch
import torch.nn as nn

import torchvision
from torchvision import models

class Model_Process():
    def __init__(self, args) -> None:
        '''init parse'''
        self.args = args
        pass
    
    @staticmethod
    def check_dir(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok= True)

    @staticmethod
    def get_state_dict(ckpt = None, url = None, model_dir = './checpoints'):
        '''raise 函数有待完善'''
        try:
            if ckpt != None:
                state_dict = torch.load(ckpt, map_location='cpu')
            
            elif url != None:
                try:
                    if model_dir != './checpoints':
                        state_dict = torch.hub.load_state_dict_from_url(url, model_dir= model_dir, map_location='cpu', check_hash= True)
                    else:
                        state_dict = torch.hub.load_state_dict_from_url(url, map_location='cpu', check_hash= True)
                except Exception as err:
                    state_dict = os.system(f'wget -P {model_dir} -c {url}')
        except Exception as err:
            print('please give a correct ckpt path or url')



        return state_dict
    
    @staticmethod
    def load_model1(model, state_dict):
        model_state = model.state_dict()
        parse_dict = {
            k:v for k, v in state_dict.items() if k in model_state.keys()
        }
        # model.state_dict().update(parse_dict)  #model.state_dict().update(parse_dict)并不能更新模型的参数
        model.load_state_dict(parse_dict)   #更新参数必须用load_state_dict
        

    @staticmethod
    def load_model2(model, state_dict):
        model_state = model.state_dict()     #model.state_dict() 返回的是每一层的名字以及对应的参数
        # for name in model.state_dict():      #但这个时候返回的name只是键
        #     model.state_dict()
        #     print(name)
        keys = model.state_dict().keys()   #这个时候返回的key也是键
        for key in keys:
            print(key)

        for k, v in state_dict.items():
            a = model.k
            model.state_dict().update(parse_dict)

if __name__ == '__main__':
    net = models.resnet50(pretrained= False)
    url = 'https://download.pytorch.org/models/resnet50-0676ba61.pth'
    state_dict = Model_Process.get_state_dict(url=url, model_dir = './xjm_checkpoints')
    Model_Process.load_model2(net, state_dict)

    print(0)

    print(1)