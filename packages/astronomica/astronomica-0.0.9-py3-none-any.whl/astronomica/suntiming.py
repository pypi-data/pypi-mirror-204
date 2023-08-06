"""
This code was developed from https://github.com/SatAgro/suntime, 
but with some edits, tweaks, accuracy improvements, and other such edits. 
However, the majority of the code is from that site, which is licensed under a 
GNU Lesser General Public License v3.0 (LGPL-3.0). 
The license can be found at https://github.com/SatAgro/suntime/blob/master/LICENSE
"""
import calendar
import math
import datetime
from dateutil import tz


class SunTimeException(Exception):

    def __init__(self, message):
        super(SunTimeException, self).__init__(message)


class Sun:
    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon

    def get_sunrise_time(self, date=None):

        date = datetime.date.today() if date is None else date
        sr = self._calc_sun_time(date, True)
        if sr is None:
            raise SunTimeException('The sun never rises on this location (on the specified date)')
        else:
            return sr

    def get_local_sunrise_time(self, date=None, local_time_zone=tz.tzlocal()):

        date = datetime.date.today() if date is None else date
        sr = self._calc_sun_time(date, True)
        if sr is None:
            raise SunTimeException('The sun never rises on this location (on the specified date)')
        else:
            return sr.astimezone(local_time_zone)

    def get_sunset_time(self, date=None):

        date = datetime.date.today() if date is None else date
        ss = self._calc_sun_time(date, False)
        if ss is None:
            raise SunTimeException('The sun never sets on this location (on the specified date)')
        else:
            return ss

    def get_local_sunset_time(self, date=None, local_time_zone=tz.tzlocal()):
        date = datetime.date.today() if date is None else date
        ss = self._calc_sun_time(date, False)
        if ss is None:
            raise SunTimeException('The sun never sets on this location (on the specified date)')
        else:
            return ss.astimezone(local_time_zone)

    def _calc_sun_time(self, date, isRiseTime=True, zenith=90.8):
        day = date.day
        month = date.month
        year = date.year

        TO_RAD = math.pi / 180.0
        N1 = math.floor(275 * month / 9)
        N2 = math.floor((month + 9) / 12)
        N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
        N = N1 - (N2 * N3) + day - 30
        lngHour = self._lon / 15

        if isRiseTime:
            t = N + ((6 - lngHour) / 24)
        else:  # sunset
            t = N + ((18 - lngHour) / 24)
        M = (0.9856 * t) - 3.289
        L = M + (1.916 * math.sin(TO_RAD * M)) + (0.020 * math.sin(TO_RAD * 2 * M)) + 282.634
        L = self._force_range(L, 360)  # NOTE: L adjusted into the range [0,360)

        RA = (1 / TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD * L))
        RA = self._force_range(RA, 360)  # NOTE: RA adjusted into the range [0,360]
        Lquadrant = (math.floor(L / 90)) * 90
        RAquadrant = (math.floor(RA / 90)) * 90
        RA = RA + (Lquadrant - RAquadrant)
        RA = RA / 15

        sinDec = 0.39782 * math.sin(TO_RAD * L)
        cosDec = math.cos(math.asin(sinDec))
        cosH = (math.cos(TO_RAD * zenith) - (sinDec * math.sin(TO_RAD * self._lat))) / (
                    cosDec * math.cos(TO_RAD * self._lat))

        if cosH > 1:
            return None  # The sun never rises on this location (on the specified date)
        if cosH < -1:
            return None  # The sun never sets on this location (on the specified date)


        if isRiseTime:
            H = 360 - (1 / TO_RAD) * math.acos(cosH)
        else:  # setting
            H = (1 / TO_RAD) * math.acos(cosH)

        H = H / 15

        T = H + RA - (0.06571 * t) - 6.622

        UT = T - lngHour
        UT = self._force_range(UT, 24)  # UTC time in decimal format (e.g. 23.23)

        hr = self._force_range(int(UT), 24)
        min = round((UT - int(UT)) * 60, 0)
        if min == 60:
            hr += 1
            min = 0

        if hr == 24:
            hr = 0
            day += 1

            if day > calendar.monthrange(year, month)[1]:
                day = 1
                month += 1

                if month > 12:
                    month = 1
                    year += 1

        return datetime.datetime(year, month, day, hr, int(min), tzinfo=tz.tzutc())

    @staticmethod
    def _force_range(v, max):
        # force v to be >= 0 and < max
        if v < 0:
            return v + max
        elif v >= max:
            return v - max

        return v
    

# this can be used to improve the calculation of the sunrise/sunset
def solar_zenith_angle(latitude, solar_declination, hour_angle):
    cos_zenith = math.sin(latitude) * math.sin(solar_declination) + math.cos(latitude) * math.cos(solar_declination) * math.cos(hour_angle)
    zenith_angle = math.acos(cos_zenith)
    return zenith_angle
