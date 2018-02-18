import configparser


class ConfigProvider(object):

    def __init__(self, file: str):
        self.__config = configparser.ConfigParser()
        self.__config.optionxform = str
        self.__config.read(file)

    def get_config(self):
        return self.__config
