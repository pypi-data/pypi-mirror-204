#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
Author   : JiQing
Email    : qing.ji@extremevision.com.cn
Date     : 2022/10/24 10:07
Desc     :
FileName : tools.py
Software : PyCharm
"""

import io
import json
import os

import yaml
from loguru import logger


def get_file_path(url, entry_json):
    '''
    获取用例文件地址
    :param url:
    :param entry_json:
    :return:
    '''
    file_name = 'test_' + ''.join(url.split("/")[-1])
    api = is_file_exist(os.path.join(os.getcwd(), "api"))
    module = is_file_exist(
        os.path.join(
            api, {"module": v.get("tags")[0] for k, v in entry_json.items()}.get("module")))
    return os.path.join(module, file_name)


def is_file_exist(files):
    '''
    检查文件是否存在
    :param files:
    :return:
    '''
    if not os.path.exists(files):
        os.mkdir(files)
    return files


def dump_yaml(case, yaml_file):
    '''
    创建YAML格式文件
    :param case:
    :param yaml_file:
    :return:
    '''
    if os.path.exists(yaml_file):
        logger.debug("文件存在，跳过解析")
        return

    logger.info("开始创建YAML格式文件")
    with io.open(yaml_file, 'w', encoding="utf-8") as outfile:
        yaml.dump(case, outfile, allow_unicode=True, default_flow_style=False, indent=4)

        logger.info(f"yaml文件:{yaml_file}创建成功")


def dump_json(case, json_file):
    '''
    创建YAML格式文件
    :param case:
    :param json_file:
    :return:
    '''
    logger.info("开始创建json格式文件")
    if not os.path.exists(json_file):
        os.makedirs(json_file)

    with io.open(json_file, 'w', encoding="utf-8") as outfile:
        my_json_str = json.dumps(case, ensure_ascii=False, indent=4)
        if isinstance(my_json_str, bytes):
            my_json_str = my_json_str.decode("utf-8")
        outfile.write(my_json_str)
    logger.info(f"json文件: {json_file}创建成功")


def get_target_value(key, _json, tmp_list=None):
    '''
    从字典中获取目标值
    :param key:
    :param _json:
    :param tmp_list:
    :return:
    '''
    if tmp_list is None:
        tmp_list = []

    if not isinstance(_json, dict) or not isinstance(tmp_list, list):
        return 'args[1]不是字典或args[-1]不是列表'

    if key in _json.keys():
        tmp_list.append(_json[key])

    for value in _json.values():
        if isinstance(value, dict):
            get_target_value(key, value, tmp_list)
        elif isinstance(value, (list, tuple)):
            _get_list_value(key, value, tmp_list)

    return tmp_list


def _get_list_value(key, value, tmp_list):
    '''
    循环访问列表获取目标值
    :param key:
    :param value:
    :param tmp_list:
    :return:
    '''
    for val_ in value:
        if isinstance(val_, dict):
            get_target_value(key, val_, tmp_list)
        elif isinstance(val_, (list, tuple)):
            _get_list_value(key, val_, tmp_list)
