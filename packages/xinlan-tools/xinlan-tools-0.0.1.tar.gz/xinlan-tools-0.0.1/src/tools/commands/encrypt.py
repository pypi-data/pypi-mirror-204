#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/4/20 05:59
# @Author  : 心蓝
# @email   : 117220100@qq.com
# @微信号  : hhxpython
from argparse import ArgumentParser
import os
import sys


class Command:
    def __init__(self):
        pass

    def run_from_argv(self, argv):
        self.parse_args(argv)
        if self.args['file_or_dir'] is None:
            raise ValueError('请指定要加密的文件或路径')
        if not os.path.exists(self.args['file_or_dir']):
            raise ValueError(f'{self.args["file_or_dir"]}不存在')

        if os.path.isfile(self.args['file_or_dir']):
            self.encrypt(self.args['file_or_dir'])
        else:
            for r, d, f in os.walk(self.args['file_or_dir']):
                for file in f:
                    self.encrypt(os.path.join(r, file))

    def parse_args(self, args):
        if sys.version < '3.9':
            parser = ArgumentParser(description='xinlan-tools 命令行参数帮助')
        else:
            parser = ArgumentParser(description='xinlan-tools 命令行参数帮助', exit_on_error=False)
        parser.add_argument('file_or_dir', nargs='?', type=str, help='路径，或需要加密的文件')
        parser.add_argument('--number', type=int, default=10, help='加密用字节数')

        self.args = vars(parser.parse_args(args))

    def encrypt(self, file):
        with open(file, 'rb+') as f:
            first = f.read(self.args['number'])
            f.seek(0-self.args['number'], 2)
            last = f.read()
            f.seek(0)
            f.write(last)
            f.seek(0-self.args['number'], 2)
            f.write(first)
        print(f'处理文件{file}完成')
