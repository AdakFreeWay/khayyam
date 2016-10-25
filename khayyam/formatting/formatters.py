# -*- coding: utf-8 -*-
import re

import khayyam
from khayyam.compat import get_unicode
from khayyam.constants import SATURDAY, MONDAY
from khayyam.formatting import constants as consts
from khayyam.formatting.directives import Directive, DayOfYearDirective, persian, PersianDayOfYearDirective

__author__ = 'vahid'


class Formattable(object):
    pass


class BaseFormatter(object):
    _directives = []

    def __init__(self):
        self._directives_by_key = {}
        self._post_parsers = []
        for d in self._directives:
            self._directives_by_key[d.key] = d
            if d.require_post_parsing:
                self._post_parsers.append(d)

    def _create_parser_regex(self, format_string):
        regex = u'^'
        index = 0
        for m in re.finditer(consts.FORMAT_DIRECTIVE_REGEX, format_string):
            directive_key = m.group()[1:]
            if directive_key not in self._directives_by_key:
                continue
            directive = self._directives_by_key[directive_key]
            if index < m.start():
                regex += format_string[index:m.start()]
            index = m.end()
            if directive.key == u'%':
                regex += u'%'
                continue
            regex += u'(?P<%(group_name)s>%(regexp)s)' % dict(
                group_name=directive.key,
                regexp=directive.regex
            )
        regex += format_string[index:]
        regex += u'$'
        return regex

    def iter_format_directives(self, format_string):
        for m in re.finditer(consts.FORMAT_DIRECTIVE_REGEX, format_string):
            key = m.group()[1:]
            if key in self._directives_by_key:
                yield m, self._directives_by_key[key]

    def format(self, format_string, formattable):
        assert isinstance(formattable, Formattable)
        result = ''
        index = 0
        for match, directive in self.iter_format_directives(format_string):
            if index < match.start():
                result += format_string[index:match.start()]
            result += directive.format(formattable)
            index = match.end()
        result += format_string[index:]
        return result

    @staticmethod
    def filter_persian_digit(s):
        # FIXME: Rename it to normalize_digits
        # FIXME: A better algorithm is needed.
        for p, e in consts.PERSIAN_DIGIT_MAPPING:
            s = s.replace(p[1], p[0])
        return s

    def _parse(self, format_string, date_string):
        parser_regex = self._create_parser_regex(format_string)

        m = re.match(parser_regex, self.filter_persian_digit(date_string))
        if not m:
            raise ValueError(u"time data '%s' does not match format '%s' with generated regex: '%s'" % (
                date_string, format_string, parser_regex))
        result = {}
        for directive_key, v in m.groupdict().items():
            directive = self._directives_by_key[directive_key]
            result[directive.target_name] = directive.coerce_type(v)
        return result

    def _parse_post_processor(self, parse_result):
        for directive in self._post_parsers:
            if directive.target_name in parse_result.keys():
                directive.post_parser(parse_result, self)

    def parse(self, format_string, date_string):
        result = self._parse(format_string, date_string)
        self._parse_post_processor(result)
        return result


