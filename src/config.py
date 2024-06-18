import os, configparser


class Configuration:
    __config: dict = None

    @classmethod
    def load_config(cls, filename=".env"):
        if not os.path.exists(filename):
            raise FileNotFoundError("Configuration file not found")

        parser = configparser.ConfigParser()
        parser.read(filename)

        cls.__config = {}
        for section in parser.sections():
            cls.__config[section] = {}
            for key, val in parser.items(section):
                cls.__config[section][key] = val

    @classmethod
    def get_config(cls):
        if cls.__config is None:
            raise Exception("Configuration has not yet loaded")
        return cls.__config


Configuration.load_config()
