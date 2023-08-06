import math
import datetime

# degree input trigonometry functions

def sin(x): return math.sin(math.radians(x))
def cos(x): return math.cos(math.radians(x))
def tan(x): return math.tan(math.radians(x))
def acos(x): return math.degrees(math.acos(x))
def asin(x): return math.degrees(math.asin(x))
def atan2(y, x): return math.degrees(math.atan2(y, x))

# Version function
def VERSION():
    return "0.0.1"

# 1. TIME
# for these calculations, it is convenient to use Julian dates.
def julian_date(date=datetime.datetime.now()):
    time = date.timestamp() * 1000
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() else 0
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5

J1970 = 2440588
dayMs = 24 * 60 * 60 * 1000
# this is the inverse of the Julian Date function
def fromJulian(j):
    return datetime.datetime.fromtimestamp((j + 0.5 - J1970) * dayMs / 1000.0)

# 2. Mean Anomaly of the Sun
def mean_anomaly(date=datetime.datetime.now()):
    julian = julian_date(date)
    # using formula defined at https://aa.quae.nl/en/reken/zonpositie.html
    M = (357.5291 + 0.98560028 * (julian - 2451545)) % 360
    return M

# 3. Equation of Center
def equation(date = datetime.datetime.now()):
    # using formula defined at https://aa.quae.nl/en/reken/zonpositie.html
    M = mean_anomaly(date)
    C = 1.9148 * sin(M) + 0.0200 * sin(2 * M) + 0.0003 * sin(3 * M)
    return C

# 4. True Anomaly
def true_anomaly(date = datetime.datetime.now()):
    M = mean_anomaly(date)
    C = equation(date)
    return M + C

# 5. The Perihelion and the Obliquity of the Ecliptic
II = 102.9373
e = 23.4393

# 6. The Ecliptical Coordinates
def ecliptical_longitude(date=datetime.datetime.now()):
    L = mean_anomaly(date) + II
    mean = L + 180
    longitude = mean + equation(date)
    return longitude % 360

# 7. The Equatorial Coordinates
def declination(date=datetime.datetime.now()):
    long = ecliptical_longitude(date)
    delta = asin(sin(long) * sin(e))
    return delta

def right_ascension(date=datetime.datetime.now()):
    long = ecliptical_longitude(date)
    alpha = atan2(sin(long) * cos(e), cos(long))
    return alpha

# 8. The Observer
def sidereal_time(longitude, time=datetime.datetime.now()):
    lw = -longitude
    theta = (280.1470 + (360.9856235 * (julian_date(time) - 2451545)) - lw) % 360
    return theta


# 9. The Solar Transit
def solar_transit(longitude, date=datetime.datetime.now()):
    lw = -longitude
    J = julian_date(date)
    J2000 = 2451545.0
    J0, J1, J2, J3 = 0.0009, 0.0053, -0.0068, 1.0000000
    nx = ((J - J2000 - J0)/J3) - lw/360
    n = round(nx)
    jx = J + J3 * (n - nx)
    Jtransit = jx + J1 * sin(mean_anomaly(date)) + J2 * sin(2 * ecliptical_longitude(date))
    return Jtransit

# 10. Sunset and Sunrise Julian
def suntimes(latitude, longitude, date=datetime.datetime.now()):
    ht = acos((sin(-0.83) - sin(latitude) * sin(declination(date))) / cos(latitude) * cos(declination(date)))
    Jtransit = solar_transit(longitude, date)
    Jrise = Jtransit - ht/360
    Jset = Jtransit + ht / 360
    return (Jrise, Jset)

def sunrise(latitude, longitude, date=datetime.datetime.now()):
    sunrise = suntimes(latitude, longitude, date)[0]
    return fromJulian(sunrise)

def sunset(latitude, longitude, date=datetime.datetime.now()):
    sunset = suntimes(latitude, longitude, date)[1]
    return fromJulian(sunset)

# 11. Hour Angle & Horizontal Coordinates
def hour_angle(longitude, date=datetime.datetime.now()):
    return sidereal_time(longitude, date) - right_ascension(date)

#12. Combine all previous methods into a convenient class
class Daystar:
    def __init__(self, latitude, longitude, height=0):
        self.lat = latitude
        self.long = longitude
        self.ht = height

    def set(self, date=datetime.datetime.now()): return sunset(self.lat, self.long, date)
    def rise(self, date=datetime.datetime.now()): return sunrise(self.lat, self.long, date)
    def transit(self, date=datetime.datetime.now(), julian=False): return fromJulian(solar_transit(self.long, date)) if julian == False else solar_transit(self.long, date)
    def right_ascension(self, date = datetime.datetime.now()): return right_ascension(date)
    def declination(self, date=datetime.datetime.now()): return declination(date)
    def ecliptical_longitude(self, date=datetime.datetime.now()): return ecliptical_longitude(date)
    def nadir(self, date=datetime.datetime.now()): return fromJulian(solar_transit(self.long, date) - 0.5)
    def hour_angle(self, date=datetime.datetime.now()): return hour_angle(self.long, date)
    def observer_angle(self): return -2.076 * math.sqrt(self.ht) / 60


