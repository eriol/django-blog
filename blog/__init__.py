# -*- coding: utf-8 -*-
VERSION = (0, 0, 6)

def get_version():
    """Returns project version in a human readable form."""
    version = '.'.join(str(v) for v in VERSION[:3])
    sub = ''.join(str(v) for v in VERSION[3:])
    return version + sub
