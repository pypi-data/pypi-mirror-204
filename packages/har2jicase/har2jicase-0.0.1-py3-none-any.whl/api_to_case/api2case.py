#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
Author   : JiQing
Email    : qing.ji@extremevision.com.cn
Date     : 2022/10/26 9:38
Desc     :
FileName : api2case.py
Software : PyCharm
"""
import sys
import argparse

from loguru import logger
from api_to_case.main import SwaggerParser
from api_to_case import __description__

try:
    from api_to_case import __version__ as version
except ImportError:
    version = None

if len(sys.argv) == 1:
    sys.argv.append('--help')

parser = argparse.ArgumentParser(description=__description__)
parser.add_argument('-v', '--version', help=f"显示版本;当前版本：{version}", action="store_true")
parser.add_argument('-u', '--url', type=str, help='swagger API接口文档地址（必填)')
parser.add_argument('-n', '--username', default=None, type=str, help='swagger用户名')
parser.add_argument('-w', '--password', default=None, type=str, help='swagger密码')
parser.add_argument('-p', '--path', default=None, type=str, help='API路径，用于单独转换指定API')


def main():
    args = parser.parse_args()
    if args.version:
        logger.info(f"当前版本：{version}")
        exit(0)
    arguments = parser.parse_args()
    if not arguments.url:
        logger.error("Swagger API地址为必填项")
    SwaggerParser(arguments.url, arguments.username, arguments.password).gen_testcase(arguments.path)


if __name__ == '__main__':
    main()
