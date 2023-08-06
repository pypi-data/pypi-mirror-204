# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:21
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's personal tool set.
"""


from typing import Final

from .rbasic import warn
from .rcompress import rzip
from .rcommon import exc, digits, randn, sleep, get_paths, n2ch
from .rdata import count, flatten, split, unique
from .rdatabase import REngine
from .rdatetime import RDateTimeMark, now, time2str, str2time
from .remail import REmail
from .rimage import encode_qrcode, decode_qrcode
from .rmultitask import threads
from . import roption
from .rregular import res_search, res_sub
from .rrequest import request, download
from .rtext import rprint
from .rwrap import runtime


__version__: Final[str] = "0.110"