# Tihs file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402


"persistence"


import json
import os
import pathlib
import time
import _thread


from .objects import Default, Object, ObjectDecoder, ObjectEncoder
from .objects import kind, search, update


def __dir__():
    return (
            'Persist',
            'cdir',
            'last',
            'find',
            'read',
            'setwd',
            'write'
           )


__all__ = __dir__()


disklock = _thread.allocate_lock()


class NoClassError(Exception):

    "class is not registered"


class Class:

    cls = Default()

    @staticmethod
    def add(clz):
        setattr(Class.cls, "%s.%s" % (clz.__module__, clz.__name__), clz)

    @staticmethod
    def get(cmd):
        return getattr(Class.cls, cmd, None)

    @staticmethod
    def match(mtc):
        mtc = mtc.lower()
        for clz in Class.cls:
            if mtc == clz.split(".")[-1].lower():
                yield clz

    @staticmethod
    def remove(cmd):
        del Class.cls[cmd]


class Persist(Object):

    workdir = ""

    @staticmethod
    def logdir():
        return os.path.join(Persist.workdir, "logs")


def cdir(pth) -> None:
    if not pth.endswith(os.sep):
        pth = os.path.dirname(pth)
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def dump(*args, **kw) -> None:
    kw["cls"] = ObjectEncoder
    return json.dump(*args, **kw)


def files() -> []:
    return os.listdir(os.path.join(Persist.workdir, "store"))


def fns(mtc) -> []:
    assert Persist.workdir
    dname = ''
    lst = mtc.lower().split(".")[-1]
    for rootdir, dirs, _files in os.walk(Persist.workdir, topdown=False):
        if dirs:
            dname = sorted(dirs)[-1]
            if dname.count('-') == 2:
                ddd = os.path.join(rootdir, dname)
                fls = sorted(os.listdir(ddd))
                if fls:
                    path2 = os.path.join(ddd, fls[-1])
                    spl = strip(path2).split(os.sep)[0]
                    if lst in spl.lower().split(".")[-1]:
                        yield strip(path2)


def hook(otp) -> Object:
    clz = fnclass(otp)
    cls = Class.get(clz)
    if cls:
        obj = cls()
        read(obj, otp)
        return obj
    raise NoClassError(clz)


def load(fpt, *args, **kw) -> Object:
    return json.load(fpt, *args, cls=ObjectDecoder, **kw)


def path(pth) -> str:
    return os.path.join(Persist.workdir, 'store', pth)


def read(obj, pth) -> None:
    pth = path(pth)
    with disklock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            data = load(ofile)
            update(obj, data)
    obj.__oid__ = strip(pth)
    return obj.__oid__


def setwd(pth) -> None:
    Persist.workdir = pth


def strip(pth) -> str:
    return os.sep.join(pth.split(os.sep)[-4:])


def touch(fname):
    fds = os.open(fname, os.O_WRONLY | os.O_CREAT)
    os.close(fds)


def write(obj) -> str:
    pth = path(obj.__oid__)
    cdir(pth)
    with disklock:
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)
    return strip(pth)


def find(mtc, selector=None) -> []:
    if selector is None:
        selector = {}
    for fnm in fns(mtc):
        obj = hook(fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        yield obj


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(kind(obj), selector),
                    key=lambda x: fntime(x.__oid__)
                   )
    if result:
        inp = result[-1]
        update(obj, inp)
        obj.__oid__ = inp.__oid__
    return obj.__oid__


def match(mtc, selector=None) -> []:
    if selector is None:
        selector = {}
    for tpe in Class.match(mtc):
        print(tpe)
        for fnm in fns(tpe):
            obj = hook(fnm)
            if '__deleted__' in obj:
                continue
            if selector and not search(obj, selector):
                continue
            yield obj


def fnclass(pth):
    try:
        *_rest, mpth = pth.split("store")
        splitted = mpth.split(os.sep)
        return splitted[0]
    except ValueError:
        pass
    return None


def fntime(daystr):
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    tme = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        tme += float('.' + rest)
    else:
        tme = 0
    return tme
