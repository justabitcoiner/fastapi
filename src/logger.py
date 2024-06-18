import os
import logging
from uvicorn.logging import ColourizedFormatter
from src.config import Configuration

config = Configuration.get_config()


def get_logger(conf):
    level = conf.get("level") or "WARNING"
    directory = conf.get("directory") or "logs"
    filename = conf.get("filename") or "app.log"

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.propagate = False

    stream_handler = create_stream_handler()
    logger.addHandler(stream_handler)

    file_path = get_path(directory, filename)
    file_handler = create_file_handler(file_path)
    logger.addHandler(file_handler)

    return logger


def create_stream_handler():
    handler = logging.StreamHandler()
    formatter = ColourizedFormatter("[%(asctime)s] %(levelprefix)s %(message)s")
    handler.setFormatter(formatter)
    return handler


def create_file_handler(filename):
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    return handler


def get_path(directory, filename):
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, filename)


logger = get_logger(config["log"])  # Root logger
