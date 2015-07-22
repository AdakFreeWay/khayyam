# -*- coding: utf-8 -*-
import re
from .directive import Directive
from khayyam.formatting import constants as consts
from khayyam.compat import get_unicode
__author__ = 'vahid'

class LocalDateFormatDirective(Directive):
    def __init__(self):
        super(LocalDateFormatDirective, self).__init__(
            'x', 'localdateformat', consts.LOCAL_DATE_FORMAT_REGEX, get_unicode)

    def format(self, d):
        return d.localdateformat()

    def post_parser(self, ctx, formatter):
        regex = ' '.join([
            '(?P<weekdayname>%s)' % consts.PERSIAN_WEEKDAY_NAMES_REGEX,
            '(?P<day>%s)' % consts.DAY_REGEX,
            '(?P<monthname>%s)' % consts.PERSIAN_MONTH_NAMES_REGEX,
            '(?P<year>%s)' % consts.YEAR_REGEX
        ])

        match = re.match(regex, ctx['localdateformat'])
        d = match.groupdict()
        ctx.update(dict(
            weekdayname = formatter.directives_by_key['A'].type_(d['weekdayname']),
            day = formatter.directives_by_key['d'].type_(d['day']),
            monthname = formatter.directives_by_key['B'].type_(d['monthname']),
            year = formatter.directives_by_key['Y'].type_(d['year'])
        ))


class LocalShortDatetimeFormatDirective(Directive):
    def __init__(self):
        super(LocalShortDatetimeFormatDirective, self).__init__(
            'c', 'localshortdatetimeformat', consts.LOCAL_SHORT_DATE_TIME_FORMAT_REGEX, get_unicode)

    def format(self, d):
        return d.localshortformat()

    def post_parser(self, ctx, formatter):
        regex = ' '.join([
            '(?P<weekdayabbr>%s)' % consts.PERSIAN_WEEKDAY_ABBRS_REGEX,
            '(?P<day>%s)' % consts.DAY_REGEX,
            '(?P<monthabbr>%s)' % consts.PERSIAN_MONTH_ABBRS_REGEX,
            '(?P<shortyear>%s)' % consts.SHORT_YEAR_REGEX,
            '(?P<hour>%s):(?P<minute>%s)' % (consts.HOUR24_REGEX, consts.MINUTE_REGEX),
        ])

        match = re.match(regex, ctx[self.name])
        d = match.groupdict()
        ctx.update(dict(
            weekdayabbr = formatter.directives_by_key['a'].type_(d['weekdayabbr']),
            day = formatter.directives_by_key['d'].type_(d['day']),
            monthabbr = formatter.directives_by_key['b'].type_(d['monthabbr']),
            shortyear = formatter.directives_by_key['y'].type_(d['shortyear']),
            hour = formatter.directives_by_key['H'].type_(d['hour']),
            minute = formatter.directives_by_key['M'].type_(d['minute'])
        ))


class LocalASCIIShortDatetimeFormatDirective(Directive):
    def __init__(self):
        super(LocalASCIIShortDatetimeFormatDirective, self).__init__(
            'q', 'localshortdatetimeformatascii', consts.LOCAL_SHORT_DATE_TIME_FORMAT_ASCII_REGEX, get_unicode)

    def format(self, d):
        return d.localshortformatascii()

    def post_parser(self, ctx, formatter):
        """
        %e %d %g %y %H:%M
        """
        regex = ' '.join([
            '(?P<weekdayabbr>%s)' % consts.PERSIAN_WEEKDAY_ABBRS_ASCII_REGEX,
            '(?P<day>%s)' % consts.DAY_REGEX,
            '(?P<monthabbr>%s)' % consts.PERSIAN_MONTH_ABBRS_ASCII_REGEX,
            '(?P<shortyear>%s)' % consts.SHORT_YEAR_REGEX,
            '(?P<hour>%s):(?P<minute>%s)' % (consts.HOUR24_REGEX, consts.MINUTE_REGEX),
        ])

        match = re.match(regex, ctx[self.name])
        d = match.groupdict()
        ctx.update(dict(
            weekdayabbr_ascii = formatter.directives_by_key['e'].type_(d['weekdayabbr']),
            day = formatter.directives_by_key['d'].type_(d['day']),
            monthabbr_ascii = formatter.directives_by_key['g'].type_(d['monthabbr']),
            shortyear = formatter.directives_by_key['y'].type_(d['shortyear']),
            hour = formatter.directives_by_key['H'].type_(d['hour']),
            minute = formatter.directives_by_key['M'].type_(d['minute'])
        ))




