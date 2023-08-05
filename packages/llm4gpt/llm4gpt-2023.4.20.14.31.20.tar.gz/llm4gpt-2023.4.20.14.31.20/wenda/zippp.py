#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : zippp
# @Time         : 2023/4/12 16:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from meutils.pipe import *
from meutils.path_utils import zipfiles

filename = Path('.').resolve().name
out_file = f'../{filename}.zip'
zipfiles(Path('.').rglob('*'), out_file=out_file)
