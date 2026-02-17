#Import Packages
import time
import json
import logging
import os

def set_up_logger(function_name):
        
#############################
# This function creates a logger to organise logs for each function into INFO, WARNING, 
# and ERROR logs. Just set up in your code as logger = set_up_logger(function.__name__) 
# and you will be able to log anything using logger.info('Log message') 
#############################

        # Set Up Logging
        logger = logging.getLogger(function_name)
        logger.setLevel(logging.DEBUG)  # Capture everything, handlers decide what to save

        #Set Up Logger Format
        log_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ) # Configure logging

        #Set up Log file Name
        ts = int(time.time())
        output_file = f"{function_name}_log_{ts}.log"

        #Set up Different Paths for different Levels of Logging (Info)
        info_dir = f"logs/{function_name}/INFO"
        os.makedirs(info_dir, exist_ok=True)
        info_log = logging.FileHandler(f"logs/{function_name}/INFO/{output_file}", encoding="utf-8")
        logger.addHandler(info_log)
        info_log.setLevel(logging.INFO)
        info_log.setFormatter(log_format)
        info_log.addFilter(lambda record: record.levelno == logging.INFO)

        #Set up Different Paths for different Levels of Logging (Warning)
        warning_dir = f'logs/{function_name}/WARNING'
        os.makedirs(warning_dir, exist_ok=True)
        Warning_log = logging.FileHandler(f"logs/{function_name}/WARNING/" + output_file, encoding="utf-8")
        logger.addHandler(Warning_log)
        Warning_log.setLevel(logging.WARNING)
        Warning_log.setFormatter(log_format)
        Warning_log.addFilter(lambda record: record.levelno == logging.WARNING)

            #Set up Different Paths for different Levels of Logging (ERROR)
        error_dir = f'logs/{function_name}/ERROR'
        os.makedirs(error_dir, exist_ok=True)
        error_log = logging.FileHandler(f"logs/{function_name}/ERROR/" + output_file, encoding="utf-8")
        logger.addHandler(error_log)
        error_log.setLevel(logging.ERROR)
        error_log.setFormatter(log_format)
        error_log.addFilter(lambda record: record.levelno == logging.ERROR)

        return logger