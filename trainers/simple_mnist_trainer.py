# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18
"""
import os
import warnings

from keras.callbacks import TensorBoard, ModelCheckpoint, Callback
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.metrics import precision_recall_fscore_support

from bases.trainer_base import TrainerBase
import numpy as np

from utils.np_utils import prp_2_oh_array


class SimpleMnistTrainer(TrainerBase):
    def __init__(self, model, data, config):
        super(SimpleMnistTrainer, self).__init__(model, data, config)
        self.callbacks = []
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []
        self.init_callbacks()

    def init_callbacks(self):
        self.callbacks.append(
            ModelCheckpoint(
                filepath=os.path.join(self.config.cp_dir,
                                      '%s.weights.{epoch:02d}-{val_loss:.2f}.hdf5' % self.config.exp_name),
                monitor="val_loss",
                mode='min',
                save_best_only=True,
                save_weights_only=False,
            )
        )

        self.callbacks.append(
            TensorBoard(
                log_dir=self.config.tb_dir,
                write_images=True,
                write_graph=True,
            )
        )

        # self.callbacks.append(FPRMetric())
        self.callbacks.append(FPRMetricDetail())

    def train(self):
        history = self.model.fit(
            self.data[0][0], self.data[0][1],
            epochs=self.config.num_epochs,
            verbose=2,
            batch_size=self.config.batch_size,
            validation_data=(self.data[1][0], self.data[1][1]),
            # validation_split=0.25,
            callbacks=self.callbacks,
        )
        self.loss.extend(history.history['loss'])
        self.acc.extend(history.history['acc'])
        self.val_loss.extend(history.history['val_loss'])
        self.val_acc.extend(history.history['val_acc'])


class FPRMetric(Callback):
    """
    输出F, P, R
    """

    def on_epoch_end(self, batch, logs=None):
        val_x = self.validation_data[0]
        val_y = self.validation_data[1]

        prd_y = prp_2_oh_array(np.asarray(self.model.predict(val_x)))

        warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
        precision, recall, f_score, _ = precision_recall_fscore_support(
            val_y, prd_y, average='macro')
        print(" — val_f1: % 0.4f — val_pre: % 0.4f — val_rec % 0.4f" % (f_score, precision, recall))


class FPRMetricDetail(Callback):
    """
    输出F, P, R
    """

    def on_epoch_end(self, batch, logs=None):
        val_x = self.validation_data[0]
        val_y = self.validation_data[1]

        prd_y = prp_2_oh_array(np.asarray(self.model.predict(val_x)))

        warnings.filterwarnings("ignore", category=UndefinedMetricWarning)
        precision, recall, f_score, support = precision_recall_fscore_support(val_y, prd_y)

        for p, r, f, s in zip(precision, recall, f_score, support):
            print(" — val_f1: % 0.4f — val_pre: % 0.4f — val_rec % 0.4f - ins %s" % (f, p, r, s))
