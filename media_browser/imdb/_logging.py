"""
_logging module (imdb package).
"""

import logging

LEVELS = {'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL}


imdbpyLogger = logging.getLogger('media_browser')
imdbpyStreamHandler = logging.StreamHandler()
imdbpyFormatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]' \
                                    ' %(pathname)s:%(lineno)d: %(message)s')
imdbpyStreamHandler.setFormatter(imdbpyFormatter)
imdbpyLogger.addHandler(imdbpyStreamHandler)

def setLevel(level):
    """Set logging level for the main logger."""
    level = level.lower().strip()
    imdbpyLogger.setLevel(LEVELS.get(level, logging.NOTSET))
    imdbpyLogger.log(imdbpyLogger.level, 'set logging threshold to "%s"',
                    logging.getLevelName(imdbpyLogger.level))


#imdbpyLogger.setLevel(logging.DEBUG)


# It can be an idea to have a single function to log and warn:
#import warnings
#def log_and_warn(msg, args=None, logger=None, level=None):
#    """Log the message and issue a warning."""
#    if logger is None:
#        logger = imdbpyLogger
#    if level is None:
#        level = logging.WARNING
#    if args is None:
#        args = ()
#    #warnings.warn(msg % args, stacklevel=0)
#    logger.log(level, msg % args)

