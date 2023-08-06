import sys
import re
import datetime as dt
import zoneinfo as zi

from typing import List, cast

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


def match_time_zone_prefix(pattern: str, time_zone: str) -> bool:
    """Predicate that returns True if `pattern` is a prefix of
    `time_zone`.  Case-sensitive."""

    return time_zone.startswith(pattern)


def match_time_zone_abbreviation(pattern: str,
                                 time_zone: str) -> bool:
    """Predicate that returns True if `pattern` is an abbreviation of
    `time_zone`.  Case-sensitive."""

    def get_segments(string: str) -> List[str]:
        return re.findall(r"/?[a-z_]+", string, flags=re.IGNORECASE)

    def get_words(string: str) -> List[str]:
        return re.findall(r"[_]?[a-z]+", string, flags=re.IGNORECASE)

    def get_initials(string: str) -> str:
        return "".join(re.findall(r"([a-z])[a-z]*",
                                  string,
                                  flags=re.IGNORECASE))

    pattern_segments = get_segments(pattern)
    time_zone_segments = get_segments(time_zone)

    if len(pattern_segments) > len(time_zone_segments):
        # Shortcut since pattern cannot match.
        #
        return False

    pattern_index = 0
    time_zone_index = 0

    while True:
        if pattern_index == len(pattern_segments):
            break

        if time_zone_index == len(time_zone_segments):
            # The pattern has leftover segments but the time zone is
            # exhausted.
            #
            return False

        pattern_segment = pattern_segments[pattern_index]
        time_zone_segment = time_zone_segments[time_zone_index]

        # Check if the pattern segment is a prefix of the time zone
        # segment.  E.g., "Lo" for "Los_Angeles".
        #

        if match_time_zone_prefix(pattern_segment, time_zone_segment):
            pattern_index += 1
            time_zone_index += 1

            continue

        # Check if the pattern segment is the initials of the time zone
        # words.  E.g., "LA" for "Los_Angeles".
        #

        pattern_words = get_words(pattern_segment)

        if len(pattern_words) == 1:
            time_zone_initials = get_initials(time_zone_segment)

            if pattern_words[0] == time_zone_initials:
                pattern_index += 1
                time_zone_index += 1

                continue

        # Check if the pattern segment is an abbreviation of the time
        # zone segment.  E.g., "L_Ang" for "Los_Angeles".
        #

        time_zone_words = get_words(time_zone_segment)

        if len(pattern_words) <= len(time_zone_words):
            for pattern_word, time_zone_word in zip(pattern_words,
                                                    time_zone_words):
                if not match_time_zone_prefix(pattern_word,
                                              time_zone_word):
                    break
            else:
                pattern_index += 1
                time_zone_index += 1

                continue

        # Try this pattern segment on the next time zone segment.
        #
        time_zone_index += 1

    return True


def match_time_zone(pattern: str, time_zone: str) -> bool:
    """Predicate that returns True if `pattern` matches `time_zone`.
    Case-insensitive."""

    lowercase_pattern = pattern.lower().replace("-", "_")
    lowercase_time_zone = time_zone.lower().replace("-", "_")

    return (match_time_zone_prefix(lowercase_pattern,
                                   lowercase_time_zone)
            or match_time_zone_abbreviation(lowercase_pattern,
                                            lowercase_time_zone))


def get_time_zones(pattern: str | None) -> set:
    """Get the names of those time zones that match `pattern`.  If
    `pattern` is None, then get all available time zones."""

    time_zones = zi.available_timezones()

    if pattern is not None:
        time_zones = set(
            name
            for name in time_zones
            if match_time_zone(pattern, name))

    return time_zones


def get_time_zone(pattern: str) -> str:
    """Get the name of the time zone that matches `pattern`.  Raises
    `ValueError` if there is no match or more than one match."""

    time_zones = get_time_zones(pattern)

    if len(time_zones) == 0:
        raise ValueError(f"No available time zone matches '{pattern}'.")

    if len(time_zones) > 1:
        raise ValueError(
            "Multiple available time zones are matched by "
            + f"'{pattern}': {', '.join(sorted(time_zones))}.")

    return time_zones.pop()


def print_time_zones(pattern: str | None) -> None:
    """Print all available time zones whose names match `pattern`.  If
    `pattern` is `None`, then print everything."""

    time_zones = get_time_zones(pattern)

    if pattern is not None:
        if len(time_zones) == 0:
            print(f"No available time zone matches '{pattern}'.")
            return

        print("The following time zones are available that match "
              + f"'{pattern}':\n")
    else:
        print("The following time zones are available:\n")

    chars_on_line = 0

    for index, time_zone in enumerate(sorted(time_zones)):
        if index + 1 < len(time_zones):
            output_string = f" {time_zone},"
        else:
            output_string = f" {time_zone}\n"

        if chars_on_line == 0:
            print(" ", end="")

        if (chars_on_line == 0
            or chars_on_line + len(output_string) <= 78):
            print(output_string, end="")

            chars_on_line += len(output_string)
        else:
            print(f"\n {output_string}", end="")

            chars_on_line = len(output_string)


def print_argument_error_and_exit(message: str) -> None:
    """Print an error message, show the help message, and exit."""

    print(f"Error: {message}\n", file=sys.stderr)

    context = click.get_current_context()

    click.echo(context.get_help())
    context.exit()


@click.command(help=("Convert a date and time from one time zone to "
                     + "one or more other time zones."))
@click.option("-d", "--debug", is_flag=True)
@click.option("-l", "--list-tz", is_flag=True,
              help=("List all available time zones. The list can be "
                    + "narrowed by providing the beginning of the name "
                    + "of the time zone, e.g., 'Af', as an additional "
                    + "argument."))
@click.option("-f", "--from-tz", required=False, type=str,
              help="The name of the time zone to convert from.")
@click.option("-t", "--to-tz", required=False, type=str, multiple=True,
              help=("The name of a time zone to convert to. Can use "
                    + "this option multiple times in order to specify "
                    + "several."))
@click.argument("date_time", required=False, type=str)
def main(from_tz, to_tz, date_time, list_tz=False, debug=False):
    if not debug:
        sys.tracebacklimit = 0

    if list_tz:
        if from_tz is not None or len(to_tz) > 0:
            print_argument_error_and_exit(
                "--list-tz cannot be used together with --from-tz or "
                "--to-tz.")

        print_time_zones(date_time)
    elif from_tz is None and len(to_tz) == 0:
        print_argument_error_and_exit(
            "Must specify either --list-tz or --from-tz and --to-tz.")
    elif from_tz is None:
        print_argument_error_and_exit(
            "Must specify --from-tz if using --to-tz.")
    elif len(to_tz) == 0:
        print_argument_error_and_exit(
            "Must specify --to-tz if using --from-tz.")
    else:
        from_tz_obj = zi.ZoneInfo(get_time_zone(from_tz))
        to_tz_objs = [zi.ZoneInfo(get_time_zone(x)) for x in to_tz]

        if date_time is None:
            base_dt = dt.datetime.now(tz=from_tz_obj)
        else:
            base_dt = make_datetime(date_time, from_tz_obj)

        print(format_datetime(base_dt))

        for timezone in to_tz_objs:
            print(
                format_datetime(
                    base_dt.astimezone(timezone)))


if __name__ == "__main__":
    main()
