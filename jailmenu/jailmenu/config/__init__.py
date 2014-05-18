

import ConfigParser
import os
from nose import case


class ConfigManager():
    _config_file = None
    fs_items = []

    @staticmethod
    def realize_path(path):
        path = os.path.expanduser(path)
        if os.path.isabs(path) == False:
            path = os.path.abspath(path)
        return os.path.normpath(path)

    def __init__(self, config_file):
        self._config_file = ConfigManager.realize_path(config_file)
        self.parse_config_file()

    def print_config_file(self):
        print(self._config_file)

    def parse_config_file(self):
        try:
            config_parser = ConfigParser.SafeConfigParser()
            if os.path.isfile(self._config_file):
                config_parser.read(self._config_file)
                for path in config_parser.sections():
                    fs_item = FilesystemItem(ConfigManager
                                          .realize_path(path))
                    for option in config_parser.options(path):
                        if option == 'allow_access_subdir':
                            fs_item.allow_access_subdir = (config_parser
                                    .getboolean(path, 'allow_access_subdir'))
                        if option == 'allow_file_listing':
                            fs_item.allow_file_listing = (config_parser
                                    .getboolean(path, 'allow_file_listing'))
                        if option == 'allow_file_copy':
                            fs_item.allow_file_copy = (config_parser
                                    .getboolean(path, 'allow_file_copy'))
                    for issue in fs_item.validate():
                        print("Warn: " + issue)
                    if not fs_item.disabled:
                        self.fs_items.append(fs_item)
                if self.fs_items.__len__() == 0:
                    raise JMConfigException("Configuration file (" +
                                            self._config_file +
                                            ") empty!")
            else:
                raise JMConfigException("Configuration file (" +
                                        self._config_file +
                                        ") not found!")
        except ConfigParser.Error as ex:
            raise JMConfigException("Configuration file parsing error! " +
                                    "See doc for details. Details:(" +
                                    ex._get_message() + ")")


class FilesystemItem():
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
        return ("path:" + self.path)

    def __repr__(self):
        return self.__str__()


class JMConfigException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
