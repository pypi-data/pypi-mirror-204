#!/usr/bin/env python
# coding: utf-8

# Copyright (c) nicolas allezard.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""


from ipywidgets import DOMWidget, ValueWidget, register,CallbackDispatcher
from traitlets import Unicode, Bool, validate, TraitError,Int,List,Dict,Bytes,Any,Instance
from ipywidgets.widgets.trait_types import (
    bytes_serialization,
    _color_names,
    _color_hex_re,
    _color_hexa_re,
    _color_rgbhsl_re,
)
from ._frontend import module_name, module_version


import numpy as np
import base64
import cv2
import copy
import json

from pathlib import Path
from urllib.request import urlopen
from PIL import Image
import io
import time

def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
    return img

def writeb64(img):
    """Encode matrix to base64 image string"""
    retval, buffer = cv2.imencode('.png', img)
    pic_bytes = base64.b64encode(buffer)
    pic_str = pic_bytes.decode()
    return pic_str


#@register
class Pixano(DOMWidget):#, ValueWidget):
    _model_name = Unicode('PixanoModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)

    _view_name = Unicode('PixanoView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    element=Unicode('').tag(sync=True)
    plugin_name=Unicode('').tag(sync=True)

    image= Any().tag(sync=True) 
    image_screenshot   = Unicode('').tag(sync=True) 

    mode=Unicode('none').tag(sync=True)
    key_event=Dict([]).tag(sync=True)
    img_count=Int(0).tag(sync=True)

    # shapes_in=List([]).tag(sync=True)
    # shapes=List([]).tag(sync=True)
    # selectedShapeIds=List([]).tag(sync=True)
    
    annotations_input=List([0]).tag(sync=True)
    annotations=List([]).tag(sync=True)
    selectedIds=List([]).tag(sync=True)
    selectedIds_input=List([]).tag(sync=True)
    
    do_screenshot=Int(0).tag(sync=True)
    modified=Int(0).tag(sync=True)
    screenshot= Unicode('').tag(sync=True) 

    current_category=Unicode('').tag(sync=True)
    categories_colors=Dict().tag(sync=True)

    
    # mask=Unicode('').tag(sync=True)
    # targetClass=Int(1).tag(sync=True)
    # clsMap=Dict().tag(sync=True)
    maskVisuMode=Unicode('INSTANCE').tag(sync=True)

    label_schema=Dict({}).tag(sync=True)
    graph_setting=Dict({}).tag(sync=True)
    annot_count=0
    toggle_labels=Int(0).tag(sync=True) 
    
    prediction=List([]).tag(sync=True)
    selectedCategory=Unicode('').tag(sync=True)

    client_ready=Bool(False).tag(sync=True)

    def __init__(self, *args, **kwargs):
        super(Pixano, self).__init__(*args, **kwargs)
        #print('Init Pixano')
        self.on_msg(self._handle_frontend_event)

        if "annotations" in kwargs:
            #print("init with annotations")
            new_annotations=kwargs['annotations']
            annot_count=self.annotations_input[0]
            annot_count+=1
            if "segmentation" in self.element :
                #print("segmentation mode")
                if not 'mask' in new_annotations[0]: return
                

            new_annotations=[annot_count,copy.deepcopy(new_annotations)]
            self.annotations_input=new_annotations

   

    def _handle_frontend_event(self, _, content, buffers):
        #print("content",content)

        if content.get("predict", ""):

            self.predict(content,buffers)
        
      
    def predict(self,content,buffers):
        try:
            x0,y0,x1,y1=content['predict']['roi']
            w,h=content['predict']['size']
            img=np.array(buffers[0].tolist(),dtype=np.uint8)
            img=np.reshape(img,(h,w,4))        
            #img=readb64(buffers[0])
            
            prediction = self.predict_function(img[:,:,0:3],[x0,y0,x1,y1])
            if prediction.ndim!=1 :
                prediction=prediction.flatten()
            self.prediction=[prediction]
        except:
            x0,y0,x1,y1=content['predict']['roi']
            print("No predict function or Error in code --> return zeros prediction mask",x0,y0,x1,y1)
            mask=np.zeros((y1-y0,x1-x0),dtype=float)
            
            self.prediction=[{'roi':[x0,y0,x1,y1],'result':mask.flatten()}]

    @validate('element')
    def _valid_element(self, proposal):
        element=str(proposal['value'])
        if not element.startswith("pxn-"):
            element='pxn-'+element
        valid_elem=["pxn-rectangle","pxn-segmentation","pxn-smart-rectangle","pxn-smart-segmentation","pxn-smart-segmentation-python","pxn-polygon",'pxn-graph','pxn-keypoints']
        #print("element",proposal["value"])
        if not element in valid_elem:
            raise TraitError('Invalid element: must be one of '+",".join(valid_elem))
        return element


    # @validate('plugin_name')
    # def _valid_plugin(self, proposal):
    #     self.element='pxn-'+proposal['value']

    @validate('label_schema')
    def _valid_schema(self,proposal):
        return proposal["value"]
    

    @validate('image')
    def _valid_image(self, proposal):
        #print(type(proposal['value']))
        if isinstance(proposal['value'], str):
            #print("string")
            filename=proposal['value']
            if 'http' in filename:
                data=urlopen(filename).read()
                data = base64.b64encode(data).decode()
            elif filename!='':
                abs_filename=Path(filename).absolute().as_posix()
                image_format=abs_filename.split(".")[-1]
                data=open(abs_filename,"rb").read()
                # abs_filename=Path(filename).absolute().as_posix()
                # #print(abs_filename)

                # data=urlopen("file://"+abs_filename).read()
                data = base64.b64encode(data).decode()
                #print(data[:100])
            else:
                return None

            return data
        elif isinstance(proposal['value'],np.ndarray) :
            #print("array")
            imPIL=Image.fromarray(proposal['value'])
            img_byte_arr = io.BytesIO()
            imPIL.save(img_byte_arr, format='PNG')
            data=base64.b64encode(img_byte_arr.getvalue()).decode()
            return data
            
        elif isinstance(proposal['value'],Image.Image):
            #print("pil image")
            img_byte_arr = io.BytesIO()
            proposal['value'].save(img_byte_arr, format='PNG')
            data=base64.b64encode(img_byte_arr.getvalue()).decode()
            #print(data[:100])
            return data
        else:
            raise TraitError('Invalid type: get '+str(type(proposal['value']))+", must be a string, a numpy ndarray or a PIL image " )
        return None


    def getMask(self):

        if self.annotations is None or len(self.annotations)==0 : return None

        annotation=self.annotations[0]

        if 'mask' in annotation and annotation['mask']!= None:
            img=readb64(annotation['mask'])
            return img
        else:
            return None

    def takeScreenShot(self):
        self.do_screenshot+=1
    def getScreenShot(self):
        return readb64(self.image_screenshot)


    def setMask(self,mask,infos=None):
        annotations_dict=[{'id': 0,'mask':"data:image/png;base64,"+writeb64(mask)}]#,*infos ]
        annot_count=self.annotations_input[0]
        annot_count+=1
        new_annotations=[annot_count,copy.deepcopy(annotations_dict)]
        self.annotations_input=new_annotations

    def getSegmentationInfos(self):
        if "segmentation" in self.element and len(self.annotations)>0:
            return self.annotations[1:]
        else :
            return None

    def save(self,filename):
        with open(filename,"w") as f:
            json.dump(self.annotations,f,indent=True)

    def load(self,filename):
        with open(filename,"r") as f:
            annotations=json.load(f)
            if annotations is not None : self.setAnnotations(annotations)

    def clearAnnotations(self):
        #print("python in",self.shapes_in)
        self.annotations_input=copy.deepcopy(['-'])
    
    def toggleLabels(self,dummy=False):
        self.toggle_labels=self.toggle_labels+1

    def setAnnotations(self,new_annotations=[]):
        # time.sleep(1)
        
        annot_count=self.annotations_input[0]
        annot_count+=1
        if "segmentation" in self.element:
            print("isinstance(new_annotations,dict)",isinstance(new_annotations,dict))
            if isinstance(new_annotations,dict):
                new_annotations=[new_annotations]
            elif isinstance(new_annotations,list):
                 new_annotations=new_annotations[:1]

        new_annotations=[annot_count,copy.deepcopy(new_annotations)]
        self.annotations_input=new_annotations


    def setImageData(self,image=None,format=None,annotations=None):
        image_data,image_format=self.convertImage(image)
        opt_image={"format":image_format if not format else format}
        #print("format",image_format)

        if image_format=="url": 
            image_data=bytes(image_data,'utf-8')
        

        message={}
        data=None
        if image is not None:
            message['set_image']=opt_image
            data={image_data}
        if annotations is not None:
            #print("set annotations","mask" in annotations)
            if "mask" in annotations:
                mask=annotations['mask']
                mask_value=mask
                if str(type(mask))== "<class 'numpy.ndarray'>":
                    mask_value="data:image/png;base64,"+writeb64(annotations['mask'])
               
                annotations=[{'id': 0,'mask':mask_value}]
            message['set_annotations']=annotations
            
        #print("message")
        self.send(message,data)
       

    def convertImage(self,image):
        image_data,image_format=None,None
        if isinstance(image, str):
            filename=image
            if 'http' in filename:
                image_data=filename
                image_format='url'
            else:
                abs_filename=Path(filename).absolute().as_posix()
                image_format=abs_filename.split(".")[-1]
                image_data=open(abs_filename,"rb").read()
                #image_data = base64.b64encode(image_data).decode()
        elif str(type(image))== "<class 'numpy.ndarray'>" :
            image_data= writeb64(image)
            image_format='png'
            
        elif isinstance(image,Image.Image):

            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            image_format='png'
            image_data=img_byte_arr.getvalue()

        return image_data,image_format