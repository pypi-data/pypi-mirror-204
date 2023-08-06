import logging
from os import getenv
import sys


def config(
        logging_level : str = "INFO",
        libs_to_silence : list = None,
        env_var_force_timestamp : list = None
    ):
    
    # Set higher level for external libs logging
    if libs_to_silence is None:
        libs_to_silence = [
            'botocore',
            'boto3',
            'urllib',
            'urllib3',
            'azure',
            'uamqp',
            'py4j',
        ]
    for lib in libs_to_silence:
            logging.getLogger(lib).setLevel(logging.ERROR)

    LOGGING_LEVEL = getenv('LOGGING_LEVEL', logging_level)

    # Local execution shows time. Remote executions logging has it's own timestamp adding
    if env_var_force_timestamp is not None and getenv(env_var_force_timestamp, None) is not None:
        log_format = '%(asctime)s - %(levelname)s - %(filename)s[%(lineno)s] %(message)s'
    else:
        log_format = '%(levelname)s - %(filename)s[%(lineno)s] %(message)s'

    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(handler)
    logger.setLevel(LOGGING_LEVEL)
    
    return logger
