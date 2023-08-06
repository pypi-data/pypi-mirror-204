from flask_restful import Resource
from flask import request
from FastCNN.prx.ValidProxy2 import insValider
from FastCNN.prx.PathProxy import PathProxy

class FastCNNApi(Resource):
    
    
    def getStatus():
        rtn = {'success':False}
        
        
        rtn['success'] = True
        return rtn
    
    def getProjectNames():
        rtn = {'success':False}
        
        data = PathProxy.getProjectNames()
        rtn['data'] = data
        
        rtn['success'] = True
        return rtn
    
    def getProjectTags():
        rtn = {'success':False}
        
        data = PathProxy.getProjectTags("GongDa")
        rtn['data'] = data
        rtn['success'] = True
        
        return rtn
    
    def setModel():
        rtn = {'success':False}
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "modelid is nesserary"
            return rtn
        
        ckpt = request.form.get("ckpt")
        if not ckpt:
            rtn["error"] = "ckpt type is nesserary"
            return rtn
        try:
            data = insValider.setModel(projectid,modeltag,ckpt)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def setModels():
        rtn = {'success':False}
        divmodels = request.form.get("divmodels")
        if not divmodels:
            rtn["error"] = "divmodels is nesserary"
            return rtn
        
        objmodels = request.form.get("objmodels")
        if not objmodels:
            rtn["error"] = "objmodels is nesserary"
            return rtn
        
        try:
            data = insValider.setModels(divmodels)
        except Exception as err:
            rtn['data'] = "set div model error : "+str(err)
            return rtn
        
        try:
            data = insValider.setYoloModels(objmodels)
        except Exception as err:
            rtn['data'] = "set obj model error : "+str(err)
            return rtn
        
        rtn['success'] = True
        return rtn
    
    def predictENet():
        rtn = {'success':False}
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "modelid is nesserary"
            return rtn
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        try:
            data = insValider.predictENet(projectid,modeltag,imagepath)
            rtn["data"] = data
        except Exception as err:
            rtn['error'] = str(err)
            return rtn
        
        rtn['success'] = True
        return rtn
        
        
    def predictYNet():
        rtn = {'success':False}
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "modelid is nesserary"
            return rtn
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        try:
            data = insValider.predictYNet(projectid,modeltag,imagepath)
            rtn["data"] = data
        except Exception as err:
            rtn['error'] = str(err)
            return rtn
        
        rtn['success'] = True
        return rtn
    
    def predictSingle():
        rtn = {'success':False}
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        try:
            data = insValider.predictSingle(imagepath)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    
    def setYoloModel():
        rtn = {'success':False}
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "modelid is nesserary"
            return rtn
        
        try:
            data = insValider.setYoloModel(projectid,modeltag)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def predictYolo():
        rtn = {'success':False}
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        try:
            data = insValider.predictYolo(imagepath)
        except Exception as err:
            rtn['data'] = str(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def predictPicture():
        rtn = {'success':False}
        
        projectid = request.form.get("projectid")
        if not projectid:
            rtn["error"] = "projectid is nesserary"
            return rtn
        
        imagepath = request.form.get("imagepath")
        if not imagepath:
            rtn["error"] = "imagepath is nesserary"
            return rtn
        
        modeltag = request.form.get("modeltag")
        if not modeltag:
            rtn["error"] = "modeltag is nesserary"
            return rtn
        
        ckpt = request.form.get("ckpt")
        if not ckpt:
            rtn["error"] = "ckpt type is nesserary"
            return rtn
        
        try:
            data = insValider.predictPicture(imagepath,projectid,modeltag,ckpt)
        except Exception as err:
            rtn['data'] = str(err)
            print(err)
            return rtn
        rtn['data'] = data
        rtn['success'] = True
        return rtn
    
    def post(self):
        _cmd = request.form.get('cmd')
        
        if _cmd == "getProjectNames":
            return FastCNNApi.getProjectNames()
        
        if _cmd == "getProjectTags":
            return FastCNNApi.getProjectTags()
        
        if _cmd == "predictPicture":
            return FastCNNApi.predictPicture()
        
        if _cmd == "setModel":
            return FastCNNApi.setModel()
        
        if _cmd == "predictSingle":
            return FastCNNApi.predictSingle()
            
        if _cmd == "setYoloModel":
            return FastCNNApi.setYoloModel()
        
        if _cmd == "predictYolo":
            return FastCNNApi.predictYolo()
        
        if _cmd == "setModels":
            return FastCNNApi.setModels()
        
        if _cmd == "predictENet":
            return FastCNNApi.predictENet()
        
        if _cmd == "predictYNet":
            return FastCNNApi.predictYNet()
