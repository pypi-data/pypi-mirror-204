# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402


"logging"


import logging
import logging.handlers
import os


from .handler import spl
from .persist import Persist, cdir, touch
from .runtime import Cfg


LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL
         }


RLEVELS = {logging.DEBUG: 'debug',
           logging.INFO: 'info',
           logging.WARNING: 'warn',
           logging.ERROR: 'error',
           logging.CRITICAL: 'critical'
          }


class Logging:

    @staticmethod
    def debug(txt):
        if not doskip(txt, Cfg.skip):
            Logging.raw(txt)

    @staticmethod
    def raw(txt):
        pass


def doskip(txt, skipping):
    for skip in spl(skipping):
        if skip in txt:
            return True
    return False


def getlevel():
    root = logging.getLogger()
    return RLEVELS.get(root.level)


def setlevel(name="info"):
    logfile = os.path.join(Persist.logdir(), "%s.log" % Cfg.name)
    cdir(logfile)
    touch(logfile)
    fplain = "%(message)s"
    datefmt = '%H:%M:%S'
    formatter_plain = logging.Formatter(fplain, datefmt=datefmt)
    try:
        filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
    except (IOError, AttributeError) as ex:
        Logging.debug("can't create file loggger %s" % str(ex))
        filehandler = None
    level = LEVELS.get(str(name).lower(), logging.NOTSET)
    root = logging.getLogger()
    root.setLevel(level)
    if root and root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)
    chl = logging.StreamHandler()
    chl.setLevel(level)
    chl.setFormatter(formatter_plain)
    root.addHandler(chl)
    if filehandler:
        root.addHandler(filehandler)
    Logging.debug("loglevel is %s" % name)
