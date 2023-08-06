import os
import datetime
import math
from astroquery.simbad import Simbad
import requests
import matplotlib.pyplot as plt
from typing import Union

"""
***********************
***********************
** TIME CALCULATIONS **
***********************
***********************
"""
# returns the time as an str: like 5:55:0 where 5 is hour, 55 is minute, 0 is second
def current_time():
    time_str = os.popen('date +%H:%M:%S').read().strip()
    return time_str

# returns the date as an str: like 4/7/23 where 4 is the month, 7 is the day, 23 is the year
def current_date():
    date_str = os.popen('date +%D').read().strip()
    return date_str

# given a time, return the local julian date (i.e, 2451545 (Jan 1st 2000))
def local_julian_date(date=datetime.datetime.now()):
    time = date.timestamp() * 1000  # Convert to milliseconds
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() is not None else 0  # Convert to minutes
    return (time / 86400000) - (tzoffset / 1440) + 2440587.5  # return the Julian Date

# given a julian date, it converts it to a datetime time
def fromJulian(j):
    J1970 = 2440588
    dayMs = 24 * 60 * 60 * 1000
    return datetime.datetime.fromtimestamp((j + 0.5 - J1970) * dayMs / 1000)

# returns the amount of days since the J2000 epoch
def daysSinceJ2000():
    jd = local_julian_date()
    return jd - 2451545

# helper method for the local sidereal time calculation
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

# get the decimal hours based on a datetime.datetime.now() object
def decimalhours(now):
    return (((now.second / 60) + now.minute) / 60) + now.hour

