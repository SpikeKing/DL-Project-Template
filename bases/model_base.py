# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18
"""


class ModelBase(object):
    """
    模型基类
    """

    def __init__(self, config):
        self.config = config  # 配置
        self.model = None  # 模型

    def save(self, checkpoint_path):
        """
        存储checkpoint, 路径定义于配置文件中
        """
        if self.model is None:
            raise Exception("[Exception] You have to build the model first.")

        print("[INFO] Saving model...")
        self.model.save_weights(checkpoint_path)
        print("[INFO] Model saved")

    def load(self, checkpoint_path):
        """
        加载checkpoint, 路径定义于配置文件中
        """
        if self.model is None:
            raise Exception("[Exception] You have to build the model first.")

        print("[INFO] Loading model checkpoint {} ...\n".format(checkpoint_path))
        self.model.load_weights(checkpoint_path)
        print("[INFO] Model loaded")

    def build_model(self):
        """
        构建模型
        """
        raise NotImplementedError
