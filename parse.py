import re


def re_groupdict_seq(regex, string):
    s = string
    match = re.search(regex, s, re.I)
    while match:
        yield {"_match": match.group(0), **match.groupdict()}
        s = s[match.end():]
        match = re.search(regex, s, re.I)


def re_groupdict_list(regex, string):
    return list(re_groupdict_seq(regex, string))


def re_groupdict_entry(regex, string):
    return next(re_groupdict_seq(regex, string), None)


def tocm(s, unit="inch"):
    if s.lower() == "o":
        return 0
    else:
        if unit == "inch":
            return int(round(float(s) * 2.54, 0))
        elif unit == "cm":
            return int(s)
        else:
            raise ValueError(f"Unrecognized units: {unit}")
