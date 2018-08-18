import configparser
from os import getenv
from os.path import join, exists, isfile
from pathlib import Path


class ConfigProvider(object):

    def __init__(self, file: str):
        self.__config = configparser.ConfigParser()
        self.__config.optionxform = str
        self.__config.read(file)

    def get_config(self) -> configparser.ConfigParser:
        return self.__config


def discover_config_file_by_name(filename: str, script_dir: str=None, env_var: str='RS500_CONF_PATH') -> str:
    if script_dir is not None:
        candidate = join(script_dir, filename)
        if exists(candidate) and isfile(candidate):
            return candidate
    if env_var is not None:
        env_var_value = getenv(env_var, None)
        if env_var_value is not None:
            candidate = join(env_var_value, filename)
            if exists(candidate) and isfile(candidate):
                return candidate
    candidate = join(str(Path.home().absolute()), '.rs500', filename)
    if exists(candidate) and isfile(candidate):
        return candidate
    candidate = join('/etc', filename)
    if exists(candidate) and isfile(candidate):
        return candidate
    raise FileNotFoundError('Unable to find configuration file "{}"'.format(filename))
