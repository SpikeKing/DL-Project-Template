# -- coding: utf-8 --
"""
Copyright (c) 2018. All rights reserved.
Created by C. L. Wang on 2018/4/18
"""
import argparse
import json

import os
from bunch import Bunch

from utils import mkdir_if_not_exist


def get_config_from_json(json_file):
    """
    将配置文件转换为配置类
    """
    with open(json_file, 'r') as config_file:
        config_dict = json.load(config_file)  # 配置字典

    config = Bunch(config_dict)  # 将配置字典转换为类

    return config, config_dict


def process_config(json_file):
    """
    解析Json文件
    :param json_file: 配置文件
    :return: 配置类
    """
    config, _ = get_config_from_json(json_file)
    config.tb_dir = os.path.join("experiments", config.exp_name, "logs/")  # 日志
    config.cp_dir = os.path.join("experiments", config.exp_name, "checkpoints/")  # 模型
    config.img_dir = os.path.join("experiments", config.exp_name, "images/")  # 网络

    mkdir_if_not_exist(config.tb_dir)  # 创建文件夹
    mkdir_if_not_exist(config.cp_dir)  # 创建文件夹
    mkdir_if_not_exist(config.img_dir)  # 创建文件夹
    return config


def get_train_args():
    """
    添加训练参数
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-c', '--cfg',
        dest='config',
        metavar='path',
        default='None',
        help='add a configuration file')
    args = parser.parse_args()
    return args, parser


def get_test_args():
    """
    添加测试路径
    :return: 参数
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-c', '--cfg',
        dest='config',
        metavar='C',
        default='None',
        help='add a configuration file')
    parser.add_argument(
        '-m', '--mod',
        dest='model',
        metavar='',
        default='None',
        help='add a model file')
    args = parser.parse_args()
    return args, parser
