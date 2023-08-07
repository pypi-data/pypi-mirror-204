# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E0402,W0120


'errors'


import io
import traceback


from ..handler import Error


def err(event):
    for ex in Error.errors:
        stream = io.StringIO(traceback.print_exception(type(ex), ex, ex.__traceback__))
        for line in stream.readlines():
            event.reply(line)
    else:
        event.reply("no error")
