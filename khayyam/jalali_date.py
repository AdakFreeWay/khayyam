# -*- coding: utf-8 -*-
__author__ = 'vahid'

import datetime
import re
from khayyam.helpers import replace_if_match
from khayyam.algorithms import days_in_month, \
    is_leap_year, \
    get_julian_day_from_gregorian, \
    jalali_date_from_julian_day, \
    julian_day_from_jalali_date, \
    gregorian_date_from_julian_day, \
    parse
from khayyam.constants import MAXYEAR, \
    MINYEAR, \
    PERSIAN_MONTH_ABBRS, \
    PERSIAN_MONTH_NAMES, \
    PERSIAN_WEEKDAY_ABBRS, \
    PERSIAN_WEEKDAY_NAMES, \
    PERSIAN_MONTH_ABBRS_ASCII, \
    PERSIAN_MONTH_NAMES_ASCII, \
    PERSIAN_WEEKDAY_ABBRS_ASCII, \
    PERSIAN_WEEKDAY_NAMES_ASCII, \
    SATURDAY
from khayyam.formatting import FORMAT_DIRECTIVE_REGEX, FORMAT_DIRECTIVES


# TODO: replace(*) method for this class

class JalaliDate(object):
    """
    Representing the Jalali Date, without the time data.
    """

    def __init__(self, year=1, month=1, day=1):
        self.year, self.month, self.day = self._validate(year, month, day)


    ##################
    ### Properties ###
    ##################

    @property
    def is_leap(self):
        """
        Determines the year is leap or not.
        """
        return is_leap_year(self.year)

    @property
    def days_in_month(self):
        """
        Get total days in the current month.
        """
        return days_in_month(self.year, self.month)

    #####################
    ### Class Methods ###
    #####################

    @classmethod
    def from_julian_days(cls, julian_day):
        """
        Create JalaliDate from julian day
        """
        arr = jalali_date_from_julian_day(julian_day)
        return cls(arr[0], arr[1], arr[2])

    @classmethod
    def from_date(cls, d):
        """
        Create JalaliDate from python's datetime.date
        """
        julian_days = get_julian_day_from_gregorian(d.year, d.month, d.day)
        return cls.from_julian_days(julian_days)

    @classmethod
    def today(cls):
        """
        Return the current local date. 
        """
        return cls.from_date(datetime.date.today())

    @classmethod
    def fromtimestamp(cls, timestamp):
        """
        Return the local date corresponding to the POSIX timestamp. such as is returned by :func:`time.time()`. This may raise :class:`ValueError`, if the timestamp is out of the range of values supported by the platform C localtime() function. It’s common for this to be restricted to years from 1970 through 2038. Note that on non-POSIX systems that include leap seconds in their notion of a timestamp, leap seconds are ignored by fromtimestamp().
        """
        return cls.from_date(datetime.date.fromtimestamp(timestamp))

    @classmethod
    def fromordinal(cls, ordinal):
        """
        Return the datetime corresponding to the proleptic Shamsi ordinal, where Farvardin 1 of year 1 has ordinal 1. ValueError is raised unless 1 <= ordinal <= :func:`datetime.max.toordinal()`.
        """
        return cls.min + datetime.timedelta(days=ordinal-1)

    @classmethod
    def strptime(cls, date_string, fmt):
        """
        Return a datetime corresponding to date_string, parsed according to format. This is equivalent to datetime(*(time.strptime(date_string, format)[0:6])). ValueError is raised if the date_string and format can't be parsed by time.strptime() or if it returns a value which isn't a time tuple. See section strftime() and strptime() Behavior.
        '1387/4/12'
        '%Y/%m/%d'
        """
        regex = '^'
        index = 0
        for m in re.finditer(FORMAT_DIRECTIVE_REGEX, fmt):
            directive = m.group()
            if directive not in FORMAT_DIRECTIVES or directive == '%%':
                continue
            group_name = directive[1:]
            if index < m.start():
                regex += fmt[index:m.start()]
            regex += '(?P<%(group_name)s>%(regexp)s)' % dict(
                group_name=group_name,
                regexp=FORMAT_DIRECTIVES[directive][1]
            )
            index = m.end()
        regex += fmt[index:]

        regex += '$'
        # print(regex) # FIXME: remove this line
        m = re.match(regex, date_string)

        if not m:
            raise ValueError("time data '%s' does not match format '%s' with generated regex: '%s'" % (
                date_string, fmt, regex))

        result = {}
        for k, v in m.groupdict().items():
            directive_key = '%%%s' % k
            if directive_key not in FORMAT_DIRECTIVES:
                raise ValueError('directive key: %s was not exists.' % directive_key)
            directive = FORMAT_DIRECTIVES[directive_key]
            name = directive[0]
            validator = directive[3]
            if not validator:
                continue
            result[name] = validator(v)


        if 'dayofyear' in result:
            _dayofyear = result['dayofyear']
            if 'year' not in result:
                result['year'] = 1
            if 'month' in result:
                del result['month']
            if 'day' in result:
                del result['day']
            res = JalaliDate(result['year'])
            max_days = 366 if res.is_leap else 365
            if _dayofyear > max_days:
                raise ValueError(
                    'Invalid dayofyear: %.3d for year %.4d. Valid values are: 1-%s' \
                     % (_dayofyear, res.year, max_days))

            return res + datetime.timedelta(days=_dayofyear-1)
        else:
            return cls(**result)

    @staticmethod
    def _validate(year, month, day):
        year = year if isinstance(year, int) else int(year)
        month = month if isinstance(month, int) else int(month)
        day = day if isinstance(day, int) else int(day)

        if year < MINYEAR or year > MAXYEAR:
            raise ValueError('Year must be between %s and %s, but it is: %s' % (MINYEAR, MAXYEAR, year))
        if month < 1 or month > 12:
            raise ValueError('Month must be between 1 and 12, but it is: %s' % month)
        _days_in_month = days_in_month(year, month)
        if day < 1 or day > _days_in_month:
            raise ValueError('Day must be between 1 and %s, but it is: %s' % (_days_in_month, day))
        return year, month, day

    ########################
    ### Instance Methods ###
    ########################

    def tojulianday(self):
        return julian_day_from_jalali_date(self.year, self.month, self.day)

    def copy(self):
        return JalaliDate(self.year, self.month, self.day)

    def replace(self, year=None, month=None, day=None):
        year, month, day = self._validate(
            year if year else self.year,
            month if month else self.month,
            day if day else self.day)

        return JalaliDate(year, month, day)


    def todate(self):
        arr = gregorian_date_from_julian_day(self.tojulianday())
        return datetime.date(int(arr[0]), int(arr[1]), int(arr[2]))
    to_date = todate

    def toordinal(self):
        return (self - self.min).days + 1

    def timetuple(self):
        """
        The same as: :func:`datetime.date.timetuple()`.
        Return a :class:`time.struct_time` such as returned by :func:`time.localtime()`. The hours, minutes and seconds are 0, and the DST flag is -1. d.timetuple() is equivalent to `time.struct_time((d.year, d.month, d.day, 0, 0, 0, d.weekday(), yday, -1))`, where `yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1` is the day number within the current year starting with `1` for January 1st.
        """
        return self.todate().timetuple()

    def weekday(self):
        """
        Return the day of the week as an integer, where Saturday is 0 and Friday is 6.
        """
        return (self.todate().weekday() + 2) % 7

    def isoweekday(self):
        """
        Return the day of the week as an integer, where Saturday is 1 and Friday is 7.
        """
        return self.weekday() + 1

    def isocalendar(self):
        return self.year, self.weekofyear(SATURDAY), self.isoweekday()

    def isoformat(self):
        return '%s-%s-%s' % (self.year, self.month, self.day)

    def __str__(self):
        return self.isoformat()

    def __repr__(self):
        return 'khayyam.JalaliDate(%s, %s, %s)' % \
               (self.year, self.month, self.day)

    def strftime(self, fmt):
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
        result = ''
        index = 0
        for m in re.finditer(FORMAT_DIRECTIVE_REGEX, fmt):
            directive = m.group()
            if directive in FORMAT_DIRECTIVES:
                if index < m.start():
                    result += fmt[index:m.start()]
                result += FORMAT_DIRECTIVES[directive][2](self)
                index = m.end()
        result += fmt[index:]
        return result


    __format__ = strftime

    def weekdayname(self):
        return PERSIAN_WEEKDAY_NAMES[self.weekday()]

    def weekdayabbr(self):
        return PERSIAN_WEEKDAY_ABBRS[self.weekday()]

    def monthname(self):
        return PERSIAN_MONTH_NAMES[self.month]

    def monthabbr(self):
        return PERSIAN_MONTH_ABBRS[self.month]

    def weekdayname_ascii(self):
        return PERSIAN_WEEKDAY_NAMES_ASCII[self.weekday()]

    def weekdayabbr_ascii(self):
        return PERSIAN_WEEKDAY_ABBRS_ASCII[self.weekday()]

    def monthname_ascii(self):
        return PERSIAN_MONTH_NAMES_ASCII[self.month]

    def monthabbr_ascii(self):
        return PERSIAN_MONTH_ABBRS_ASCII[self.month]

    def localformat(self):
        return '%s %s %s %s' % (self.weekdayname(), self.day, self.monthname(), self.year)

    def firstdayofyear(self):
        return JalaliDate(self.year, 1, 1)

    def dayofyear(self):
        return (self - self.firstdayofyear()).days + 1

    def weekofyear(self, first_day_of_week=SATURDAY):
        first_day_of_year = self.firstdayofyear()
        days = (self - first_day_of_year).days
        offset = first_day_of_week - first_day_of_year.weekday()
        if offset < 0:
            offset += 7

        if days < offset:
            return 0

        return int((days - offset) / 7 + 1)

    #################
    ### Operators ###
    #################

    def __add__(self, x):
        if isinstance(x, datetime.timedelta):
            days = self.tojulianday() + x.days
            return JalaliDate.from_julian_days(days)

        raise ValueError('JalaliDate object can added by timedelta or JalaliDate object')

    def __sub__(self, x):
        if isinstance(x, datetime.timedelta):
            days = self.tojulianday() - x.days
            return JalaliDate.from_julian_days(days)
        elif isinstance(x, JalaliDate):
            days = self.tojulianday() - x.tojulianday()
            return datetime.timedelta(days=days)

        raise ValueError('JalaliDate object can added by timedelta or JalaliDate object')

    def __lt__(self, x):
        assert isinstance(x, JalaliDate), 'Comparison just allow with JalaliDate'
        return self.tojulianday() < x.tojulianday()

    def __le__(self, x):
        assert isinstance(x, JalaliDate), 'Comparison just allow with JalaliDate'
        return self.tojulianday() <= x.tojulianday()

    def __eq__(self, x):
        if not x:
            return False
        assert isinstance(x, JalaliDate), 'Comparison just allow with JalaliDate'
        return self.tojulianday() == x.tojulianday()

    def __ne__(self, x):
        assert isinstance(x, JalaliDate), 'Comparison just allow with JalaliDate'
        return self.tojulianday() != x.tojulianday()

    def __gt__(self, x):
        assert isinstance(x, JalaliDate), 'Comparison just allow with JalaliDate'
        return self.tojulianday() > x.tojulianday()

    def __ge__(self, x):
        assert isinstance(x, JalaliDate), 'Comparison just allow with JalaliDate'
        return self.tojulianday() >= x.tojulianday()


# Class attributes
JalaliDate.min = JalaliDate(MINYEAR, 1, 1)
JalaliDate.max = JalaliDate(MAXYEAR, 12, 29)
JalaliDate.resolution = datetime.timedelta(days=1)