# helper method for the local sidereal time
def gst(jd, dechours):
    S = jd - 2451545
    T = S / 36525
    T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T ** 2)
    if T0 < 0:
        T0 = (T0 + abs(T0) // 24 * 24) % 24
    else:
        T0 = T0 % 24
    T0 = T0 + (dechours * 1.002737909)
    if T0 < 0:
        T0 = T0 + 24
    if T0 > 24:
        T0 = T0 - 24
    return T0

# returns the local sidereal time
def local_sidereal_time(long):
    now = datetime.datetime.utcnow()
    jd = local_julian_date()
    dechours = decimalhours(now)
    gstime = gst(jd, dechours)
    LONGITUDE = long
    utcdiff = math.fabs(LONGITUDE) / 15
    if sign(LONGITUDE) == -1:
        lstime = gstime - utcdiff
    else:
        lstime = gstime + utcdiff
    if lstime > 24:
        lstime = lstime - 24
    if lstime < 0:
        lstime = lstime + 24

    raw = lstime
    h = math.floor(lstime)
    m = math.floor((lstime - h) * 60)
    s = math.floor((((lstime - h) * 60) - m) * 60)

    times = {
        "raw": raw,
        "hour": h,
        "minute": m,
        "second": s
    }
    return times


"""
****************
****************
GENERAL SUN CALC
****************
****************
"""

def declination(l, b):
    e = math.radians(23.4397)  # obliquity of the ecliptic in degrees
    return math.asin(
        math.sin(math.radians(b)) * math.cos(e) + math.cos(math.radians(b)) * math.sin(e) * math.sin(math.radians(l)))

def solar_mean_anomaly(d):
    """
    :param d: days since J2000
    :return: the solar mean anomaly for EARTH (other planets in other function)
    """
    rad = math.pi / 180.0
    return rad * (357.5291 + 0.98560028 * d)

def ecliptic_longitude(M):
    """
    :param M: solar mean anomaly
    :return: the ecliptic longitude of the sun
    """
    rad = math.pi / 180.0
    PI = math.pi
    C = rad * (1.9148 * math.sin(M) + 0.02 * math.sin(2 * M) + 0.0003 * math.sin(3 * M))  # equation of center
    P = rad * 102.9372  # perihelion of the Earth
    return M + C + P + PI

def solar_hour_angle(longitude, lst):
    """Calculate the solar hour angle for a given longitude and local sidereal time."""
    # Convert longitude and LST to radians
    longitude = math.radians(longitude)
    lst = math.radians(lst)
    # Calculate the solar noon for the given longitude
    solarNoon = longitude + (12 - 12 * 4.0 / 1440) * math.radians(360) / 24
    # Calculate the solar hour angle
    hourAngle = lst - solarNoon
    return hourAngle

def altitude(lat, long):
    """
    :param lat: the latitude of the user
    :param long: the longitude of the user
    :return: the altitude of the sun
    """
    long = -long
    d = daysSinceJ2000()
    M = solar_mean_anomaly(d)
    L = ecliptic_longitude(M)
    dec = declination(L, 0)
    H = solar_hour_angle(long, local_sidereal_time(long)['raw'])
    a = math.asin(math.sin(lat) * math.sin(dec) + math.cos(lat) * math.cos(dec) * math.cos(H))
    return math.degrees(a)

def azimuth(lat, long):
    """
    :param lat: latitude of the user
    :param long: longitude of the user
    :return: the azimuth of the sun in degrees
    """
    long = -long
    d = daysSinceJ2000()
    M = solar_mean_anomaly(d)
    L = ecliptic_longitude(M)
    H = solar_hour_angle(long, local_sidereal_time(long)['raw'])
    dec = declination(L, 0)
    return math.degrees(math.atan2(math.sin(H), math.cos(H) * math.sin(lat) - math.tan(dec) * math.cos(lat)))

# returns the mean anomaly of a planet
def mean_anomaly(planet):
    """
    :param planet: planet is the desired planet
    :return: the mean anomaly of the planet
    """
    # formula from https://www.aa.quae.nl/en/reken/zonpositie.html
    # formula is M = (M0 + M1 * (J - J2000)) mod 360˚
    J2000 = 2451545
    m_list = [
        (174.7948, 4.09233445),
        (50.4161, 1.60213034),
        (357.5291, 0.98560028),
        (19.3730, 0.52402068),
        (20.0202, 0.08308529),
        (317.0207, 0.03344414),
        (141.0498, 0.01172834),
        (256.2250, 0.00598103),
        (14.882, 0.00396),
    ]
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    plan_number = planetMap.get(planet, 2)  # if the planet is not found, calculate for earth
    m_row = m_list[plan_number]
    M = (m_row[0] + m_row[1] * (local_julian_date() - J2000)) % 360
    return M

# returns the mean anomaly of a planet
def mean_anomaly_over_time(planet: any) -> list[int]:
    """
    :param planet: a planet to calculate the mean anomaly for
    :return: a list of rounded mean anomalies for the planet through the next 30 days.
    """
    # formula from https://www.aa.quae.nl/en/reken/zonpositie.html
    # formula is M = (M0 + M1 * (J - J2000)) mod 360˚
    J2000 = 2451545
    m_list = [
        (174.7948, 4.09233445),
        (50.4161, 1.60213034),
        (357.5291, 0.98560028),
        (19.3730, 0.52402068),
        (20.0202, 0.08308529),
        (317.0207, 0.03344414),
        (141.0498, 0.01172834),
        (256.2250, 0.00598103),
        (14.882, 0.00396),
    ]
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    Mlist = []

    plan_number = planetMap.get(planet, 2)  # if the planet is not found, calculate for earth
    m_row = m_list[plan_number]
    for i in range(31):
        M = (m_row[0] + m_row[1] * ((local_julian_date() + i)- J2000)) % 360
        Mlist.append(round(M))

    return Mlist

# the equation of center for any planet
def equation_of_center(planet):
    c_dict = {
        "mercury": [23.4400, 2.9818, 0.5255, 0.1058, 0.0241, 0.0055],  # 0.0026 is the maximum error
        "venus": [0.7758, 0.0033, 0, 0, 0, 0],  # 0.0000 is the maximum error
        "earth": [1.9148, 0.0200, 0.0003, 0, 0, 0],  # 0.0000 is the maximum error
        "mars": [10.6912, 0.6228, 0.0503, 0.0046, 0.0005, 0],  # 0.0001 is the maximum error
        "jupiter": [5.5549, 0.1683, 0.0071, 0.0003, 0, 0],  # 0.0001 is the maximum error
        "saturn": [6.3585, 0.2204, 0.0106, 0.0006, 0, 0],  # 0.0001 is the maximum error
        "uranus": [5.3042, 0.1534, 0.0062, 0.0003, 0, 0],  # 0.0001 is the maximum error
        "neptune": [1.0302, 0.0058, 0, 0, 0, 0],  # 0.0001 is the maximum error
        "pluto": [28.3150, 4.3408, 0.9214, 0.2235, 0.0627, 0.0174]  # 0.0096 is the maximum error
    }
    # the formula used is from https://www.aa.quae.nl/en/reken/zonpositie.html#10
    # c = c1 * sin(m) + c2 * sin(2m) + c3 * sin(3m) + c4 * sin(4m) + c5 * sin(5m) + c6 * sin(6m)
    c = c_dict.get(planet, [1.9148, 0.0200, 0.0003, 0, 0, 0])
    m = mean_anomaly(planet)
    center_eq = c[0] * math.sin(m) + c[1] * math.sin(2 * m) + c[2] * math.sin(3 * m) + c[3] * math.sin(4 * m) + \
                c[4] * math.sin(5 * m) + c[5] * math.sin(6 * m)
    return center_eq

# return the true anomaly of the planet
def true_anomaly(planet):
    c = equation_of_center(planet)
    m = mean_anomaly(planet)
    return m + c  # the equation of center is the correction factor

# return the perihelion and obliquity of a planet
def get_peri_obli(planet):
    perihelion_longitude_and_obliquity = [
        (230.3265, 0.0351),
        (73.7576, 2.6376),
        (102.9373, 23.4393),
        (71.0041, 25.1918),
        (237.1015, 3.1189),
        (99.4587, 26.7285),
        (5.4634, 82.2298),
        (182.2100, 27.8477),
        (184.5484, 119.6075),
    ]
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    key = planetMap.get(planet, 2)
    datatuple = perihelion_longitude_and_obliquity[key]
    perihelion = datatuple[0]
    obliquity = math.radians(datatuple[1])
    return perihelion, obliquity

# return the ecliptical longitude of a planet
def ecliptical_longitude(planet):
    peri, obli = get_peri_obli(planet)  # setup information
    L = mean_anomaly(planet) + peri
    Lsun = L + 180
    long = (Lsun + equation_of_center(planet)) % 360
    return math.radians(long)

# the equatorial coordinates of a planet
def equatorial_coordinates(planet):
    long = ecliptical_longitude(planet)
    peri, obli = get_peri_obli(planet)
    asun = math.atan2(math.sin(long) * math.cos(obli), math.cos(long))
    decsun = math.asin(math.sin(long) * math.sin(obli))
    return {
        'ra': math.degrees(asun),
        'dec': math.degrees(decsun)
    }

# the solar transit julian of a planet
def local_solar_transit(planet, long):
    """
    :param planet: name of the desired planet
    :param long: longitude EAST (i.e, west of the prime meridian is negative)
    :return: the solar transit julian
    """
    long = -long
    Jtable = [
        [45.3497, 11.4556, 0, 175.9386],
        [52.1268, -0.2516, 0.0099, -116.7505],
        [0.0009, 0.0053, -0.0068, 1.0000000],
        [0.9047, 0.0305, -0.0082, 1.027491],
        [0.3345, 0.0064, 0, 0.4135778],
        [0.0766, 0.0078, -0.0040, 0.4440276],
        [0.1260, -0.0106, 0.0850, -0.7183165],
        [0.3841, 0.0019, -0.0066, 0.6712575],
        [4.5635, -0.5024, 0.3429, 6.387672]
    ]
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    plannumber = planetMap.get(planet, 2)
    Jrow = Jtable[plannumber]
    j0 = Jrow[0]
    j1 = Jrow[1]
    j2 = Jrow[2]
    j3 = Jrow[3]
    nx = (local_julian_date() - 2451545 - j0) / j3 - long / 360
    n = math.floor(nx)
    jx = local_julian_date() + j3 * (n - nx)
    peri, obli = get_peri_obli(planet)
    L = mean_anomaly(planet) + peri
    lsun = L + 180
    jtransit = jx + j1 * math.sin(math.radians(mean_anomaly(planet))) + j2 * math.sin(2 * math.radians(lsun))
    return jtransit + 1

# returns the distance to the sun
def distance_to_sun(planet):
    square_table = [
        0.37073,
        0.72330,
        0.99972,
        1.51039,
        5.19037,
        9.52547,
        19.17725,
        30.10796,
        37.09129
    ]
    e_table = [
        0.20563,
        0.00677,
        0.01671,
        0.09340,
        0.04849,
        0.05551,
        0.04630,
        0.00899,
        0.2490,
    ]
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    key = planetMap.get(planet, 2)
    e = e_table[key]
    square = square_table[key]
    r = square / 1 + e * math.cos(true_anomaly(planet))
    return r

# returns the heliocentric coordinates of the planet
def planet_heliocentric_coordinates(planet):
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    r = distance_to_sun(planet)
    horse_table = [
        48.331,
        76.680,
        174.873,
        49.558,
        100.464,
        113.666,
        74.006,
        131.784,
        110.307
    ]
    i_table = [
        7.005,
        3.395,
        0.000,
        1.850,
        1.303,
        2.489,
        0.773,
        1.770,
        17.140,
    ]
    w_table = [
        29.125,
        54.884,
        288.064,
        286.502,
        273.867,
        339.391,
        98.999,
        276.340,
        113.768
    ]
    key = planetMap.get(planet, 2)
    i = i_table[key]
    horse = horse_table[key]
    w = w_table[key]
    v = true_anomaly(planet)
    r = distance_to_sun(planet)
    xplanet = r * (math.cos(horse) * math.cos(w + v) - math.sin(horse) * math.cos(i) * math.sin(w + v))
    yplanet = r * (math.sin(horse) * math.cos(w + v) + math.cos(horse) * math.cos(i) * math.sin(w + v))
    zplanet = r * math.sin(i) * math.sin(w + v)
    return xplanet, yplanet, zplanet

# returns the geocentric coordinates of the planet
def planet_geocentric_coordinates(planet):
    x, y, z = planet_heliocentric_coordinates('earth')
    xplanet, yplanet, zplanet = planet_heliocentric_coordinates(planet)
    return xplanet - x, yplanet - y, zplanet - z

# returns the geocentric latitude and longitude of the planet
def planet_geocentric_lat_long(planet):
    x, y, z = planet_geocentric_coordinates(planet)
    change = math.sqrt((x ** 2) + (y ** 2) + (z ** 2))
    long = math.atan2(y, x)
    lat = math.asin(z / change)
    return lat, long


"""
********************
********************
**STAR CALCULATION**
********************
********************
"""
star_catalog = {
    'Sun': 'G2V',
    'Sirius': 'A1V',
    'Betelgeuse': 'M2Iab',
    'Rigel': 'B8Ia',
    'Vega': 'A0Va',
    'Alpha Centauri A': 'G2V',
    'Alpha Centauri B': 'K1V',
    'Proxima Centauri': 'M5Ve',
    'Polaris': 'F7Ib',
    'Capella': 'G5III',
    'Arcturus': 'K1.5III',
    'Aldebaran': 'K5III',
    'Deneb': 'A2Ia',
    'Antares': 'M1.5Iab-IbB',
    'Altair': 'A7V',
    'Fomalhaut': 'A3V',
    'Spica': 'B1III-IV',
    'Bellatrix': 'B2III',
    'Regulus': 'B7V',
    'Mizar': 'A2V',
    'Castor': 'A1V',
    'Pollux': 'K0III',
    'Achernar': 'B3Vp',
    'Acrux': 'B0.5IV',
    'Alnair': 'B7IV-V',
    'Atria': 'K2Ib-IIa',
    'Canopus': 'F0Ib',
    'Gamma Velorum': 'WC8+O9I',
    'Hadar': 'B1IV',
    'Miaplacidus': 'A0III',
    'Naos': 'O5If',
    'Rigil Kentaurus': 'G2V+K1V',
    'Sadr': 'F8Ib',
    'Shaula': 'B0.5IV-V',
    'Suhail': 'K4Ib-II',
    'Adhara': 'B2II',
    'Albireo A': 'K3II-III',
    'Albireo B': 'B8V',
    'Alcor': 'A5V',
    'Alioth': 'A0p',
    'Alkaid': 'B3V',
    'Alnath': 'B7III',
    'Alnilam': 'B0Ia',
    'Alnitak': 'O9.5Ib',
    'Alpha Aurigae': 'A7IV',
    'Alpha Boötis': 'K2III',
    'Alpha Camelopardalis': 'A3V',
    'Alpha Carinae': 'F0Ia',
    'Alpha Cephei': 'A7IV',
    'Alpha Columbae': 'B5III',
    'Alpha Crucis': 'B0.5IV',
    'Alpha Eridani': 'K0III',
    'Alpha Geminorum': 'A1V',
    'Alpha Herculis': 'K3II',
    'Alpha Leporis': 'B5V',
    'Alpha Lupi': 'B1.5III',
    'Alpha Ophiuchi': 'A5III',
    'Alpha Pavonis': 'B2IV',
    'Alpha Pegasi': 'B9III',
    'Alpha Persei': 'F5Ib',
}


def map_star(star):
    type = star_catalog.get(star, "Star not currently supported")
    return type

def get_object_equatorial_coords(obj_name):
    """
    :param obj_name: name of the SIMBAD object
    :return: the RA and declination of the object
    """
    # Query the SIMBAD database for the object
    result_table = Simbad.query_object(obj_name)
    # Extract the RA and Dec coordinates from the result table
    ra = result_table['RA'][0]
    dec = result_table['DEC'][0]
    # Return the RA and Dec coordinates as floats
    return ra, dec

def calculate_energy(mass):
    c = 299792458  # speed of light in meters per second
    energy = mass * c**2
    return energy

def definition_of(word):
    # make a request to the Wikipedia API
    response = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{word}")
    # check if the request was successful
    if response.status_code != 200:
        return "Sorry, I could not find information on that word."
    # extract the summary text from the response
    summary = response.json()['extract']
    return summary

"""
******************
******************
*MOON CALCULATION*
******************
******************
"""

LUNAR_MONTH = 29.530588853

def get_lunar_age():
    percent = get_lunar_age_percent()
    age = percent * LUNAR_MONTH
    return age


def get_lunar_age_percent():
    julian_date = local_julian_date()
    return normalize((julian_date - 2451550.1) / LUNAR_MONTH)


def normalize(value):
    value = value - int(value)
    if value < 0:
        value = value + 1
    return value


def getLunarPhase():
    age = get_lunar_age()
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
    return "New"


"""
*******************
*******************
**TRIGONOMETRY*****
*******************
*******************
"""
def sin(x):
    return math.sin(x)

def arcsin(x):
    return math.asin(x)

def tan(x):
    return math.tan(x)

def arctan(x):
    return math.atan(x)

def arctan2(y, x):
    return math.atan2(y, x)

def sqrt(x):
    return math.sqrt(x)

def cos(x):
    return math.cos(x)

def arccos(x):
    return math.acos(x)

def cosh(x):
    return math.cosh(x)

def arccosh(x):
    return math.acosh(x)

def power(x, exponent):
    return x ** exponent

def root_of(x, root):
    return x ** (1/root)

def sinh(x):
    return math.sinh(x)

def tanh(x):
    return math.tanh(x)

def arctanh(x):
    return math.atanh(x)

def arcsinh(x):
    return math.asinh(x)
"""
**********************
**********************
*****ESTIMATION*******
**********************
**********************
"""
def gravitational_force(m_obj: Union[int, float], r: Union[int, float]) -> float:
    """
    Estimate the gravitational force experienced by Earth due to another object.
    :param m_obj: mass of the object in kg
    :param r: distance between the object and the Earth in AU
    :return: gravitational force in newtons
    """
    au_to_meters = 1.496e11
    G = 6.6743e-11  # gravitational constant in m^3/(kg*s^2)
    M_earth = 5.9722e24  # mass of Earth in kg
    F = G * M_earth * m_obj / (r * au_to_meters)**2
    return F


"""
*********************
*********************
VISUAL REPRESENTATION
*********************
*********************
"""

def plot_list(data, planet):
    plt.axes()
    plt.xlabel("Days")
    plt.ylabel("Mean Anomaly")
    plt.title(f"The Mean Anomaly of {planet}")
    x = range(len(data))
    y = data
    plt.scatter(x, y)
    plt.show()


def mean_anomaly_plot(planet):
    planetMap = {
        'mercury': 0,
        'venus': 1,
        'earth': 2,
        'mars': 3,
        'jupiter': 4,
        'saturn': 5,
        'uranus': 6,
        'neptune': 7,
        'pluto': 8,
    }
    if planetMap.get(planet, None) is None:
        plot_list(mean_anomaly_over_time(planet), 'earth')
    else:
        plot_list(mean_anomaly_over_time(planet), planet)

