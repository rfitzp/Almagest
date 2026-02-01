# Script to determine syzygies in given year

import math

degtorad = math.pi/180.
radtodeg = 180./math.pi

# Epoch
t0 = 2451545.0

# Solar parameters
nS   = 0.98564735
ntS  = 0.98560025
lb0S = 280.458
M0S  = 357.588
eS   = 0.016711

# Lunar parameters
eM   = 0.054881
nM   = 13.17639646
ntM  = 13.06499295
nbM  = 13.22935027
lb0M = 218.322
M0M  = 134.916
F0M  = 93.284
iM   = 5.161

def julian_day_number(day, month, year):
    """
    Return Julian Day Number (integer) for a Gregorian calendar date.
    day, month, year are integers.

    JDN starts at noon UT; this returns the civil-day JDN.
    """

    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12*a - 3

    jdn = (day
           + (153*m + 2)//5
           + 365*y
           + y//4
           - y//100
           + y//400
           - 32045)

    return jdn

def deg_to_degmin(angle):
    """
    Convert fractional degrees to (degrees, minutes),
    with minutes rounded to nearest integer.
    Sign is carried by degrees.
    """

    sign = -1 if angle < 0 else 1
    angle = abs(angle)

    deg = int(angle)
    minutes = round((angle - deg) * 60)

    # handle rounding overflow (e.g., 59.9 -> 60)
    if minutes == 60:
        deg += 1
        minutes = 0

    deg *= sign

    return deg, minutes

def Get_Lambda_Sun (t):
    """
    Takes Julian day number and returns solar ecliptic longitude
    and mean anomaly in degrees
    """

    lab = lb0S + nS  * (t - t0)
    M   = (M0S  + ntS * (t - t0)) % 360.

    labr = lab * degtorad
    Mr   = M   * degtorad

    qr   = 2.*eS * math.sin (Mr) + 1.25 * eS*eS * math.sin (2.*Mr)
    q    = qr * radtodeg

    lam  = lab + q

    return lam, M

def Get_Lambda_Moon (t):
    """
    Takes Julian day number and returns lunar ecliptic longitude and latitude
    in degrees and minutes
    """

    labM = lb0M + nM  * (t - t0)
    MM   = (M0M  + ntM * (t - t0)) % 360.
    FbM  = (F0M  + nbM * (t - t0)) % 360.

    lamS, MS = Get_Lambda_Sun (t)

    Db = labM - lamS

    q1 = (2.*eM * math.sin (MM*degtorad) + 1.430 * eM*eM * math.sin (2.*MM*degtorad)) * radtodeg
    q2 = (0.422 * eM * math.sin ((2.*Db - MM)*degtorad)) * radtodeg
    q3 = (0.211 * eM * (math.sin (2.*Db*degtorad) - 0.066 * math.sin (Db*degtorad))) * radtodeg
    q4 = - 0.051 * eM * math.sin (MS*degtorad) * radtodeg
    q5 = - 0.038 * eM * math.sin (2.*FbM*degtorad) * radtodeg

    lamM = labM + q1 + q2 + q3 + q4 + q5

    FM = FbM + q1 + q2 + q3 + q4 + q5

    betaM = math.sin (math.sin (iM*degtorad) * math.sin (FM*degtorad)) * radtodeg

    return lamM, betaM

def Get_DMS (t):

    lamS, SM    = Get_Lambda_Sun  (t)
    lamM, betaM = Get_Lambda_Moon (t)

    D = lamM - lamS

    return D

def Get_D (t0, t):

    return Get_DMS (t0 + t) - Get_DMS (t0)

def Get_New_Moon (t0, t, i):

    target = 360.*i

    D = Get_D (t0, 0.)
    t = (target - D) /(nM - nS)

    for j in range (10):
        D  = Get_D (t0, t)
        t += (target - D) /(nM - nS)
 
yr   = input ("\nyear ? ")
year = int (yr)
t0   = julian_day_number (1, 1, year)
t    = 0.

Get_New_Moon (t0, t, 1)
