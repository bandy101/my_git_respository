import logging
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


class Log:
    def __init__(self, prefix: str, log_name: str):
        self.__prefix = prefix
        self.__log_name = log_name

    def _log(self, level, msg, *args, **kwargs):
        msg = "{prefix}{msg}".format(prefix=self.__prefix, msg=msg)
        logging.getLogger(self.__log_name).log(level, msg, *args, **kwargs)

    def _debug(self, msg, *args, **kwargs):
        self._log(DEBUG, msg, *args, **kwargs)

    def _info(self, msg, *args, **kwargs):
        self._log(INFO, msg, *args, **kwargs)

    def _warning(self, msg, *args, **kwargs):
        self._log(WARNING, msg, *args, **kwargs)

    def _error(self, msg, *args, **kwargs):
        self._log(ERROR, msg, *args, **kwargs)

    def _critical(self, msg, *args, **kwargs):
        self._log(CRITICAL, msg, *args, **kwargs)
