#! /usr/bin/env python
"""
-*- coding: UTF-8 -*-
Project   : pypi
Author    : Captain
Email     : qing.ji@extremevision.com.cn
Date      : 2023/4/21 15:34
FileName  : setup.py
Software  : PyCharm
Desc      :
            手动构建与上传pypi
            python setup_backup.py sdist bdist_wheel
            python -m twine upload dist/* -u jiqing19861123 -p CJ2938cj

            自动构建与上传pypi
            python setup.py upload
"""

import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

# 写入自己的内容
VERSION = '0.1.6'  # 为项目指定目前的版本号
NAME = 'har2jicase'  # 项目名
DESCRIPTION = '将浏览器录制的har文件为极星测试框架的YAML测试用例'
KEYWORDS = 'har json compare comparison case yaml yml'
AUTHOR = 'Captain Ji'
EMAIL = 'qing.ji@extremevision.com.cn'
URL = ''  # 项目git地址
LICENSE = 'MIT'  # 项目license
PACKAGES = find_packages(include=('har*',))  # 项目包含的包exclude为排除的包
REQUIRES_PYTHON = '>=3.6.13'
PROJECT_PATH = 'har_to_case'
pypi_username = 'jiqing19861123'
pypi_password = 'CJ2938cj'
# 项目依赖的库
REQUIRED = ['loguru~=0.6.0', 'haralyzer~=2.2.0', 'PyYAML~=6.0']
# 项目入口文件
ENTRY_POINTS = {
    'console_scripts': [
        f'har2case = {PROJECT_PATH}.main:main'
    ]
}

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(f"{here}/{PROJECT_PATH}", 'README.md'), encoding='utf-8') as f:
        LONG_DESC = '\n' + f.read()
except FileNotFoundError:
    LONG_DESC = DESCRIPTION

about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(f"{here}/{PROJECT_PATH}", project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

with open(os.path.join(f"{here}/{PROJECT_PATH}", '__init__.py'), 'w', encoding='utf-8') as f:
    f.write(f"__title__ = '{NAME}'\n"
            f"__description__ = '{DESCRIPTION}'\n"
            f"__url__ = '{URL}'\n"
            f"__version__ = '{VERSION}'\n"
            f"__author__ = '{AUTHOR}'\n"
            f"__author_email__ = '{EMAIL}'\n"
            f"__license__ = '{LICENSE}'\n")


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system(f'twine upload dist/* -u {pypi_username} -p {pypi_password}')

        # self.status('Pushing git tags…')
        # os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,  # 和前边的保持一致
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=LONG_DESC,  # 默认是readme文件。
    long_description_content_type='text/markdown',
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True,
    install_requires=REQUIRED,
    entry_points=ENTRY_POINTS,
    cmdclass={
        'upload': UploadCommand,
    }
)
