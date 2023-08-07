#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0413,W0212,E0611,E0401,E0402,I1101


'OTP-CR-117/19'


import os
import readline
import sys
import termios
import time
import traceback


sys.path.insert(0, os.getcwd())


from . import modules


from .handler import Client, Error, command, parse
from .loggers import Logging
from .objects import update
from .persist import Persist
from .runtime import Cfg
from .scanner import importer, scandir, scanpkg, starter
from .threads import launch


readline.redisplay()


MOD = "cmd,err,irc,log,rss,sts,tdo,thr"


Persist.workdir = os.path.expanduser("~/.%s" % Cfg.name)


date = time.ctime(time.time()).replace('  ', ' ')


def cprint(txt):
    if "v" in Cfg.opts:
        print(txt)
        sys.stdout.flush()


Logging.debug = cprint


class CLI(Client):

    @staticmethod
    def announce(txt):
        pass

    @staticmethod
    def raw(txt):
        print(txt)
        sys.stdout.flush()


class Console(CLI):

    def handle(self, evt):
        CLI.handle(self, evt)
        evt.wait()

    def poll(self):
        return self.event(input("> "))


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open('/dev/null', 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    sos = open('/dev/null', 'a+')
    ses = open('/dev/null', 'a+')
    os.dup2(sos.fileno(), sys.stdout.fileno())
    os.dup2(ses.fileno(), sys.stderr.fileno())


def waiter():
    got = []
    for ex in Error.errors:
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        got.append(ex)
    for exc in got:
        Error.errors.remove(exc)


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print('')
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)
        waiter()


def main():
    dowait = False
    cfg = parse(' '.join(sys.argv[1:]))
    update(Cfg, cfg)
    if os.path.exists("modules"):
        scandir("modules", importer, cfg.mod or MOD)
    scanpkg(modules, importer, cfg.mod or MOD)
    if cfg.txt:
        cli = CLI()
        command(cli, cfg.otxt)
    elif 'd' in cfg.opts:
        daemon()
        dowait = True
    elif 'c' in cfg.opts:
        print(f'{Cfg.name.upper()} started {date}')
        dowait = True
    if dowait:
        scanpkg(modules, starter, cfg.mod or MOD)
        scandir("modules", starter, cfg.mod or MOD)
        if "c" in cfg.opts:
            csl = Console()
            launch(csl.loop)
        while 1:
            time.sleep(1.0)
            waiter()


if __name__ == "__main__":
    wrap(main)
    waiter()
