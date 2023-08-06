#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/4/21 05:56
# @Author  : 心蓝
# @email   : 117220100@qq.com
# @微信号  : hhxpython
from argparse import ArgumentParser
import sys

from PIL import Image


class Command:
    def __init__(self):
        pass

    def run_from_argv(self, argv):
        self.parse_args(argv)
        source = self.args['source']
        target = self.args['target']
        if 'jpg' in target.lower():
            Image.open(source).convert('RGB').save(target)
        else:
            Image.open(source).convert('RGBA').save(target)


    def parse_args(self, args):
        if sys.version < '3.9':
            parser = ArgumentParser(description='xinlan-tools 命令行参数帮助')
        else:
            parser = ArgumentParser(description='xinlan-tools 命令行参数帮助', exit_on_error=False)
        parser.add_argument('source', nargs='?', type=str, help='需要转换的源文件名')
        parser.add_argument('target', type=str, nargs='?', help='要转换成的目标文件名')

        self.args = vars(parser.parse_args(args))