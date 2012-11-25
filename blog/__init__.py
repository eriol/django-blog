# -*- coding: utf-8 -*-
VERSION = (0, 0, 4)

def get_version():
    """Returns project version in a human readable form."""
    return '.'.join(str(v) for v in VERSION)
