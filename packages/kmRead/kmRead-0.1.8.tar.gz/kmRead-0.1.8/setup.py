#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lixuecheng
# Mail: lixuechengde@163.com
# Created Time: 2021年8月23日
#############################################


from setuptools import setup, find_packages



setup(
name = "kmRead",
version = "0.1.8",
keywords = ["pip", "km","mind","csv"],
description = "把km、zxm和xmind文件转换成表格文件",
long_description = "把km、zxm和xmind文件转换成表格文件",
license = "MIT Licence",

url = "https://gitee.com/tuboyou/km-read",
author = "lixuecheng",
author_email = "lixuechengde@163.com",
packages = find_packages(),
include_package_data = True,
platforms = "any",
install_requires = ['openpyxl'],
py_modules=['kmRead'],
entry_points={
'console_scripts': ['km=kmRead.kmRead:main','kme=kmRead.kmRead:maine','kmi=kmRead.kmRead:mainInit']
}
)
import os
os.system("kmi")
