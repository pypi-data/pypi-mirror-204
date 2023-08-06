import logging
import os

log_path = 'log.txt'


class LogHandler:

    @staticmethod
    def get_log_handler(name, level="info"):
        log_level = LogHandler._get_log_level(level)
        logger = logging.getLogger(name)
        logger.setLevel(level=log_level)

        if os.path.exists(log_path):
            # handler = RotatingFileHandler(filename=log_path, maxBytes=1024, backupCount=1)
            log_size = round(os.path.getsize(log_path) / float(1024), 2)
            if log_size > 5.0:  # 如果文件大于5KB
                os.remove(log_path)

            handler = logging.FileHandler(filename=log_path)
            handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @staticmethod
    def _get_log_level(level: str):
        if level == "warning":
            return logging.WARNING
        elif level == "info":
            return logging.INFO
        elif level == "debug":
            return logging.DEBUG
        elif level == "error":
            return logging.ERROR
        elif level == "critical":
            return logging.CRITICAL
        else:
            raise Exception("Given log level is invalid.")