class JalaliDateFormatter(BaseFormatter):
    """
    Responsible to parse and formatting of a :py:class:`khayyam.JalaliDate` instance.

    """

    _directives = [

        # YEAR

        Directive(
            'Y',
            consts.YEAR_REGEX,
            name='year',
            type_=int,
            formatter=lambda d: '%.4d' % d.year
        ),
        Directive(
            'y',
            consts.SHORT_YEAR_REGEX,
            type_=int,
            formatter=lambda d: '%.2d' % (d.year % 100),
            post_parser=lambda ctx, f: ctx.update(year=int(khayyam.JalaliDate.today().year / 100) * 100 + ctx['y'])
        ),
        Directive(
            'n',
            consts.PERSIAN_SHORT_YEAR_REGEX,
            type_=int,
            formatter=lambda d: persian('%d' % (d.year % 100)),
            post_parser=lambda ctx, f: ctx.update(year=int(khayyam.JalaliDate.today().year / 100) * 100 + ctx['n'])
        ),
        Directive(
            'u',
            consts.PERSIAN_SHORT_YEAR_ZERO_PADDED_REGEX,
            type_=int,
            formatter=lambda d: persian('%.2d' % (d.year % 100)),
            post_parser=lambda ctx, f: ctx.update(year=int(khayyam.JalaliDate.today().year / 100) * 100 + ctx['u'])
        ),
        Directive(
            'N',
            consts.PERSIAN_YEAR_REGEX,
            type_=int,
            formatter=lambda d: persian('%d' % d.year),
            post_parser=lambda ctx, f: ctx.update(year=int(ctx['N']))
        ),
        Directive(
            'O',
            consts.PERSIAN_YEAR_ZERO_PADDED_REGEX,
            type_=int,
            formatter=lambda d: persian('%.4d' % d.year),
            post_parser=lambda ctx, f: ctx.update(year=int(ctx['O']))
        ),

        # MONTH
        Directive(
            'm',
            consts.MONTH_REGEX,
            name='month',
            type_=int,
            formatter=lambda d: '%.2d' % d.month,
        ),
        Directive(
            'R',
            consts.PERSIAN_MONTH_REGEX,
            type_=int,
            formatter=lambda d: persian(d.month),
            post_parser=lambda ctx, f: ctx.update(month=int(ctx['R']))
        ),
        Directive(
            'P',
            consts.PERSIAN_MONTH_ZERO_PADDED_REGEX,
            type_=int,
            formatter=lambda d: persian('%.2d' % d.month),
            post_parser=lambda ctx, f: ctx.update(month=int(ctx['P']))
        ),
        Directive(
            'b',
            consts.PERSIAN_MONTH_ABBRS_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.monthabbr(),
            post_parser=lambda ctx, f: ctx.update(
                month=next(k for k, v in consts.PERSIAN_MONTH_ABBRS.items() if v == ctx['b'])
            )
        ),
        Directive(
            'B',
            consts.PERSIAN_MONTH_NAMES_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.monthname(),
            post_parser=lambda ctx, f: ctx.update(
                month=next(k for k, v in consts.PERSIAN_MONTH_NAMES.items() if v == ctx['B'])
            )
        ),
        Directive(
            'g',
            consts.PERSIAN_MONTH_ABBRS_ASCII_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.monthabbr_ascii(),
            post_parser=lambda ctx, f: ctx.update(
                month=next(k for k, v in consts.PERSIAN_MONTH_ABBRS_ASCII.items() if v == ctx['g'])
            )
        ),
        Directive(
            'G',
            consts.PERSIAN_MONTH_NAMES_ASCII_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.monthnameascii(),
            post_parser=lambda ctx, f: ctx.update(
                month=next(k for k, v in consts.PERSIAN_MONTH_NAMES_ASCII.items() if v == ctx['G'])
            )
        ),

        # WEEK
        Directive(
            'a',
            consts.PERSIAN_WEEKDAY_ABBRS_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.weekdayabbr()
        ),
        Directive(
            'A',
            consts.PERSIAN_WEEKDAY_NAMES_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.weekdayname()
        ),
        Directive(
            'e',
            consts.PERSIAN_WEEKDAY_ABBRS_ASCII_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.weekdayabbrascii(),
        ),
        Directive(
            'E',
            consts.PERSIAN_WEEKDAY_NAMES_ASCII_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.weekdaynameascii(),
        ),
        Directive(
            'T',
            consts.ENGLISH_WEEKDAY_NAMES_ASCII_REGEX,
            type_=get_unicode,
            formatter=lambda d: d.englishweekdaynameascii(),
        ),
        Directive(
            'w',
            consts.WEEKDAY_REGEX,
            type_=int,
            formatter=lambda d: '%d' % d.weekday(),
        ),
        Directive(
            'W',
            consts.WEEK_OF_YEAR_REGEX,
            type_=int,
            formatter=lambda d: '%.2d' % d.weekofyear(SATURDAY),
        ),
        Directive(
            'U',
            consts.WEEK_OF_YEAR_REGEX,
            type_=int,
            formatter=lambda d: '%.2d' % d.weekofyear(MONDAY),
        ),

        # DAY
        Directive(
            'd',
            consts.DAY_REGEX,
            name='day',
            type_=int,
            formatter=lambda d: '%.2d' % d.day
        ),
        Directive(
            'D',
            consts.PERSIAN_DAY_REGEX,
            type_=int,
            formatter=lambda d: persian(d.day),
            post_parser=lambda ctx, f: ctx.update(day=int(ctx['D']))
        ),
        Directive(
            'K',
            consts.PERSIAN_DAY_ZERO_PADDED_REGEX,
            type_=int,
            formatter=lambda d: persian('%.2d' % d.day),
            post_parser=lambda ctx, f: ctx.update(day=int(ctx['K']))
        ),
        DayOfYearDirective('j'),
        PersianDayOfYearDirective('J'),
        PersianDayOfYearDirective('V', regex=consts.PERSIAN_DAY_OF_YEAR_ZERO_PADDED_REGEX, zero_padded=True)
    ]

    """



    PersianDayOfYearDirective('V', 'persiandayofyearzeropadded', consts.PERSIAN_DAY_OF_YEAR_ZERO_PADDED_REGEX,
                              zero_padding=True, zero_padding_length=3),
    """

    # _post_parsers = [
    #     'persianday',
    #     'persiandayzeropadded',
    #     'persiandayofyear',
    #     'persiandayofyearzeropadded',
    #     'persianmonth',
    #     'persianmonthzeropadded',
    #     'persianyear',
    #     'persianyearzeropadded',
    #     'persianshortyear',
    #     'persianshortyearzeropadded',
    #     'localdateformat',
    #     'monthabbr',
    #     'monthabbr_ascii',
    #     'monthname',
    #     'monthnameascii',
    #     'shortyear',
    #     'dayofyear',
    # ]


