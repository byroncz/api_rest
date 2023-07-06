import logging



def setup_logger():
    """
    The function `setup_logger` sets up a logger named "ApiRest" with a logging level of INFO and a
    specific log message format.
    :return: a logger object.
    """
    logger = logging.getLogger("ApiRest")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    return logger