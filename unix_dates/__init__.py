import datetime
import time


class UnixDate(object):
    ISO_DATE_FMT = "%Y-%m-%dT%H:%M:%S"
    AWS_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f+0000"

    """
    Utilities to convert dates to Unix time and back.

    Unix timestamps are the format we use to store dates in the system. This is a consistent way to store dates - cross
    time-zones, efficiently, without having to parse strings back and forth.
    """

    class UTCTimeZoneInfo(datetime.tzinfo):

        UTC_OFFSET_SECONDS = -1 * (time.timezone if (time.localtime().tm_isdst == 0) else time.altzone)

        def utcoffset(self, dt):
            return datetime.timedelta(seconds=self.UTC_OFFSET_SECONDS)

        def dst(self, dt):
            return datetime.timedelta(0)

    UTC = UTCTimeZoneInfo()

    @classmethod
    def now(cls):
        """
        :rtype: float
        :return: The Unix epoch: number of seconds that have elapsed since January 1, 1970 (UTC)
        """
        return cls.to_unix_time(datetime.datetime.now())

    @classmethod
    def to_unix_time(cls, dt):
        """
        convert datetime to epoch
        :type dt: datetime.datetime
        :rtype: float
        :return: The Unix epoch: number of seconds that have elapsed since January 1, 1970
        """

        timetuple = dt.timetuple()
        return time.mktime(timetuple)

    @classmethod
    def to_unix_time_from_iso_format(cls, date_str):
        """
        Parse ISO formatted strings back into unix timestamp

        :param date_str: String of date in ISO format
        :type date_str: str|unicode
        :rtype: float
        :return: The Unix epoch: number of seconds that have elapsed since January 1, 1970
        """

        if isinstance(date_str, (unicode, str,)):
            # is on 0 milliseconds
            # here are few solutions:
            #   http://stackoverflow.com/questions/30584364/python-strptime-format-with-optional-bits

            no_ms = date_str.split('.')[0]
            value = datetime.datetime.strptime(no_ms, cls.ISO_DATE_FMT)
            return cls.to_unix_time(value)

        else:
            raise ValueError("Failed convert {} {} to unix time".format(str.__class__, date_str))

    @classmethod
    def to_unix_time_from_aws_format(cls, date_str):
        """
        Parse AWS date formats back into unix timestamp

        :param date_str: String of date in ISO format
        :type date_str: str
        :rtype: float
        :return: The Unix epoch: number of seconds that have elapsed since January 1, 1970
        """
        return cls.to_unix_time(datetime.datetime.strptime(date_str, cls.AWS_DATE_FORMAT))

    @classmethod
    def to_datetime(cls, unix_time_sec):
        """
        :type unix_time_sec: float
        :rtype: datetime.datetime
        """

        return datetime.datetime.fromtimestamp(timestamp=unix_time_sec, tz=cls.UTC)

    @classmethod
    def to_naive_datetime(cls, unix_time_sec):
        """
        :type unix_time_sec: float
        :rtype: datetime.datetime
        """

        return datetime.datetime.fromtimestamp(timestamp=unix_time_sec)


class UnixTimeDelta(object):
    """
    Convert time delta to unix time (allow easy calculations with UnixDate)
    """
    SECONDS_IN_HOUR = 60 * 60
    SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR

    @classmethod
    def calc(cls, days=0, hours=0, minutes=0, seconds=0, millis=0):
        return days * cls.SECONDS_IN_DAY + \
               hours * cls.SECONDS_IN_HOUR + \
               minutes * 60 + \
               seconds + \
               millis / 1000
