# flake8: noqa

from datetime import datetime
import logging


def debug_logger(method):
    def internal(cls, *args, **kwargs):
        logging.info(f"{cls.__class__}.{method.__name__}() initiated.")
        start = datetime.now()
        result = method(cls, *args, **kwargs)
        end = datetime.now()
        duration = (end-start).total_seconds()
        logging.info(f"{cls.__class__}.{method.__name__}() complete in {duration:.1f} seconds.")
        return result
    return internal
