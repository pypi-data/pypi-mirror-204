# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@version    : v1.0
@author     : fangzheng
@contact    : fangzheng@rp-pet.cn
@software   : PyCharm
@filename   : Time.py
@create time: 2023/4/13 3:35 PM
@modify time: 2023/4/13 3:35 PM
@describe   : 
-------------------------------------------------
"""
from time import strftime, localtime
from datetime import datetime, timedelta


class Time:
    def __init__(self):
        self.time_format = "%Y-%m-%d %H:%M:%S"

    def curr_time(self, time_format=None):
        if time_format:
            return strftime(time_format, localtime())
        else:
            return strftime(self.time_format, localtime())

    def curr_time_by_number(self):
        return self.curr_time("%Y%m%d%H%M%S")

    def _today(self):
        return datetime.today()

    def today(self):
        return self._today().strftime("%Y-%m-%d")

    def yesterday(self):
        yesterday = self._today() - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
