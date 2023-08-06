import torch
import torch.nn as nn
import torch.optim as optim

from FastCNN.datasets.fastcsv import FastCsvT1

from torch.autograd import Variable
import time
import os
import datetime
import json

from IutyLib.file.files import CsvFile
from IutyLib.commonutil.config import JConfig

from FastCNN.prx.PathProxy import PathProxy3 as PathProxy
from FastCNN.nn.neuralnets import getNeuralNet

from PIL import Image

from FastCNN.prx.YoloV5DetectProxy import _model as ymodel

class DivValidObj:
    _model = None
    _labels = None
    _pre = None
    _projid = ""
    _modelid = ""
    _busy = False
    
    def __init__(self):
        pass
    
    def setModel(self,projectid,modelid,mtype="valid"):
        self._projid = projectid
        self._modelid = modelid
        config = ValidProxy.getConfig(projectid,modelid)
        self._labels = config["LabelList"]
        
        net_name = config["Type"]
        
        net = getNeuralNet(net_name)
        net.initModel(len(self._labels))
        
        self._pre = net.getPreProcess(fliph=True)["valid"]
        
        train_ckpt = PathProxy.getTrainCKPT(projectid,modelid)
        valid_ckpt = PathProxy.getValidCKPT(projectid,modelid)
        
        if mtype == "train":
            self._model = net.loadModel(train_ckpt)
        elif mtype == "valid":
            self._model = net.loadModel(valid_ckpt)
        else:
            raise Exception("unrecorgnised model type,you should try from 'train' or 'valid'")
        
        pass
    
    def predict(self,imgpath):
        self._busy = True
        if self._model == None:
            raise Exception("Model has not initialed")
        s = time.time()
        img=Image.open(imgpath).convert('RGB')
    
        
        img = self._pre(img).unsqueeze(0).cuda()
    
        outputs = self._model(img).cuda()
        
        indices = torch.argmax(outputs,1)
        
        ptype = self._labels[indices.item()]
        
        #percentage = outputs.item()[indices.item()]
        percentage = torch.softmax(outputs, dim=1)[0][indices.item()].item()
        e = time.time()
        result = {
            "name":imgpath,
            "maybetype":ptype,
            "percent":str(round(percentage,3)),
            "spend":str(round(e-s,2))
            }
        self._busy = False
        return result
    
    def isTheModel(self,projectid,modelid):
        return projectid == self._projid and modelid == self._modelid and (not _busy)
    
    
class ValidProxy:
    _div_ = []
    
    def __init__(self):
        pass
    
    def getConfig(projectid,modelid):
        cfgpath = PathProxy.getConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data
    
    def getSuperParam(projectid,modelid):
        cfgpath = PathProxy.getSuperParamConfigPath(projectid,modelid)
        jfile = JConfig(cfgpath)
        data = jfile.get()
        return data
    
    def predict(self,imgpath):
        if len(self._div_) > 0:
            return self._div_[0].predict(imgpath)
        else:
            raise Exception("No model setted")
        
    def predictSingle(self,imgpath):
        """
        predict with the last model
        imgpath: local image path for decode
        """
        return self.predict(imgpath)
    
    def getModelByID(self,projectid,modelid):
        rtn = None
        for m in self._div_:
            if m._projid == projectid and m._modelid == modelid and m._busy == False:
                rtn = m
                rtn._busy = True
                break
        return rtn
    
    
    def setModel(self,projectid,modelid,mtype="valid",clr = True):
        m = DivValidObj()
        m.setModel(projectid,modelid,mtype)
        if(clr):
            self._div_.clear()
        self._div_.append(m)
        pass
    
    def setModels(self,listProjMod):
        self._div_.clear()
        listProjMod = json.loads(listProjMod)
        for projectid,modelid in listProjMod:
            self.setModel(projectid,modelid,"valid",False)
        pass
    
    def setYoloModel(self,projectid,modelid):
        ymodel.loadModel(projectid,modelid)
        pass
    
    def setYoloModels(self,ymodels):
        ymodels = json.loads(ymodels)
        ymodel.loadModels(ymodels)
        pass
    
    def predictYolo(self,imgpath):
        return ymodel.predictSingle(imgpath)
    
    def predictPicture(self,imgpath,projectid,modelid,mtype):
        self.setModel(projectid,modelid,mtype)
        return self.predict(imgpath)
    
    def predictENet(self,projid,modid,imgpath):
        mdl = self.getModelByID(projid,modid)
        return mdl.predict(imgpath)
    
    def predictYNet(self,projid,modid,imgpath):
        return ymodel.predictByID(projid,modid,imgpath)
    
    pass

insValider = ValidProxy()

def test():
    insValider.setModel("New_Project3","20210812_210246","valid")
    for i in range(5):
        print(insValider.predictSingle(r"E:\yaoping1\Valid\OK\Grab3_0_1256445_074239.bmp"))
    
    print(insValider.predictPicture(r"E:\yaoping1\Valid\OK\Grab3_0_1256445_074239.bmp","New_Project3","20210812_210246","valid"))
