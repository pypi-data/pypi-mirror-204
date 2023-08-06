
from functools import wraps
import time
import logging
import datetime
from . import access

class CloudLogger():
    def __init__(self, app_logger_name, module_name, logger_level=10):
        self.LOGGER_LEVEL = logger_level
        self.logger = self._get_logger(app_logger_name=app_logger_name, module_name=module_name)

        
    def _get_logger(self, app_logger_name, module_name):
        FMT = "[{levelname:^9}] {name}: {message}"
        FORMATS = {
            logging.DEBUG: FMT,
            logging.INFO: "\33[36m{fmt}\33[0m".format(fmt=FMT),
            logging.WARNING: "\33[33m{fmt}\33[0m".format(fmt=FMT),
            logging.ERROR: "\33[31m{fmt}\33[0m".format(fmt=FMT),
            logging.CRITICAL: "\33[1m\33[31m{fmt}\33[0m".format(fmt=FMT)
        }



        class CustomFormatter(logging.Formatter):
            def format(self, record):
                log_fmt = FORMATS[record.levelno]
                formatter = logging.Formatter(log_fmt, style="{")
                return formatter.format(record)

        

        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logging.basicConfig(
            level=self.LOGGER_LEVEL,
            handlers=[handler]
        )

        logger = logging.getLogger(app_logger_name).getChild(module_name)
        return logger


    def timeit(self, func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            self.logger.log(msg=f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds', level=logging.INFO)
            #logging.log(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds', level=logging.DEBUG)
            return result
        return timeit_wrapper




    def except_block(self, inst, exceptionMessage="No message"):
        exceptionMessage = exceptionMessage
        exceptionTimne = str(datetime.datetime.now())
        exceptionType = str(type(inst))
        exceptionArgument = str(inst.args)
        exceptionInstance = str(inst)
        self.logger.log(msg="Exception message: {message}".format(message=exceptionMessage), level=logging.ERROR)
        self.logger.log(msg="Exception occured at: {message}".format(message=exceptionTimne), level=logging.ERROR)
        self.logger.log(msg="Exception instance type: {message}".format(message=exceptionType), level=logging.ERROR)
        self.logger.log(msg="Exception argument: {message}".format(message=exceptionArgument), level=logging.ERROR)
        self.logger.log(msg="Exception instance: {message}".format(message=exceptionInstance), level=logging.ERROR)

