import requests
from diskcache import Cache
from parse import re_groupdict_list, re_groupdict_entry, tocm

cache = Cache(__name__)

ORDERS = "alfs ands ids ents els ists epts olls ox ods ults erts".split()
SUBS = (
    "wass aqu orth ud ust xer torr cry gel hum vitr fluv psamm "
    "turb rend alb per fibr hem sapr fol "
    "sal dur gyps arg calc camb misc1 misc2 misc3"
).split()
TAXA = [f"{s}{o}" for o in ORDERS for s in SUBS]


def suborder_from_full_taxon(taxon):
    # E.G. taxon = Fine-loamy, parasesquic, mesic Typic Hapludults

    # Take the group, the last word in the full name
    # E.G. group = Hapludults
    (_, group) = taxon.strip().rsplit(" ", 1)

    # Find the matches, should be unique
    matches = [t for t in TAXA if t in group]

    if len(matches) == 0:
        raise LookupError(f"No matching group found in '{taxon}'")
    elif len(matches) == 1:
        # Use title case to match other datasets
        return matches[0].title()
    else:
        raise LookupError(f"Multiple matching groups found in '{taxon}': {matches}")


def _parse_soil_series(html):
    series = re_groupdict_entry(r"<h1>(?P<name>.*?)</h1>", html)
    series_name = series["name"].replace(" SERIES", "").title()

    klass = re_groupdict_entry(r"<b>taxonomic class:</b>\s*(?P<class>.*?)(<p>)?\s*\n", html)

    suborder = suborder_from_full_taxon(klass["class"])

    profile_matches = re_groupdict_list(
        (
            r"<b>\s*(?P<designation>\S+)\s*</b>"
            r"-+"
            r"(?:"
            r"(?P<min>\S+)\s+to\s+(?P<max>\S+)"
            r"|"
            r"(?P<depth>\S+?)"
            r")"
            r"\s*(?P<unit>inch|cm)"
        ),
        html,
    )

    # Check for unexpected units
    bad_units = [
        match["unit"] for match in profile_matches
        if match["unit"] not in ["inch", "cm"]
    ]
    if bad_units:
        raise TypeError(f"Unexpected units detected: {bad_units}")

    profile = [_format_horizon(match) for match in profile_matches]

    return {
        "series": series_name,
        "class": klass["class"],
        "suborder": suborder,
        "profile": profile,
    }


def _format_horizon(horizon):
    if horizon.get("depth") is not None:
        start = tocm(horizon["depth"], horizon["unit"])
        end = None
    else:
        start = tocm(horizon["min"], horizon["unit"])
        end = tocm(horizon["max"], horizon["unit"])
    return (horizon["designation"], start, end)


def _get_soil_series(name):
    name = name.replace(" ", "_").upper()
    first = name[0]
    url = f"https://soilseries.sc.egov.usda.gov/OSD_Docs/{first}/{name}.html"
    return requests.get(url)


@cache.memoize()
def soil_series(name):
    res = _get_soil_series(name)
    res.raise_for_status()
    return _parse_soil_series(res.text)


def multiple_soil_series(names):
    return [soil_series(name) for name in names]


def soil_series_dict(names):
    return {
        s["series"]: s for s in multiple_soil_series(names)
    }
