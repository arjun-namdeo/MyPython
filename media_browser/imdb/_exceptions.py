"""
_exceptions module (imdb package).
"""

import logging


class IMDbError(Exception):
    """Base class for every exception raised by the imdb package."""
    _logger = logging.getLogger('media_browser')

    def __init__(self, *args, **kwargs):
        """Initialize the exception and pass the message to the log system."""
        # Every raised exception also dispatch a critical log.
        self._logger.critical('%s exception raised; args: %s; kwds: %s',
                                self.__class__.__name__, args, kwargs,
                                exc_info=True)
        Exception.__init__(self, *args, **kwargs)

class IMDbDataAccessError(IMDbError):
    """Exception raised when is not possible to access needed data."""
    pass

class IMDbParserError(IMDbError):
    """Exception raised when an error occurred parsing the data."""
    pass

