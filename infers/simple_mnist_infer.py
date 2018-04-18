# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18
"""
import os

from bases.infer_base import InferBase
from keras.models import load_model


class SimpleMnistInfer(InferBase):
    def __init__(self, name, config=None):
        super(SimpleMnistInfer, self).__init__(config)
        self.model = self.load_model(name)

    def load_model(self, name):
        model = os.path.join(self.config.cp_dir, name)
        return load_model(model)

    def predict(self, data):
        return self.model.predict(data)
