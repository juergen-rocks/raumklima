import configparser
from os import getenv
import os.path
import pathlib


class ConfigProvider(object):

    def __init__(self, file: str):
        self.__config = configparser.ConfigParser()
        self.__config.optionxform = str
        with open(file, 'r') as fp:
            self.__config.read_file(fp)

    def get_config(self) -> configparser.ConfigParser:
        return self.__config


def discover_config_file_by_name(filename: str, script_dir: str=None, env_var: str='RS500_CONFIG_PATH') -> str:
    if script_dir is not None:
        candidate = os.path.join(script_dir, filename)
        if os.path.exists(candidate) and os.path.isfile(candidate):
            return candidate
    if env_var is not None:
        env_var_value = getenv(env_var, None)
        if env_var_value is not None:
            candidate = os.path.join(env_var_value, filename)
            if os.path.exists(candidate) and os.path.isfile(candidate):
                return candidate
    candidate = os.path.join(str(pathlib.Path.home().absolute()), '.rs500', filename)
    if os.path.exists(candidate) and os.path.isfile(candidate):
        return candidate
    candidate = os.path.join('/etc', filename)
    if os.path.exists(candidate) and os.path.isfile(candidate):
        return candidate
    raise FileNotFoundError('Unable to find configuration file "{}"'.format(filename))
