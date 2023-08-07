# This file is placed in the Public Domain.
# pylint: disable=E0402


"runtime"


from .objects import Default


Cfg = Default()
Cfg.debug = False
Cfg.name = "operbot"
Cfg.skip = "PING,PONG"
Cfg.verbose = False