class JalaliDatetimeFormatter(JalaliDateFormatter):
    """
    Responsible to parse and formatting of a :py:class:`khayyam.JalaliDatetime` instance.

    """
    _directives = []

    # _post_parsers = [
    #     'persianday',
    #     'persiandayzeropadded',
    #     'persiandayofyear',
    #     'persiandayofyearzeropadded',
    #     'persianmonth',
    #     'persianmonthzeropadded',
    #     'persianyear',
    #     'persianyearzeropadded',
    #     'persianshortyear',
    #     'persianshortyearzeropadded',
    #     'persianmicrosecond',
    #     'persianhour12',
    #     'persianhour12zeropadded',
    #     'persianhour24',
    #     'persianhour24zeropadded',
    #     'persianminute',
    #     'persianminutezeropadded',
    #     'persiansecond',
    #     'persiansecondzeropadded',
    #     'persianutcoffset',
    #     'localdateformat',
    #     'localshortdatetimeformat',
    #     'localshortdatetimeformatascii',
    #     'localdatetimeformat',
    #     'localdatetimeformatascii',
    #     'localtimeformat',
    #     'monthabbr',
    #     'monthabbr_ascii',
    #     'monthname',
    #     'monthnameascii',
    #     'ampm',
    #     'ampmascii',
    #     'shortyear',
    #     'dayofyear',
    #     'utcoffset'
    # ]


class JalaliTimedeltaFormatter(JalaliDateFormatter):
    """
    Responsible to parse and formatting of a :py:class:`khayyam.JalaliTimedelta` instance.

    """
    _directives = []

    # _post_parsers = [
    #
    #     'totalhours',
    #     'persiantotalhours',
    #     'totalminutes',
    #
    # ]
