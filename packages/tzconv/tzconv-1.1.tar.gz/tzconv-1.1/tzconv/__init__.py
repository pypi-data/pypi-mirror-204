import sys
import re
import datetime as dt
import zoneinfo as zi

from typing import cast

import click


def make_datetime(date_time: str, timezone: zi.ZoneInfo) -> dt.datetime:
    """Construct a `datetime` instance from a date-time string formatted
    as `YYYY-MM-DD HH:MM` or `HH:MM` and attach timezone information."""

    match = (
        re.match(r"^\s*(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}):(\d{2})\s*$",
                 date_time)
        or re.match(r"^\s*(\d{1,2}):(\d{2})\s*$", date_time)
    )

    if match is None:
        raise ValueError(
            f"Date and time '{date_time}' matches neither "
            + "'YYYY-MM-DD HH:MM' nor 'HH:MM'.")

    if len(match.groups()) == 5:
        year, month, day, hour, minute = tuple(int(x)
                                               for x in match.groups())
    else:
        today = dt.date.today()

        year, month, day = today.year, today.month, today.day
        hour, minute = tuple(int(x) for x in match.groups())

    return dt.datetime(year, month, day, hour, minute, tzinfo=timezone)


def format_datetime(obj: dt.datetime) -> str:
    """Create a human-readable representation of a `datetime`
    object. The resulting string includes the timezone's name and its
    `zoneinfo` key."""

    tz_name = obj.tzname()
    tz_key = cast(zi.ZoneInfo, obj.tzinfo).key

    return f"{tz_name}: {obj.strftime('%Y-%m-%d %H:%M')} ({tz_key})"


@click.command()
@click.option("-d", "--debug", is_flag=True)
@click.option("-f", "--from-tz", required=True, type=str)
@click.option("-t", "--to-tz", required=True, type=str, multiple=True)
@click.argument("date_time", type=str)
def main(from_tz, to_tz, date_time, debug=False):
    if not debug:
        sys.tracebacklimit = 0

    from_tz_obj = zi.ZoneInfo(from_tz)
    to_tz_objs = [zi.ZoneInfo(x) for x in to_tz]

    base_dt = make_datetime(date_time, from_tz_obj)

    print(format_datetime(base_dt))

    for timezone in to_tz_objs:
        print(
            format_datetime(
                base_dt.astimezone(timezone)))


if __name__ == "__main__":
    main()
