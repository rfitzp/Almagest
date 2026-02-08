# Script to determine full moons in given year

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
rS0  = 15.987

# Lunar parameters
eM   = 0.054881
nM   = 13.17639646
ntM  = 13.06499295
nbM  = 13.22935027
lb0M = 218.322
M0M  = 134.916
F0M  = 93.284
#iM   = 5.161
iM = 5.1281
dM0  = 56.976
rM0  = 15.534

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

def jd_to_gregorian_datetime(jd):
    """
    Convert Julian Day Number (fractional) to
    Gregorian date and time: year, month, day, hour, minute
    Minutes are rounded to nearest integer.
    """
    # Separate integer and fractional part
    jd_int = int(jd + 0.5)
    frac_day = jd + 0.5 - jd_int

    # --- Gregorian calendar conversion ---
    l = jd_int + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    day = l - (2447 * j) // 80
    l = j // 11
    month = j + 2 - 12 * l
    year = 100 * (n - 49) + i + l

    # --- Convert fractional day to hours and minutes ---
    total_hours = frac_day * 24
    hour = int(total_hours)
    minute = round((total_hours - hour) * 60)

    # Handle minute overflow
    if minute == 60:
        hour += 1
        minute = 0
    if hour == 24:
        hour = 0
        # increment date by 1
        # simple fix (naive, works for most purposes)
        day += 1
        # month/year adjustment
        if month in [1,3,5,7,8,10,12]:
            if day > 31:
                day = 1
                month += 1
        elif month in [4,6,9,11]:
            if day > 30:
                day = 1
                month += 1
        else:  # February, ignore leap-year correction for simplicity
            if day > 28:
                day = 1
                month += 1
        if month > 12:
            month = 1
            year += 1

    return year, month, day, hour, minute

def jd_to_gregorian_utc_hour(jd):
    """
    Convert fractional Julian Day Number to Gregorian date and time (UTC),
    rounding time to nearest hour.

    Returns: (year, month, day, hour)
    """

    # Shift so day starts at midnight
    jd += 0.5
    Z = int(jd)
    F = jd - Z

    # Gregorian calendar correction
    alpha = int((Z - 1867216.25) / 36524.25)
    A = Z + 1 + alpha - alpha // 4

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day = B - D - int(30.6001 * E) + F

    if E < 14:
        month = E - 1
    else:
        month = E - 13

    if month > 2:
        year = C - 4716
    else:
        year = C - 4715

    # Separate fractional day → hours
    day_int = int(day)
    frac_day = day - day_int

    hour = int(round(frac_day * 24))

    # handle rounding overflow
    if hour == 24:
        hour = 0
        day_int += 1

    return year, month, day_int, hour

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
    M   = M0S  + ntS * (t - t0)

    labr = lab * degtorad
    Mr   = M   * degtorad

    qr   = 2.*eS * math.sin (Mr) + 1.25 * eS*eS * math.sin (2.*Mr)
    q    = qr * radtodeg

    lam  = lab + q

    rhoS = 15.987 * (1. + eS * math.cos (Mr) + eS*eS * math.cos (2.*Mr))    

    return lam, M, rhoS

def Get_R_Moon (t):
    """
    Takes Julian day number and returns Earth-Moon distance in km
    """

    labM = (lb0M + nM  * (t - t0)) % 360.
    MM   = (M0M  + ntM * (t - t0)) % 360.
    FbM  = (F0M  + nbM * (t - t0)) % 360.

    lamS, MS, rhoS = Get_Lambda_Sun (t)

    Db = labM - lamS
  
    q1 = - (0.9894 * eM * math.cos (MM*degtorad) + 0.4915 * eM*eM * math.cos (2.*MM*degtorad)) 
    q2 = - (0.1751 * eM * math.cos ((2.*Db-MM)*degtorad))                                     
    q3 = - (0.1399 * eM * (math.cos (2.*Db*degtorad) - 0.0368 * math.cos (Db*degtorad)))    
    q4 =    0.0023 * eM * math.cos (MS*degtorad)                                               
    q5 = - 0.00015 * eM * math.cos (2.*FbM*degtorad)                                           
 
    rM = 385000.56 * (1. + q1 + q2 + q3 + q4 + q5)

    rhoM = 60. * (1737./rM) * radtodeg
    delM = 60. * (6371./rM) * radtodeg

    bMt = delM - rhoM - rhoS
    bM  = delM + rhoM - rhoS

    return bMt, bM

