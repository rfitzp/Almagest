# Script to calculate angular size of Sun

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

day, month, year, hour = map (int, input ("\nday month year hour ?? ").split())

t = julian_day_number (day, month, year) + (hour - 12) /24

M  = (M0  + nt * (t - t0)) % 360.
Mr = M * degtorad

r = 1. - e * math.cos (Mr) + e*e * math.sin (Mr) * math.sin (Mr)

S = 15.987 * (1. + e * math.cos (Mr) + e*e * math.cos (2.*Mr))

print ("\nt = %.1f  M = %.3f  r = %.5f  S = %.3f′\n" % (t, M, r, S))

with open ("Angular.txt", "w") as f:

    for deg in range (46):

        deg1 = deg
        deg2 = deg + 25
        deg3 = deg + 90
        deg4 = deg + 135

        M1 = deg1 * degtorad
        M2 = deg2 * degtorad
        M3 = deg3 * degtorad
        M4 = deg4 * degtorad

        S1 = 15.987 * (1. + e * math.cos (M1) + e*e * math.cos (2.*M1))
        S2 = 15.987 * (1. + e * math.cos (M2) + e*e * math.cos (2.*M2))
        S3 = 15.987 * (1. + e * math.cos (M3) + e*e * math.cos (2.*M3))
        S4 = 15.987 * (1. + e * math.cos (M4) + e*e * math.cos (2.*M4))

        print ("%03d/%03d & %0.3f & %03d/%03d & %0.3f & %03d/%03d & %0.3f & %03d/%03d & %0.3f\\\\"
               % (deg1, 360-deg1, S1, deg2, 360-deg2, S2, deg3, 360-deg3, S3, deg4, 360-deg4, S4), file=f)
