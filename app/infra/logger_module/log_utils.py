import logging


class LogUtils(logging.Logger):
    
    """
    This class create a log in your project

    :param tag: Small text that represents your project.
    :param logger_format: Show info line.
    :param mask_date: Date format info.
    :return:
    """

    def __init__(
        self, 
        tag: str, 
        logger_format: str = "%(asctime)s|{}|%(levelname)s|%(message)s", 
        mask_date: str = "%d/%m/%Y|%H:%M:%S"
        ):

        logging.Logger.__init__(self, tag)

        logger_format = logger_format.format(tag)

        self.formatter = logging.Formatter(logger_format, mask_date)

        self.__set_handlers(self.formatter)


    def __set_handlers(self, formatter):
        """
        Add formatter in Logger instance.

        :param formatter: Config Handler
        :return:
        """

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.addHandler(sh)

    def __del__(self):
        """ Destroy handlers log """
        
        try:
            map(self.removeHandler, self.handlers)
        except Exception:
            pass
