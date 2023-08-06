#! /usr/bin/env python
"""
-*- coding: UTF-8 -*-
Project   : har2case
Author    : Captain
Email     : qing.ji@extremevision.com.cn
Date      : 2023/4/19 14:15
FileName  : main.py
Software  : PyCharm
Desc      : 项目主入口
"""
import sys
import argparse
import time

from loguru import logger
from har_to_case.parse_har import ParseHar
from har_to_case import __description__

try:
    from har_to_case import __version__ as version
except ImportError:
    version = None

if len(sys.argv) == 1:
    sys.argv.append('--help')
now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
parser = argparse.ArgumentParser(description=__description__)
parser.add_argument('-v', '--version', help=f"显示版本;当前版本：{version}", action="store_true")
parser.add_argument('-i', '--input', type=str, help='har文件路径（必填）')
parser.add_argument('-o', '--output', default=f"record_{now}.yaml", type=str, help='指定输出文件名')


def main():
    args = parser.parse_args()
    if args.version:
        logger.info(f"当前版本：{version}")
        exit(0)
    arguments = parser.parse_args()
    if not arguments.input:
        logger.error("har文件路径为必填项：-i {har file path}")
    ParseHar(arguments.input, arguments.output).generate_yaml_case()


if __name__ == '__main__':
    main()
