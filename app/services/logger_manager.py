import logging


class LoggerManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def setup(self):
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        file_handler = logging.FileHandler('application.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        return self.logger
