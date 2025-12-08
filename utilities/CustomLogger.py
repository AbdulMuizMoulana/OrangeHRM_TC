import logging


class LogMaker:
    @staticmethod
    def log_gen():
        logging.basicConfig(filename=r'.\\logs\\orangehrm_test_logs',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%d-%b-%Y %I:%M:%S %p', force=True)
        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)
        return logger