class LocalDatetimeFormatDirective(Directive):
    def __init__(self):
        super(LocalDatetimeFormatDirective, self).__init__(
            'C', 'localdatetimeformat', consts.LOCAL_DATE_TIME_FORMAT_REGEX, get_unicode)

    def format(self, d):
        return d.localdatetimeformat()

    def post_parser(self, ctx, formatter):
        """
        %A %d %B %Y %I:%M:%S %p
        """
        regex = ' '.join([
            '(?P<weekdayname>%s)' % consts.PERSIAN_WEEKDAY_NAMES_REGEX,
            '(?P<day>%s)' % consts.DAY_REGEX,
            '(?P<monthname>%s)' % consts.PERSIAN_MONTH_NAMES_REGEX,
            '(?P<year>%s)' % consts.YEAR_REGEX,
            '(?P<hour12>%s):(?P<minute>%s):(?P<second>%s)' % (
                consts.HOUR12_REGEX, consts.MINUTE_REGEX, consts.SECOND_REGEX),
            '(?P<ampm>%s)' % consts.AM_PM_REGEX
        ])

        match = re.match(regex, ctx[self.name])
        d = match.groupdict()
        ctx.update(dict(
            weekdayname = formatter.directives_by_key['A'].type_(d['weekdayname']),
            day = formatter.directives_by_key['d'].type_(d['day']),
            monthname = formatter.directives_by_key['B'].type_(d['monthname']),
            year = formatter.directives_by_key['Y'].type_(d['year']),
            hour12 = formatter.directives_by_key['I'].type_(d['hour12']),
            minute = formatter.directives_by_key['M'].type_(d['minute']),
            second = formatter.directives_by_key['S'].type_(d['second']),
            ampm = formatter.directives_by_key['p'].type_(d['ampm']),
        ))


class LocalASCIIDatetimeFormatDirective(Directive):
    def __init__(self):
        super(LocalASCIIDatetimeFormatDirective, self).__init__(
            'Q', 'localdatetimeformatascii', consts.LOCAL_DATE_TIME_FORMAT_ASCII_REGEX, get_unicode)

    def format(self, d):
        return d.localdatetimeformatascii()

    def post_parser(self, ctx, formatter):
        """
        %E %d %G %Y %I:%M:%S %t
        """
        regex = ' '.join([
            '(?P<weekdayname>%s)' % consts.PERSIAN_WEEKDAY_NAMES_ASCII_REGEX,
            '(?P<day>%s)' % consts.DAY_REGEX,
            '(?P<monthname>%s)' % consts.PERSIAN_MONTH_NAMES_ASCII_REGEX,
            '(?P<year>%s)' % consts.YEAR_REGEX,
            '(?P<hour12>%s):(?P<minute>%s):(?P<second>%s)' % (
                consts.HOUR12_REGEX, consts.MINUTE_REGEX, consts.SECOND_REGEX),
            '(?P<ampm>%s)' % consts.AM_PM_ASCII_REGEX
        ])

        match = re.match(regex, ctx[self.name])
        d = match.groupdict()

        ctx.update(dict(
            weekdayname_ascii = formatter.directives_by_key['E'].type_(d['weekdayname']),
            day = formatter.directives_by_key['d'].type_(d['day']),
            monthname_ascii = formatter.directives_by_key['G'].type_(d['monthname']),
            year = formatter.directives_by_key['Y'].type_(d['year']),
            hour12 = formatter.directives_by_key['I'].type_(d['hour12']),
            minute = formatter.directives_by_key['M'].type_(d['minute']),
            second = formatter.directives_by_key['S'].type_(d['second']),
            ampmascii = formatter.directives_by_key['t'].type_(d['ampm']),
        ))


class LocalTimeFormatDirective(Directive):
    def __init__(self):
        super(LocalTimeFormatDirective, self).__init__(
            'X', 'localtimeformat', consts.LOCAL_TIME_FORMAT_REGEX, get_unicode)

    def format(self, d):
        return d.localtimeformat()

    def post_parser(self, ctx, formatter):
        """
        '%I:%M:%S %p'
        """
        regex = ' '.join([
            '(?P<hour12>%s):(?P<minute>%s):(?P<second>%s)' % (
                consts.HOUR12_REGEX, consts.MINUTE_REGEX, consts.SECOND_REGEX),
            '(?P<ampm>%s)' % consts.AM_PM_REGEX
        ])

        match = re.match(regex, ctx[self.name])
        d = match.groupdict()
        ctx.update(dict(
            hour12 = formatter.directives_by_key['I'].type_(d['hour12']),
            minute = formatter.directives_by_key['M'].type_(d['minute']),
            second = formatter.directives_by_key['S'].type_(d['second']),
            ampm = formatter.directives_by_key['p'].type_(d['ampm']),
        ))