def Get_Lambda_Moon (t):
    """
    Takes Julian day number and returns lunar ecliptic longitude and latitude
    in degrees and minutes
    """

    labM = lb0M + nM  * (t - t0)
    MM   = M0M  + ntM * (t - t0)
    FbM  = F0M  + nbM * (t - t0)

    lamS, MS, rhoS = Get_Lambda_Sun (t)

    Db = labM - lamS

    q1 =   (2.*eM * math.sin (MM*degtorad) + 1.2379 * eM*eM * math.sin (2.*MM*degtorad)) * radtodeg
    q2 =   (0.4052 * eM * math.sin ((2.*Db-MM)*degtorad))                                * radtodeg
    q3 =   (0.2094 * eM * (math.sin (2.*Db*degtorad) - 0.0527 * math.sin (Db*degtorad))) * radtodeg
    q4 = -  0.0589 * eM * math.sin (MS*degtorad)                                         * radtodeg
    q5 = -  0.0364 * eM * math.sin (2.*FbM*degtorad)                                     * radtodeg
 
    lamM = labM + q1 + q2 + q3 + q4 + q5

    FM = FbM + q1 + q2 + q3 + q4 + q5

    betaM = 60. * math.asin (math.sin (5.128122*degtorad) * math.sin (FM*degtorad)) * radtodeg    

    bMt, bM = Get_R_Moon (t)

    mag = (bM - abs (betaM)) /(bM - bMt)

    return lamM, betaM, bM, bMt, mag

def Get_DMS (t):

    lamS, SM, rhoS           = Get_Lambda_Sun  (t)
    lamM, bsyz, bM, bMt, mag = Get_Lambda_Moon (t)

    D = lamM - lamS

    return D

def Get_D (tx, t):

    D0 = Get_DMS (tx)

    offset = math.atan2 (math.sin (D0*degtorad), math.cos (D0*degtorad)) * radtodeg
    
    return offset, offset + Get_DMS (tx + t) - Get_DMS (tx)

def Get_New_Moon (tx, i):

    off, D = Get_D (tx, 0.)

    #if off < 0:
    #    i -= 1
    target = 180.*(2.*i-1.)

    t = (target - D) /(nM - nS)

    for j in range (10):
        off, D  = Get_D (tx, t)
        t += (target - D) /(nM - nS)
        
    return t, abs(D)

yr   = input ("\nyear ? ")
year = int (yr)
tx   = julian_day_number (1, 1, year) * 1.0

f = open ("FullMoon.txt", "w")

print ("\n")
for i in range (1, 14):

    t, eps = Get_New_Moon (tx, i)

    jd = tx + t

    year, month, day, hour, minute = jd_to_gregorian_datetime (jd)
    lamM, bsyz, bM, bMt, mag       = Get_Lambda_Moon (jd)

    if abs (bsyz) < bMt:
        c = 'T'
    elif bMt < abs (bsyz) and abs (bsyz) < bM:
        c = 'P'
    else:
        c = ' '

    if (mag > 0.):    
        print ("%02d:  %02d/%02d/%4d:  %02d:%02d  %.1f  %.1f  %05.1f  %s  %.2f" % (i, day, month, year, hour, minute, bM, bMt, abs (bsyz), c, mag))
    else:
        print ("%02d:  %02d/%02d/%4d:  %02d:%02d  %.1f  %.1f  %05.1f  %s" % (i, day, month, year, hour, minute, bM, bMt, abs (bsyz), c))

    if (mag > 0.):
        print ("%02d/%02d/%4d &  %02d:%02d & %.1f & %.1f & %05.1f & %s & %.2f\\\\" % (day, month, year, hour, minute, bM, bMt, abs (bsyz), c, mag), file=f)
    else:
        print ("%02d/%02d/%4d &  %02d:%02d & %.1f & %.1f & %05.1f & %s &\\\\" % (day, month, year, hour, minute, bM, bMt, abs (bsyz), c), file=f)

print ("\n")

f.close ()
