#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18

参考:
NumPy FutureWarning
https://stackoverflow.com/questions/48340392/futurewarning-conversion-of-the-second-argument-of-issubdtype-from-float-to
"""

from data_loaders.simple_mnist_dl import SimpleMnistDL
from infers.simple_mnist_infer import SimpleMnistInfer
from models.simple_mnist_model import SimpleMnistModel
from trainers.simple_mnist_trainer import SimpleMnistTrainer
from utils.config_utils import process_config, get_train_args
import numpy as np


def main_train():
    """
    训练模型

    :return:
    """
    print('[INFO] 解析配置...')

    parser = None
    config = None

    try:
        args, parser = get_train_args()
        config = process_config(args.config)
    except Exception as e:
        print('[Exception] 配置无效, %s' % e)
        if parser:
            parser.print_help()
        print('[Exception] 参考: python main_train.py -c configs/simple_mnist_config.json')
        exit(0)
    # config = process_config('configs/simple_mnist_config.json')

    print('[INFO] 加载数据...')
    dl = SimpleMnistDL(config=config)

    print('[INFO] 构造网络...')
    model = SimpleMnistModel(config=config)

    print('[INFO] 训练网络...')
    trainer = SimpleMnistTrainer(
        model=model.model,
        data=[dl.get_train_data(), dl.get_test_data()],
        config=config)
    trainer.train()
    print('[INFO] 训练完成...')


def test_main():
    print('[INFO] 解析配置...')
    config = process_config('configs/simple_mnist_config.json')

    print('[INFO] 加载数据...')
    dl = SimpleMnistDL()
    test_data = np.expand_dims(dl.get_test_data()[0][0], axis=0)
    test_label = np.argmax(dl.get_test_data()[1][0])

    print('[INFO] 预测数据...')
    infer = SimpleMnistInfer("simple_mnist.weights.16-0.19.hdf5", config)
    infer_label = np.argmax(infer.predict(test_data))
    print('[INFO] 真实Label: %s, 预测Label: %s' % (test_label, infer_label))

    print('[INFO] 预测完成...')


if __name__ == '__main__':
    main_train()
    # test_main()
