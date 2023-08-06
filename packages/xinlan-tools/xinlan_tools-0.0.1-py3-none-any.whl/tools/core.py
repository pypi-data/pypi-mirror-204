#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2023/4/20 04:25
# @Author  : 心蓝
# @email   : 117220100@qq.com
# @微信号  : hhxpython
import os
import sys
from argparse import ArgumentParser


class TestProgram:
    def __init__(self, args=None):
        self.args = args or sys.argv[1:]

    def parse_args(self, args):
        if sys.version < '3.9':
            parser = ArgumentParser(description='xinlan-tools 命令行参数帮助')
        else:
            parser = ArgumentParser(description='xinlan-tools 命令行参数帮助', exit_on_error=False)
        parser.add_argument('file_or_dir', nargs='?', type=str, help='路径，或需要加密的文件')
        parser.add_argument('--number', type=int, default=10, help='加密用字节数')
        if args:
            self.args = vars(parser.parse_args(args))
        else:
            self.args = vars(parser.parse_args())

    def fetch_command(self, subcommand):
        if subcommand == 'encrypt':
            from .commands.encrypt import Command
            return Command()

    def execute(self):
        try:
            subcommand = self.args[0]
        except IndexError:
            subcommand = 'help'

        self.fetch_command(subcommand).run_from_argv(self.args[1:])


if __name__ == '__main__':
    TestProgram().execute()