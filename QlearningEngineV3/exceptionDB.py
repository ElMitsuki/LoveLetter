import linecache
import sys
import functools
import logging

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("dbAccess")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    fh = logging.FileHandler("QlearningEngine/log/dbAccess.log")
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger

def log(log_enabled, logger):
    def exception(function):
        """
        A decorator that wraps the passed in function and logs 
        exceptions should one occur
        """
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except:
                if log_enabled:
                    # log the exception
                    err = "There was an exception in  "
                    err += function.__name__
                    logger.exception(err)
                raise
        return wrapper
    return exception
