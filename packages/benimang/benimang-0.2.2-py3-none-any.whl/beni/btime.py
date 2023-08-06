import datetime as xdatetime
import time as xtime

from beni import bhttp

_serverTime: float = xtime.time()
_initTime: float = xtime.monotonic()


async def networkTime():
    _, response = await bhttp.get('https://www.baidu.com')
    date_str = response.headers['Date']
    return xdatetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT') + xdatetime.timedelta(hours=8)


async def initServerDatetime():
    global _serverTime, _initTime
    _serverTime = (await networkTime()).timestamp()
    _initTime = xtime.monotonic()


def timestamp():
    return _serverTime + xtime.monotonic() - _initTime


def timestampSecond():
    return int(timestamp())


def timestampMillisecond():
    return int(timestamp() * 1000)


def datetime():
    return xdatetime.datetime.fromtimestamp(timestamp())


def date():
    return xdatetime.date.fromtimestamp(timestamp())


def time():
    return datetime().time()


def datetimeStr(fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return datetime().strftime(fmt)


def dateStr(fmt: str = r'%Y-%m-%d'):
    return date().strftime(fmt)


def timeStr(fmt: str = r'%H:%M:%S'):
    return time().strftime(fmt)


def makeDatetime(date_str: str, fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return xdatetime.datetime.strptime(date_str, fmt)


def makeDate(date_str: str, fmt: str = r'%Y-%m-%d'):
    return xdatetime.datetime.strptime(date_str, fmt).date()


# def tomorrowDatetime():
#     return datetime.datetime.combine(
#         nowDate(),
#         datetime.time(),
#     )


# def foreverDatetime():
#     return datetime.datetime(9999, 1, 1)
