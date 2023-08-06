# Standard library imports
import datetime as dt
from typing import List, Union

# Third party imports
import pandas as pd

# DSC imports
from dsc.util.error import InvalidArgumentError

# fmt: off
__all__ = [
    "is_valid_datetime",
    "is_valid_date",
    "date_to_datetime",
    "datetime_to_str",
    "str_to_datetime",
    "date_to_str",
    "str_to_date",
    "to_date",
    "to_str",
    "to_datetime",
    "date_range",
]
# fmt: on


def str_to_datetime(s: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> dt.datetime:
    """
    Convert a string object to a datetime.

    Args:
        s: string to convert
        fmt: format to use for conversion

    Returns:
        datetime
    """
    try:
        return dt.datetime.strptime(s, fmt)
    except ValueError:
        raise InvalidArgumentError(f"Not a valid date or datetime: '{s}, {fmt}'.")


def str_to_date(s: str, fmt: str = "%Y-%m-%d") -> dt.date:
    """
    Convert a string object to a date.

    Args:
        s: string to convert
        fmt: format to use for conversion

    Returns:
        date
    """
    return str_to_datetime(s, fmt).date()


def datetime_to_str(d: dt.datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Convert a datetime object to a string.

    Args:
        d: datetime to convert
        fmt: format to use for the conversion

    Returns:
        output string
    """
    try:
        return d.strftime(fmt)
    except ValueError:
        raise InvalidArgumentError(f"Not a valid date or datetime: '{d}, {fmt}'.")


def date_to_str(d: dt.date, fmt: str = "%Y-%m-%d") -> str:
    """
    Convert a date object to a string.

    Args:
        d: date to convert
        fmt: format to use for the conversion

    Returns:
        output string

    """
    return datetime_to_str(dt.datetime(*d.timetuple()[:6]), fmt)


def is_valid_datetime(s: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> bool:
    """
    Determine if string represents valid datetime.

    Args:
        s: string to test
        fmt: format to validate against

    Returns:
        bool
    """
    try:
        dt.datetime.strptime(s, fmt)
        return True
    except ValueError:
        return False


def is_valid_date(s: str, fmt: str = "%Y-%m-%d") -> bool:
    """
    Determine if string represents valid date.

    Args:
        s: string to test
        fmt: format to validate against

    Returns:
        bool
    """
    try:
        dt.datetime.strptime(s, fmt)
        return True
    except ValueError:
        return False


def date_to_datetime(d: dt.date) -> dt.datetime:
    """
    Convert a date object to a datetime object.

    Args:
        d: date to convert

    Returns:
        datetime
    """
    result = dt.datetime(year=d.year, month=d.month, day=d.day)
    return result


def to_datetime(
    v: Union[str, dt.date, dt.datetime, pd.Timestamp], fmt: str = "%Y-%m-%d %H:%M:%S"
) -> dt.date:
    """
    Cast an object is a datetime.

    Args:
        v: value to convert
        fmt: format to use for the conversion

    Returns:
        datetime
    """
    if isinstance(v, str):
        if is_valid_datetime(v, fmt):
            v = str_to_datetime(v, fmt)
        elif is_valid_date(v, "%Y-%m-%d"):
            v = date_to_datetime(str_to_date(v))
        else:
            raise InvalidArgumentError("malformed datetime/date string")
    elif isinstance(v, dt.date):
        v = date_to_datetime(v)
    elif isinstance(v, pd.Timestamp):
        v = v.to_pydatetime()
    elif isinstance(v, dt.datetime):
        pass
    else:
        raise InvalidArgumentError("s must of type date, datetime or str")
    return v


def to_date(v: Union[str, dt.date, dt.datetime], fmt: str = "%Y-%m-%d") -> dt.date:
    """
    Cast an object is a date.

    Args:
        v: value to convert
        fmt: format to use for the conversion

    Returns:
        date
    """
    if isinstance(v, str):
        return str_to_date(v, fmt)
    if isinstance(v, dt.datetime):
        return v.date()
    # must come after datetime because a datetime is a date too
    if isinstance(v, dt.date):
        return v

    raise InvalidArgumentError(
        "s must of type date, datetime or str. "
        "Got '{v}' of type '{t}'.".format(
            v=repr(v),
            t=type(v),
        )
    )


def to_str(v: Union[str, dt.date, dt.datetime], fmt: str = "%Y-%m-%d") -> str:
    """
    Cast an object is a string.

    Args:
        v : value to convert
        fmt: format to use for the conversion

    Returns:
        output string
    """
    if isinstance(v, dt.date) or isinstance(v, dt.datetime):
        s = date_to_str(v, fmt)
    elif isinstance(v, str):
        s = to_str(str_to_date(v, fmt))
    else:
        raise InvalidArgumentError("d must of type date, datetime or str")

    return s


def date_range(
    begin_date: dt.date, end_date: dt.date, freq: str = "D"
) -> List[dt.date]:
    """
    Create a list of dates between begin and end dates.

    Args:
        begin_date: range begin date
        end_date: range end date
        freq:  frequency of range (default is daily: 'D')

    Returns:
        list of dates from begin to end
    """
    result = [
        t.to_pydatetime().date() for t in pd.date_range(begin_date, end_date, freq=freq)
    ]
    return result
