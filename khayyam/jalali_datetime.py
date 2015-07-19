# -*- coding: utf-8 -*-
from datetime import timedelta, time, datetime
from khayyam.algorithms import get_julian_day_from_gregorian, \
    jalali_date_from_julian_day, \
    gregorian_date_from_julian_day
from khayyam.constants import MINYEAR, MAXYEAR, AM_PM, AM_PM_ASCII
from khayyam import JalaliDate
from khayyam.formatting import JalaliDatetimeFormatter
__author__ = 'vahid'


class JalaliDatetime(JalaliDate):
    def __init__(self, year=1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        if isinstance(year, JalaliDate):
            jd = year
            year = jd.year
            month = jd.month
            day = jd.day

        JalaliDate.__init__(self, year, month, day)
        self._time = time(hour, minute, second, microsecond, tzinfo)

    # #################
    ### Properties ###
    ##################

    def get_hour(self):
        return self._time.hour

    def set_hour(self, val):
        self._time.hour = val

    hour = property(get_hour, set_hour)

    def get_minute(self):
        return self._time.minute

    def set_minute(self, val):
        self._time.minute = val

    minute = property(get_minute, set_minute)

    def get_second(self):
        return self._time.second

    def set_second(self, val):
        self._time.second = val

    second = property(get_second, set_second)

    def get_microsecond(self):
        return self._time.microsecond

    def set_microsecond(self, val):
        self._time.microsecond = val

    microsecond = property(get_microsecond, set_microsecond)

    def get_tzinfo(self):
        return self._time.tzinfo

    def set_tzinfo(self, val):
        self._time.tzinfo = val

    tzinfo = property(get_tzinfo, set_tzinfo)

    ######################
    ### Static Methods ###
    ######################

    @staticmethod
    def create_formatter(fmt):
        return JalaliDatetimeFormatter(fmt)

    #####################
    ### Class Methods ###
    #####################

    @classmethod
    def from_datetime(cls, dt, tz=None):
        julian_days = get_julian_day_from_gregorian(dt.year, dt.month, dt.day)
        arr = jalali_date_from_julian_day(julian_days)
        if not tz:
            tz = dt.tzinfo
        return cls(arr[0], arr[1], arr[2], dt.hour, dt.minute, dt.second, dt.microsecond, tz)

    @classmethod
    def now(cls, tz=None):
        """
        Return the current local date and _time. If optional argument tz is None or not specified, this is like today(), but, if possible, supplies more precision than can be gotten from going through a _time._time() timestamp (for example, this may be possible on platforms supplying the C gettimeofday() function).
        
        Else tz must be an instance of a class tzinfo subclass, and the current date and _time are converted to tz's _time zone. In this case the result is equivalent to tz.fromutc(datetime.utcnow().replace(tzinfo=tz)). See also today(), utcnow().
        """
        return cls.from_datetime(datetime.now(tz))

    @classmethod
    def utcnow(cls):
        """
        Return the current UTC date and _time, with tzinfo None. This is like now(), but returns the current UTC date and _time, as a naive datetime object. See also now().
        """
        return cls.from_datetime(datetime.utcnow())

    @classmethod
    def dstnow(cls, tz):
        now = cls.now(tz=tz)
        return now + now.dst()

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        """
        Return the local date and _time corresponding to the POSIX timestamp, such as is returned by _time._time(). If optional argument tz is None or not specified, the timestamp is converted to the platform's local date and _time, and the returned datetime object is naive.
        
        Else tz must be an instance of a class tzinfo subclass, and the timestamp is converted to tz's _time zone. In this case the result is equivalent to tz.fromutc(datetime.utcfromtimestamp(timestamp).replace(tzinfo=tz)).
        
        fromtimestamp() may raise ValueError, if the timestamp is out of the range of values supported by the platform C localtime() or gmtime() functions. It's common for this to be restricted to years in 1970 through 2038. Note that on non-POSIX systems that include leap seconds in their notion of a timestamp, leap seconds are ignored by fromtimestamp(), and then it's possible to have two timestamps differing by a second that yield identical datetime objects. See also utcfromtimestamp().
        """
        return cls.from_datetime(datetime.fromtimestamp(timestamp, tz=tz))

    @classmethod
    def utcfromtimestamp(cls, timestamp):
        """
        Return the UTC datetime corresponding to the POSIX timestamp, with tzinfo None. This may raise ValueError, if the timestamp is out of the range of values supported by the platform C gmtime() function. It's common for this to be restricted to years in 1970 through 2038. See also fromtimestamp().
        """
        return cls.from_datetime(datetime.utcfromtimestamp(timestamp))

    @classmethod
    def fromordinal(cls, ordinal):
        """
        Return the jalali datetime corresponding to the proleptic Gregorian ordinal, where January 1 of year 1 has ordinal 1. ValueError is raised unless 1 <= ordinal <= datetime.max.toordinal(). The hour, minute, second and microsecond of the result are all 0, and tzinfo is None.
        """
        return cls.from_datetime(datetime.fromordinal(ordinal))

    @classmethod
    def combine(cls, date, _time):
        """
        Return a new jalali datetime object whose date members are equal to the given date object's, and whose _time and tzinfo members are equal to the given _time object's. For any datetime object d, d == datetime.combine(d.date(), d.timetz()). If date is a datetime object, its _time and tzinfo members are ignored.
        """
        if isinstance(date, (JalaliDatetime, JalaliDate)):
            date = date.to_datetime()
        return cls.from_datetime(datetime.combine(date, _time))

    @classmethod
    def strptime(cls, date_string, fmt):
        result = cls.create_formatter(fmt).parse(date_string)
        result = {k:v for k, v in result.items() if k in (
            'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond', 'tzinfo')}
        return cls(**result)


    # @classmethod
    # def strptime(cls, date_string, frmt):
    #     """
    #     Return a datetime corresponding to date_string, parsed according to format. This is equivalent to datetime(*(_time.strptime(date_string, format)[0:6])). ValueError is raised if the date_string and format can't be parsed by _time.strptime() or if it returns a value which isn't a _time tuple. See section strftime() and strptime() Behavior.
    #     '1387/4/12'
    #     '%Y/%m/%d'
    #     """
    #     # TODO: Implement full features of python, see: http://docs.python.org/library/datetime.html
    #     valid_codes = {'%Y': (4, 'year'),
    #                    '%m': (2, 'month'),
    #                    '%d': (2, 'day'),
    #                    '%H': (2, 'hour'),
    #                    '%M': (2, 'minute'),
    #                    '%S': (2, 'second'),
    #                    '%f': (6, 'microsecond')
    #                    }
    #
    #     return parse(cls, date_string, frmt, valid_codes)

    ########################
    ### Instance Methods ###
    ########################


    def to_datetime(self):
        arr = gregorian_date_from_julian_day(self.tojulianday())
        return datetime(int(arr[0]), int(arr[1]), int(arr[2]), self.hour, self.minute, self.second, self.microsecond,
                        self.tzinfo)

    def date(self):
        return JalaliDate(self.year, self.month, self.day)

    def time(self):
        return time(self.hour, self.minute, self.second, self.microsecond)

    def timetz(self):
        return time(self.hour, self.minute, self.second, self.microsecond, self.tzinfo)

    def replace(self, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=None):
        """
        Without adjusting the the and time based tzinfo
        """
        year, month, day = self._validate(
            year if year else self.year,
            month if month else self.month,
            day if day else self.day
        )

        result = JalaliDatetime(year,
                                month,
                                day,
                                self.hour if hour is None else hour,
                                self.minute if minute is None else minute,
                                self.second if second is None else second,
                                self.microsecond if microsecond is None else microsecond,
                                self.tzinfo if tzinfo is None else tzinfo)
        # TODO: Test Case required
        # if hour: result.hour = hour
        # if minute: result.minute = minute
        # if second: result.second = second
        # if microsecond: result.microsecond = microsecond
        # if tzinfo: result.tzinfo = tzinfo
        return result

    def astimezone(self, tz):
        if self.tzinfo is tz:
            return self
        if self.tzinfo:
            utc = self - self.utcoffset()
        else:
            utc = self
        return tz.fromutc(utc.replace(tzinfo=tz))

    def utcoffset(self):
        if self.tzinfo:
            return self.tzinfo.utcoffset(self)
        else:
            return None

    def dst(self):
        """
        If tzinfo is None, returns None, else returns self.tzinfo.dst(self), and raises an exception if the latter doesn’t return None, or a timedelta object representing a whole number of minutes with magnitude less than one day.
        """
        if self.tzinfo:
            return self.tzinfo.dst(self)
        else:
            return None

    def tzname(self):
        if self.tzinfo:
            return self.tzinfo.tzname(self)
        else:
            return None

    def isoformat(self, sep='T'):
        """
        Return a string representing the date and time in ISO 8601 format, YYYY-MM-DDTHH:MM:SS.mmmmmm or, if microsecond is 0, YYYY-MM-DDTHH:MM:SS

        If utcoffset() does not return None, a 6-character string is appended, giving the UTC offset in (signed) hours and minutes: YYYY-MM-DDTHH:MM:SS.mmmmmm+HH:MM or, if microsecond is 0 YYYY-MM-DDTHH:MM:SS+HH:MM
        """
        return self.strftime('%Y-%m-%d' + sep + '%H:%M:%S.%f%z')

    def localshortformat(self):
        return self.strftime('%a %d %b %y %H:%M')

    def localshortformatascii(self):
        return self.strftime('%e %d %g %y %H:%M')

    def localdatetimeformat(self):
        return self.strftime('%A %d %B %Y %I:%M:%S %p')

    def localdatetimeformatascii(self):
        return self.strftime('%E %d %G %Y %I:%M:%S %t')

    def localtimeformat(self):
        return self.strftime('%I:%M:%S %p')


    def hour12(self):
        res = self.hour
        if res > 12:
            res -= 12
        elif res == 0:
            res = 12
        return res

    def ampm(self):
        if self.hour < 12:
            return AM_PM[0]
        return AM_PM[1]

    def ampmascii(self):
        if self.hour < 12:
            return AM_PM_ASCII[0]
        return AM_PM_ASCII[1]

    def utcoffsetformat(self):
        if self.tzinfo:
            td = self.utcoffset()
            _minutes = td.seconds / 60
            hours = _minutes / 60
            minutes = _minutes % 60
            return '%s%s' % (minutes, hours)
        return ''

    def tznameformat(self):
        return self.tzname() or ''

    def dayofyear(self):
        return (self.date() - JalaliDate(self.year, 1, 1)).days + 1

    def __repr__(self):
        return 'khayyam.JalaliDatetime(%s, %s, %s, %s, %s, %s, %s%s)' % \
               (self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsecond, \
                ', tzinfo=%s' % self.tzinfo if self.tzinfo else '')

    #################
    ### Operators ###
    #################

    def __add__(self, x):
        if isinstance(x, timedelta):
            return JalaliDatetime.from_datetime(self.to_datetime() + x)

        raise ValueError('JalaliDatetime object can added by timedelta or JalaliDate object')

    def __sub__(self, x):
        if isinstance(x, timedelta):
            return JalaliDatetime.from_datetime(self.to_datetime() - x)
        elif isinstance(x, JalaliDatetime):
            return self.to_datetime() - x.to_datetime()
        elif isinstance(x, JalaliDate):
            return self.to_datetime() - JalaliDatetime(x).to_datetime()

        raise ValueError('JalaliDatetime object can added by timedelta, JalaliDatetime or JalaliDate object')

    def __lt__(self, x):
        assert isinstance(x, JalaliDatetime), 'Comparison just allow with JalaliDate'
        return self.to_datetime() < x.to_datetime()

    def __le__(self, x):
        assert isinstance(x, JalaliDatetime), 'Comparison just allow with JalaliDatetime'
        return self.to_datetime() <= x.to_datetime()

    def __hash__(self):
        return super(JalaliDatetime, self).__hash__() ^ \
            hash(self.hour) ^ \
            hash(self.minute) ^ \
            hash(self.second) ^ \
            hash(self.microsecond) ^ \
            hash(self.tzinfo)

    def __eq__(self, x):
        if not x:
            return False
        if isinstance(x, datetime):
            return self.to_datetime().__eq__(x)
        elif isinstance(x, JalaliDatetime):
            return hash(self) == hash(x)
        else:
            raise ValueError('Comparison only allowed with JalaliDatetime and datetime.datetime objects.')


    def __gt__(self, x):
        assert isinstance(x, JalaliDatetime), 'Comparison just allow with JalaliDatetime'
        return self.to_datetime() > x.to_datetime()

    def __ge__(self, x):
        assert isinstance(x, JalaliDatetime), 'Comparison just allow with JalaliDate'
        return self.to_datetime() >= x.to_datetime()


# # Class attributes
JalaliDatetime.min = JalaliDatetime(MINYEAR, 1, 1)
JalaliDatetime.max = JalaliDatetime(MAXYEAR, 12, 29, 23, 59, 59, 999999)
JalaliDatetime.resolution = timedelta(microseconds=1)
