# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0902,R0903,W0613,E1101,R0912,R0904,R0915,E0402


'users'


import time


from ..clocked import elapsed
from ..objects import Object, update
from ..persist import Class, find, fntime, write


def __dir__():
    return (
            'NoUser',
            'Users',
            'User',
            'dlt',
            'met'
           )


class NoUser(Exception):

    "user not found"


class Users(Object):

    @staticmethod
    def allowed(origin, perm):
        perm = perm.upper()
        user = Users.get_user(origin)
        val = False
        if user and perm in user.perms:
            val = True
        return val

    @staticmethod
    def delete(origin, perm):
        res = False
        for user in Users.get_users(origin):
            try:
                user.perms.remove(perm)
                write(user)
                res = True
            except ValueError:
                pass
        return res

    @staticmethod
    def get_users(origin=''):
        selector = {'user': origin}
        return find('user', selector)

    @staticmethod
    def get_user(origin):
        users = list(Users.get_users(origin))
        res = None
        if len(users) > 0:
            res = users[-1]
        return res

    @staticmethod
    def perm(origin, permission):
        user = Users.get_user(origin)
        if not user:
            raise NoUser(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            write(user)
        return user


class User(Object):

    def __init__(self, val=None):
        Object.__init__(self)
        self.user = ''
        self.perms = []
        if val:
            update(self, val)


Class.add(User)


def dlt(event):
    if not event.args:
        event.reply('dlt <username>')
        return
    selector = {'user': event.args[0]}
    for obj in find('user', selector):
        obj.__deleted__ = True
        write(obj)
        event.reply('ok')
        break


def met(event):
    if not event.args:
        nmr = 0
        for obj in find('user'):
            event.reply('%s %s %s %s' % (
                                         nmr,
                                         obj.user,
                                         obj.perms,
                                         elapsed(time.time() - fntime(obj.__fnm__)))
                                        )
            nmr += 1
        if not nmr:
            event.reply('no user')
        return
    user = User()
    user.user = event.rest
    user.perms = ['USER']
    write(user)
    event.reply('ok')
