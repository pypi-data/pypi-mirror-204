
# `tzconv`: convert a date and time to several time zones at once

This Python package provides a small command-line utility to convert a `YYYY-MM-DD HH:MM` formatted date and time to several other time zones.

## Installation

`tzconv` is available through PyPI:

```
$ python3 -m pip install tzconv
```

Alternatively, you can install it directly from the Codeberg Git repository:

```
$ git clone https://codeberg.org/gnyeki/tzconv
$ python3 -m pip install --user ./tzconv
```

## Usage

### Basic usage

`tzconv` uses the time zone information available through your operating system, so time zones have to be specified accordingly:

```
$ tzconv \
    -f America/New_York \
    -t Pacific/Galapagos \
    -t America/Santa_Isabel \
    "2023-04-25 10:00"
EDT: 2023-04-25 10:00 (America/New_York)
-06: 2023-04-25 08:00 (Pacific/Galapagos)
PDT: 2023-04-25 07:00 (America/Santa_Isabel)
$
```

Time zone names can be shortened as long as they remain unique.
Initials, prefixes, and abbreviations are all recognized:

```
$ tzconv \
    -f ny \
    -t gal \
    -t san_i \
    "2023-04-25 10:00"
EDT: 2023-04-25 10:00 (America/New_York)
-06: 2023-04-25 08:00 (Pacific/Galapagos)
PDT: 2023-04-25 07:00 (America/Santa_Isabel)
$
```

Available time zones can be listed with the `--list-tz` option (or `-l` for short):

```
$ tzconv -l am/n
The following time zones are available that match 'am/n':

  America/Nassau, America/New_York, America/Nipigon, America/Nome,
  America/Noronha, America/North_Dakota/Beulah, America/North_Dakota/Center,
  America/North_Dakota/New_Salem, America/Nuuk
$
```

### Imputing the current date and the current time

If the date is omitted, today's date is imputed:

```
$ tzconv -f ny -t aa 10:00
EDT: 2023-04-20 10:00 (America/New_York)
EAT: 2023-04-20 17:00 (Africa/Addis_Ababa)
$

```

If the time is omitted, too, then `tzconv` imputes the current time:

```
$ tzconv -f ny -t aa
EDT: 2023-04-20 15:03 (America/New_York)
EAT: 2023-04-20 22:03 (Africa/Addis_Ababa)
$
```

### Daylight savings

Daylight savings can complicate conversions.
However, thanks to the Python standard library, `tzconv` is aware of changes to daylight savings, and it infers the correct offsets.
For example, in March 2023, New York switched to daylight savings two weeks earlier than Budapest.
Notice the switch from EST/CET to EDT/CET, and finally to EDT/CEST:

```
$ tzconv -f ny -t bud "2023-03-07 10:00"
EST: 2023-03-07 10:00 (America/New_York)
CET: 2023-03-07 16:00 (Europe/Budapest)
$ tzconv -f ny -t bud "2023-03-14 10:00"
EDT: 2023-03-14 10:00 (America/New_York)
CET: 2023-03-14 15:00 (Europe/Budapest)
$ tzconv -f ny -t bud "2023-03-28 10:00"
EDT: 2023-03-28 10:00 (America/New_York)
CEST: 2023-03-28 16:00 (Europe/Budapest)
$
```

### Custom shell commands for common conversions

If you have a project that spans several time zones, it is convenient to define a command for it in your `.bashrc`, `.zshrc`, or equivalent dot file, depending on what shell you use.
For example, if you are using zsh, you can add the following to `~/.zshrc`:

```sh
project_tz() {
    declare -a opts=(
        --from-tz America/New_York
        --to-tz America/Los_Angeles
        --to-tz America/Halifax
        --to-tz Asia/Karachi
        --to-tz Asia/Calcutta
    )

    if [ "$*" = "" ]; then
        tzconv $opts
    else
        tzconv $opts "$*"
    fi
}
```

Now you can reload `~/.zshrc` and use `project_tz` as a shell command:

```
$ . ~/.zshrc
$ project_tz 2023-04-25 10:00
EDT: 2023-04-25 10:00 (America/New_York)
PDT: 2023-04-25 07:00 (America/Los_Angeles)
ADT: 2023-04-25 11:00 (America/Halifax)
PKT: 2023-04-25 19:00 (Asia/Karachi)
IST: 2023-04-25 19:30 (Asia/Calcutta)
$
```

