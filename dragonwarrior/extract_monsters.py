"""

Extract monster data from Ryan8bit's formula text file.

"""

import re

regex = r"""
^\#(?P<number>\d\d)\s:\s(?P<name>[\w\ ]+)\n.*?
Strength:\s(?P<strength>\d+)\n.*?
Agility:\s(?P<agility>\d+).*?
HP:\s(?P<hp>\d+).*?
SLEEP\sresist:\s(?P<sleep_min>\d+)\s/\s(?P<sleep_max>\d+).*?
STOPSPELL\sresist:\s(?P<stop_min>\d+)\s/\s(?P<stop_max>\d+).*?
HURT\sresist:\s(?P<hurt_min>\d+)\s/\s(?P<hurt_max>\d+).*?
Dodge:\s(?P<dodge_min>\d+)\s/\s(?P<dodge_max>\d+).*?
XP:\s(?P<xp>\d+).*?
GP:\s(?P<gp>\d+).*?
Pattern:\s(?P<pattern>.+?)(?=\#)""".strip()


def slugify(text):
    return re.sub(r"\s", "_", text).lower()


with open("documents/dw_formulas.txt") as fp:
    data = fp.read()
    for match in re.finditer(regex, data, re.DOTALL | re.ASCII | re.MULTILINE | re.VERBOSE):
        d = match.groupdict()
        print(f'  - slug: mob_{slugify(d["name"])}')
        print(f'    name: {d["name"].title()}')
        print(f'    strength: {d["strength"]}')
        print(f'    agility: {d["strength"]}')
        print(f'    sleep_resist: {d["sleep_min"]}~{d["sleep_max"]}')
        print(f'    stopspell_resist: {d["stop_min"]}~{d["stop_max"]}')
        print(f'    hurt_resist: {d["hurt_min"]}~{d["hurt_max"]}')
        print(f'    dodge: {d["dodge_min"]}~{d["dodge_max"]}')
        print(f'    xp: {d["xp"]}')
        print(f'    gp: {d["gp"]}')
