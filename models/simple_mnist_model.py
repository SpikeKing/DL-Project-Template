# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18
"""
import os
from keras import Input, Model
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import plot_model

from bases.model_base import ModelBase


class SimpleMnistModel(ModelBase):
    """
    SimpleMnist模型
    """

    def __init__(self, config):
        super(SimpleMnistModel, self).__init__(config)
        self.build_model()

    def build_model(self):
        main_input = Input(shape=(28 * 28,), name='main_input')
        x = Dense(units=32, activation='relu', kernel_initializer='random_uniform')(main_input)
        x = Dense(units=16, activation='relu')(x)
        output = Dense(units=10, activation='softmax')(x)
        model = Model([main_input], output)
        model.compile(loss='categorical_crossentropy',
                      optimizer=Adam(lr=self.config.lr),
                      metrics=['accuracy'])

        plot_model(model, to_file=os.path.join(self.config.img_dir, "model.png"), show_shapes=True)  # 绘制模型图

        self.model = model
