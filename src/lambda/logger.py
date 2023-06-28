import logging


def setup_logger():
    
    logger = logging.getLogger("ApiRest")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    return logger