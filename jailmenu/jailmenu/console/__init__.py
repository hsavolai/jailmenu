#!/usr/bin/env python
# encoding: utf-8
'''
This file is part of Jailmenu program, which is a console jail
to provide secure access to a system.

Jailmenu program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


@author:     Harri Savolainen
@copyright:  Harri Savolainen 2014. All rights reserved.
@license:    GPLv2
@contact:    harri.savolainen@gmail.com
@deffield    updated: Updated
'''


import sys
import cmd
import os
import time
from datetime import datetime


class ConsoleManager(cmd.Cmd):

    _fs_items = None
    _system_config = None
    last_output = ''
    _cwd = "/"

    def __init__(self, config_manager):
        cmd.Cmd.__init__(self)
        self._fs_items = config_manager.fs_items
        self._system_config = config_manager.system_config
        os.chdir(self._cwd)
        self.create_prompt()

    def create_prompt(self):
        self.prompt = "[" + os.getcwd() + "]>"

    def postcmd(self, stop, line):
        self.create_prompt()
        return cmd.Cmd.postcmd(self, stop, line)

    def do_cd(self, line):
        try:
            os.chdir(line)
        except OSError as err:
            print(repr(err))

    def do_ls(self, line):
        "List files in directory"
        output = os.popen("/bin/ls " + line).read()
        print output

    def do_EOF(self, line):
        print ""
        sys.exit(0)

    def do_exit(self, line):
        sys.exit(0)


