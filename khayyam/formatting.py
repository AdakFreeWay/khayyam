# -*- coding: utf-8 -*-
import re
from khayyam.constants import SATURDAY
__author__ = 'vahid'


class JalaliDateFormatter(object):
    """
    =========    =======
    Directive    Meaning
    =========    =======
    %a           Locale’s abbreviated weekday name.
    %A           Locale’s full weekday name.
    %b           Locale’s abbreviated month name.
    %B           Locale’s full month name.
    %d           Day of the month as a decimal number [01,31].
    %j           Day of the year as a decimal number [001,366].
    %m           Month as a decimal number [01,12].
    %w           Weekday as a decimal number [0(Saturday),6(Friday)].
    %W           Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.
    %x           Locale’s appropriate date representation.
    %y           Year without century as a decimal number [00,99].
    %Y           Year with century as a decimal number.
    %e           ASCII Locale’s abbreviated weekday name.
    %E           ASCII Locale’s full weekday name.
    %g           ASCII Locale’s abbreviated month name.
    %G           ASCII Locale’s full month name.
    %%           A literal '%' character.
    =========    =======
    """

    # TODO: _first_day_of_week = SATURDAY
    _directive_regex = '%[a-zA-Z%]'
    _directives = {
        '%a': ('weekdayabbr',       '', lambda d: d.weekdayabbr(), None),
        '%A': ('weekdayname',       '', lambda d: d.weekdayname(), None),
        '%b': ('monthabbr',         '', lambda d: d.monthabbr(), None),
        '%B': ('monthname',         '', lambda d: d.monthname(), None),
        '%j': ('dayofyear',         '', lambda d: '%.3d' % d.dayofyear(), None),
        '%w': ('weekday',           '', lambda d: '%d' % d.weekday(), None),
        '%W': ('weekofyear',        '', lambda d: '%.2d' % d.weekofyear(SATURDAY), None),
        '%x': ('localformat',       '', lambda d: d.localformat(), None),
        '%y': ('short_year',        '\d{2}', lambda d: '%.2d' % (d.year % 100), lambda v: int(v)),
        '%Y': ('year',              '\d{4}', lambda d: '%.4d' % d.year, lambda v: int(v)),
        '%e': ('weekdayabbr_ascii', '', lambda d: d.weekdayabbr_ascii(), None),
        '%E': ('weekdayname_ascii', '', lambda d: d.weekdayname_ascii(), None),
        '%g': ('monthabbr_ascii',   '', lambda d: d.monthabbr_ascii(), None),
        '%G': ('monthname_ascii',   '', lambda d: d.monthname_ascii(), None),
        '%m': ('month',             '', lambda d: '%.2d' % d.month, None),
        '%d': ('day',               '', lambda d: '%.2d' % d.day, None),
        '%%': ('percent',           '', lambda d: '%', None),
    }

    def __init__(self, format):
        self._format = format

    def update_format(self, format):
        self._format = format

    def get_string(self, jalali_date):
        return self.format(jalali_date, self._format)

    def get_jalali_date(self, date_string):
        return self.parse(date_string, self._format)

    @classmethod
    def format(cls, jalali_date, fmt):
        result = ''
        index = 0
        for m in re.finditer(cls._directive_regex, fmt):
            directive = m.group()
            if directive in cls._directives:
                if index < m.start():
                    result += fmt[index:m.start()]
                result += cls._directives[directive][2](jalali_date)
                index = m.end()
        return result

    @classmethod
    def parse(cls, date_string, fmt, factory=dict):
        regex = '^'
        index = 0
        for m in re.finditer(cls._directive_regex, fmt):
            directive = m.group()
            group_name = directive[1:]
            if index < m.start():
                regex += fmt[index:m.start()]
            regex += '(?P<%(group_name)s>%(regexp)s)' % dict(
                group_name=group_name,
                regexp=cls._directives[directive][1]
            )
            index = m.end()
        regex += fmt[index:]

        regex += '$'
        print(regex) # FIXME: remove this line
        m = re.match(regex, date_string)
        if not m:
            raise ValueError("time data '%s' does not match format '%s' with generated regex: '%s'" % (
                date_string, fmt, regex))

        result = {}
        for k, v in m.groupdict().items():
            directive_key = '%%%s' % k
            if directive_key not in cls._directives:
                raise ValueError('directive key: %s was not exists' % directive_key)
            directive = cls._directives[directive_key]
            name = directive[0]
            validator = directive[3]
            if not validator:
                continue
            result[name] = validator(v)

        return factory(**result)




