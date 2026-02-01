# Script to calculate solar ecliptic longitude

import math

n   = 0.98564735
nt  = 0.98560025
lb0 = 280.458
M0  = 357.588
t0  = 2451545.0
e   = 0.016711

degtorad = math.pi/180.
radtodeg = 180./math.pi

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

day, month, year, hour = map (int, input ("\nday month year hour ?? ").split())

t = julian_day_number (day, month, year) + (hour - 12) /24

lab = (lb0 + n  * (t - t0)) % 360.
M   = (M0  + nt * (t - t0)) % 360.

labr = lab * degtorad
Mr   = M   * degtorad

qr   = 2.*e * math.sin (Mr) + 1.25 * e*e * math.sin (2.*Mr)
q    = qr * radtodeg

lam  = lab + q

if lam < 0.:
    lam += 360.

deg, min = deg_to_degmin (lam)    

print ("\nt = %.1f lambda_bar = %.3f M = %.3f q = %.3f lambda = %.3f = %03d°%02d′\n" % (t, lab, M, q, lam, deg, min))
