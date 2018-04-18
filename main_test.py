#!/usr/bin/env python
# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18
"""
import numpy as np

from data_loaders.simple_mnist_dl import SimpleMnistDL
from infers.simple_mnist_infer import SimpleMnistInfer
from utils.config_utils import process_config, get_test_args


def main_test():
    print '[INFO] 解析配置...'
    parser = None
    config = None
    model_path = None

    try:
        args, parser = get_test_args()
        config = process_config(args.config)
        model_path = args.model
    except Exception as e:
        print '[Exception] 配置无效, %s' % e
        if parser:
            parser.print_help()
        print '[Exception] 参考: python main_test.py -c configs/simple_mnist_config.json ' \
              '-m simple_mnist.weights.10-0.24.hdf5'
        exit(0)
    # config = process_config('configs/simple_mnist_config.json')

    print '[INFO] 加载数据...'
    dl = SimpleMnistDL()
    test_data = np.expand_dims(dl.get_test_data()[0][0], axis=0)
    test_label = np.argmax(dl.get_test_data()[1][0])

    print '[INFO] 预测数据...'
    # infer = SimpleMnistInfer("simple_mnist.weights.16-0.19.hdf5", config)
    infer = SimpleMnistInfer(model_path, config)
    infer_label = np.argmax(infer.predict(test_data))
    print '[INFO] 真实Label: %s, 预测Label: %s' % (test_label, infer_label)

    print '[INFO] 预测完成...'


if __name__ == '__main__':
    main_test()
