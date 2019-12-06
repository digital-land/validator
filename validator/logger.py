import logging

handler = logging.StreamHandler()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    return logger
