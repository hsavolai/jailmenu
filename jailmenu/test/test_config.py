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


from config import ConfigManager, JMConfigException, FileSystemItem
from mock import patch, Mock, call, MagicMock
import os
import ConfigParser
import mock
from nose.tools import raises


def test_realize_path():
    assert "/baz" == ConfigManager.realize_path("/foo/../bar/../baz")
    os.path.abspath = Mock(return_value="/baz")
    assert "/baz" == ConfigManager.realize_path("../baz")

    os.path.expanduser = Mock(return_value="/home/foobar")
    assert "/home/foobar" == ConfigManager.realize_path("~foobar/")


@raises(JMConfigException)
def test_config_file_not_found():
    os.path.isfile = Mock(return_value=False)
    ConfigManager("/tmp/jailmenu.conf")


@mock.patch("config.ConfigParser.SafeConfigParser")
@raises(JMConfigException)
def test_config_file_broken(mock):
    os.path.isfile = Mock(return_value=True)
    mock.return_value.read.side_effect = ConfigParser.Error
    ConfigManager("/tmp/jailmenu.conf")


@mock.patch("config.ConfigParser.SafeConfigParser")
def test_config_file_parsing(mock):
    os.path.isfile = Mock(return_value=True)
    os.path.exists = Mock(return_value=True)
    os.path.isdir = Mock(return_value=True)
    os.path.expanduser = Mock(return_value="/foo")
    os.listdir = Mock()
    mock.return_value.sections.return_value = ["config", "path:/foo"]
    mock.return_value.options = lambda x: {
                                      "config": ["log_level"],
                                      "path:/foo": ["allow_file_listing"]
                                      }[x]
    mock.return_value.get.return_value = "DEBUG"
    mock.return_value.getboolean.return_value = True

    cm = ConfigManager("/tmp/jailmenu.conf")
    assert cm.system_config.log_level == "DEBUG"
    print cm.fs_items[0].path
    assert cm.fs_items[0].path == "/foo"
    assert cm.fs_items[0].allow_file_listing == True


def test_fs_item_validation():
    os.path.exists = Mock(return_value=False)
    fs_item = FileSystemItem("/foo")
    assert any("not exist" in s for s in fs_item.validate()) == True
    os.path.exists = Mock(return_value=True)
    os.path.isdir = Mock(return_value=True)
    os.listdir.side_effect = OSError
    fs_item = FileSystemItem("/foo")
    fs_item.allow_file_listing = True
    assert any("allow_file_listing" in s for s in fs_item.validate()) == True
