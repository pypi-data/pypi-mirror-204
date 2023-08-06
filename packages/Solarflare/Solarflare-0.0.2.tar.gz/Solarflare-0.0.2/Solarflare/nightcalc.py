import math
import datetime

LUNAR_MONTH = 29.530588853

def get_julian_date(date=None):
    """Returns the Julian date for the given date."""
    if date is None:
        date = datetime.datetime.utcnow()
    time = date.timestamp() # seconds since epoch
    tzoffset = date.utcoffset().total_seconds() / 60 if date.utcoffset() else 0 # minutes
    return (time / 86400) - (tzoffset / 1440) + 2440587.5

def get_lunar_age(date=None):
    """Returns the age of the moon in days for the given date."""
    percent = get_lunar_age_percent(date)
    age = percent * LUNAR_MONTH
    return age

def get_lunar_age_percent(date=None):
    """Returns the age of the moon as a percentage of the lunar month for the given date."""
    jd = get_julian_date(date)
    return normalize((jd - 2451550.1) / LUNAR_MONTH)

def normalize(value):
    """Normalizes a value to the range [0, 1)."""
    value = value - math.floor(value)
    if value < 0:
        value = value + 1
    return value

def get_lunar_phase(date=None):
    """Returns the phase of the moon for the given date."""
    age = get_lunar_age(date)
    if age < 1.84566:
        return "New"
    elif age < 5.53699:
        return "Waxing Crescent"
    elif age < 9.22831:
        return "First Quarter"
    elif age < 12.91963:
        return "Waxing Gibbous"
    elif age < 16.61096:
        return "Full"
    elif age < 20.30228:
        return "Waning Gibbous"
    elif age < 23.99361:
        return "Last Quarter"
    elif age < 27.68493:
        return "Waning Crescent"
    else:
        return "New"

def lunar_phase(date=None):
    """Returns the phase of the moon for the given date as a float between 0 and 1."""
    age_percent = get_lunar_age_percent(date)
    if age_percent < 0.5:
        return age_percent * 2
    else:
        return (1 - age_percent) * 2


def next_full_moon(date=datetime.datetime.now()):
    """Return the date of the next full moon"""
    phase = 0.0
    full_moon = None
    next_date = date
    while not full_moon:
        next_date += datetime.timedelta(days=1)
        phase = get_lunar_phase(next_date)
        if phase == "Full":
            full_moon = next_date
    return full_moon

def next_new_moon(date=datetime.datetime.now()):
    """Return the date of the next full moon"""
    new_moon = None
    next_date = date
    while not new_moon:
        next_date += datetime.timedelta(days=1)
        phase = get_lunar_phase(next_date)
        if phase == "New":
            new_moon = next_date
    return new_moon

def previous_full_moon(date= datetime.datetime.now()):
    """Return the date of the previous full moon"""
    phase = 0.0
    full_moon = None
    next_date = date
    while not full_moon:
        next_date -= datetime.timedelta(days=1)
        phase = get_lunar_phase(next_date)
        if phase == "Full":
            full_moon = next_date
    return full_moon

def harvest_moon():
    autumn = 22
    year = datetime.datetime.now().year
    sep22 = datetime.datetime(year, 9, autumn)
    full_moon_after = next_full_moon(sep22)
    full_moon_before = previous_full_moon(sep22)
    if abs(full_moon_after - sep22) < abs(sep22 - full_moon_before):
        return full_moon_after
    else:
        return full_moon_before

class Moon:
    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.long = longitude

    def upcoming_harvest_moon(self): return harvest_moon()
    def lunar_phase(self, date=datetime.datetime.now()): return get_lunar_phase(date)
    def phase_percent(self, date=datetime.datetime.now()): return lunar_phase(date)
    def age(self, date = datetime.datetime.now()): return get_lunar_age(date)
    def age_percent(self, date=datetime.datetime.now()): return get_lunar_age_percent(date)



