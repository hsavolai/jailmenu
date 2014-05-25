'''
This file is part of Jailmenu program, which is a console jail
to provide secure access to a system.

This is part of Jailmenu program, which is free software:
you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option)
any later version.

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

import ConfigParser
import os
from nose import case


class ConfigManager():
    '''
    ConfiguratioManager
    '''
    _config_file = None
    fs_items = []
    system_config = None
    FS_SEP = 'path:'
    CNF_SEP = 'config'

    @staticmethod
    def realize_path(path):
        path = os.path.expanduser(path)
        if os.path.isabs(path) == False:
            path = os.path.abspath(path)
        return os.path.normpath(path)

    def __init__(self, config_file):
        self.system_config = SystemConfig()
        self._config_file = ConfigManager.realize_path(config_file)
        self.parse_config_file()

    def parse_config_file(self):
        try:
            config_parser = ConfigParser.SafeConfigParser()
            if os.path.isfile(self._config_file):
                config_parser.read(self._config_file)
                for section in config_parser.sections():
                    # Parse Main configuration
                    if section == self.CNF_SEP:
                        self._parse_system_config(section, config_parser)
                    # Parse FS path configurations
                    if section.startswith(self.FS_SEP):
                        self._parse_fs_path_config(section, config_parser)
            else:
                raise JMConfigException("Configuration file (" +
                                        self._config_file +
                                        ") not found!")
        except ConfigParser.Error as ex:
            raise JMConfigException("Configuration file parsing error! " +
                                    "See doc for details. Details:(" +
                                    ex._get_message() + ")")

    def _parse_fs_path_config(self, section, config_parser):

        path = section.replace(self.FS_SEP, '')
        fs_item = FileSystemItem(ConfigManager.realize_path(path))

        for option in config_parser.options(section):
            if option == 'allow_access_subdir':
                fs_item.allow_access_subdir = (config_parser
                        .getboolean(section,
                        'allow_access_subdir'))
            if option == 'allow_file_listing':
                fs_item.allow_file_listing = (config_parser
                        .getboolean(section,
                        'allow_file_listing'))
            if option == 'allow_file_copy':
                fs_item.allow_file_copy = (config_parser
                        .getboolean(section,
                        'allow_file_copy'))

        for issue in fs_item.validate():
            print("Warn: " + issue)

        if not fs_item.disabled:
            self.fs_items.append(fs_item)

        if self.fs_items.__len__() == 0:
            raise JMConfigException("Configuration file (" +
                                    self._config_file +
                                    ") empty!")

    def _parse_system_config(self, section, config_parser):
        for option in config_parser.options(section):
            if option == 'log_level':
                self.system_config.log_level = (config_parser.get(section,
                        'log_level'))
            if option == 'log_path':
                self.system_config.log_path = (config_parser.get(section),
                        'log_path')


# pylint: disable=R0903
class FileSystemItem():
    '''
    FileSystemItem
    '''
    path = None
    allow_access_subdir = False
    allow_file_listing = False
    allow_file_copy = False
    disabled = False

    def __init__(self, path):
        self.path = path

    def validate(self):
        validation_issues = []
        if not os.path.exists(self.path):
            validation_issues.append("Path not exist or accessible. " +
                                           "File/directory ignored. (" +
                                           self.path + ")")
            self.disabled = True
        if not self.disabled:
            if os.path.isdir(self.path):
                if self.allow_file_listing == True:
                    try:
                        os.listdir(self.path)
                    except OSError as err:
                        validation_issues.append("Unable to access, " +
                                                 "ignoring " +
                                                 "allow_file_listing (" +
                                                 repr(err) + ") for " +
                                                 "files for " + self.path)
                        self.allow_file_listing = False
            else:
                if self.allow_access_subdir == True:
                    validation_issues.append("File, ignoring: " +
                                                   "allow_access_subdir for " +
                                                   self.path)
                    self.allow_access_subdir = False

                if self.allow_file_listing == True:
                    validation_issues.append("File, ignoring: " +
                                                   "allow_file_listing for "
                                                   + self.path)
                    self.allow_file_listing = False

        return validation_issues

    def __str__(self):
        return (self.path)

    def __repr__(self):
        return self.__str__()


class SystemConfig():

    log_file = "~/jailmenu.log"
    log_level = "INFO"

    def __init__(self):
        pass


class JMConfigException(Exception):
    '''
    JMConfigException
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
