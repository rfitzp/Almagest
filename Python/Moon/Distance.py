# Script to determine Earth-Moon distance

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

    lab = (lb0S + nS  * (t - t0)) % 360.
    M   = (M0S  + ntS * (t - t0)) % 360.

    labr = lab * degtorad
    Mr   = M   * degtorad

    qr   = 2.*eS * math.sin (Mr) + 1.25 * eS*eS * math.sin (2.*Mr)
    q    = qr * radtodeg

    lam  = lab + q

    if lam < 0.:
        lam += 360.

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

    return rM, delM, rhoM, rhoS

day, month, year, hour = map (int, input ("\nday month year hour ?? ").split())

t = julian_day_number (day, month, year) + (hour - 12) /24

rM, delM, rhoM, rhoS = Get_R_Moon (t)

print ("\nt-t0 = %.1f  R_M = %.2f km  del_M = %.3f′  rho_M = %.3f′  rho_S = %.3f′\n"
       % (t-t0, rM, delM, rhoM, rhoS))

