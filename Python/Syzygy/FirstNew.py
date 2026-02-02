# Script to determine first new moon in given year

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
rS0  = 15.99380

# Lunar parameters
eM   = 0.054881
nM   = 13.17639646
ntM  = 13.06499295
nbM  = 13.22935027
lb0M = 218.322
M0M  = 134.916
F0M  = 93.284
iM   = 5.161
dM0  = 56.98585
rM0  = 15.58795

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

    return lam, M

def Get_Lambda_Moon (t):
    """
    Takes Julian day number and returns lunar ecliptic longitude and latitude
    in degrees and minutes
    """

    labM = lb0M + nM  * (t - t0)
    MM   = M0M  + ntM * (t - t0)
    FbM  = F0M  + nbM * (t - t0)

    lamS, MS = Get_Lambda_Sun (t)

    Db = labM - lamS

    """
    q1 = (2.*eM * math.sin (MM*degtorad) + 1.430 * eM*eM * math.sin (2.*MM*degtorad)) * radtodeg
    q2 = (0.422 * eM * math.sin ((2.*Db - MM)*degtorad)) * radtodeg
    q3 = (0.211 * eM * (math.sin (2.*Db*degtorad) - 0.066 * math.sin (Db*degtorad))) * radtodeg
    q4 = - 0.051 * eM * math.sin (MS*degtorad) * radtodeg
    q5 = - 0.038 * eM * math.sin (2.*FbM*degtorad) * radtodeg
    """
    
    q1 =   (2.*eM * math.sin (MM*degtorad) + 1.2379 * eM*eM * math.sin (2.*MM*degtorad)) * radtodeg
    q2 =   (0.4052 * eM * math.sin ((2.*Db-MM)*degtorad))                                * radtodeg
    q3 =   (0.2094 * eM * (math.sin (2.*Db*degtorad) - 0.0527 * math.sin (Db*degtorad))) * radtodeg
    q4 = -  0.0589 * eM * math.sin (MS*degtorad)                                         * radtodeg
    q5 = -  0.0364 * eM * math.sin (2.*FbM*degtorad)                                     * radtodeg

    lamM = labM + q1 + q2 + q3 + q4 + q5

    FM = FbM + q1 + q2 + q3 + q4 + q5

    betaM = math.asin (math.sin (iM*degtorad) * math.sin (FM*degtorad)) * radtodeg

    db1 = dM0 * eM * math.cos (MM*degtorad)
    db2 = rM0 * eM * math.cos (MM*degtorad)
    db3 = rS0 * eS * math.cos (MM*degtorad)

    bS  = 88.57 + db1 + db2 + db3
    bSt = 56.59 + db1 + db2 - db3
    bSa = 57.39 + db1 - db2 + db3

    return lamM, betaM*60., bS, bSt, bSa

def Get_DMS (t):

    lamS, SM                 = Get_Lambda_Sun  (t)
    lamM, bsyz, bS, bSt, bSa = Get_Lambda_Moon (t)

    D = lamM - lamS

    return D

def Get_D (tx, t):

    D0 = Get_DMS (tx)

    offset = math.atan2 (math.sin (D0*degtorad), math.cos (D0*degtorad)) * radtodeg
    
    return offset, offset + Get_DMS (tx + t) - Get_DMS (tx)

def Get_New_Moon (tx, i):

    off, D = Get_D (tx, 0.)

    if off < 0:
        i -= 1
    target = 360.*i

    t = (target - D) /(nM - nS)

    for j in range (10):
        off, D  = Get_D (tx, t)
        t += (target - D) /(nM - nS)
        
    return t, abs(D)

f = open ("First.txt", "w")

for cnt in range (0, 50):
    
    year1    = 1900 + cnt
    tx1      = julian_day_number (1, 1, year1) * 1.0
    t1, eps1 = Get_New_Moon (tx1, 1)
    jd1      = tx1 + t1
    
    year2    = 1950 + cnt
    tx2      = julian_day_number (1, 1, year2) * 1.0
    t2, eps2 = Get_New_Moon (tx2, 1)
    jd2      = tx2 + t2

    year3    = 2000 + cnt
    tx3      = julian_day_number (1, 1, year3) * 1.0
    t3, eps3 = Get_New_Moon (tx3, 1)
    jd3      = tx3 + t3

    year4    = 2050 + cnt
    tx4      = julian_day_number (1, 1, year4) * 1.0
    t4, eps4 = Get_New_Moon (tx4, 1)
    jd4      = tx4 + t4
  
    year1, month1, day1, hour1, minute1 = jd_to_gregorian_datetime (jd1)
    year2, month2, day2, hour2, minute2 = jd_to_gregorian_datetime (jd2)
    year3, month3, day3, hour3, minute3 = jd_to_gregorian_datetime (jd3)
    year4, month4, day4, hour4, minute4 = jd_to_gregorian_datetime (jd4)
    
    print ("%02d/%02d/%4d %.2f %02d/%02d/%4d %.2f %02d/%02d/%4d %.2f %02d/%02d/%4d %.2f"
           % (day1, month1, year1, jd1, day2, month2, year2, jd2, day3, month3, year3, jd3, day4, month4, year4, jd4))

    print ("%02d/%02d/%4d &  %.2f &  %02d/%02d/%4d &  %.2f & %02d/%02d/%4d &  %.2f %02d/%02d/%4d & %.2f\\\\"
           % (day1, month1, year1, jd1, day2, month2, year2, jd2, day3, month3, year3, jd3, day4, month4, year4, jd4), file=f)
    
f.close()
