# Script to calculate solar ecliptic longitude

import math

n   = 0.98564735
nt  = 0.98560025
lb0 = 280.458
M0  = 357.588
t0  = 2451545.0
e   = 0.016711
yr  = 360./n

degtorad = math.pi/180.
radtodeg = 180./math.pi

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

def Get_Lambda (t):
    """
    Takes Julian day number and returns solar longitude
    in degrees and minutes
    """

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

    return deg, min

tVE = t0 + 78.81
tSS = t0 + 171.58
tAE = t0 + 265.22
tWS = t0 + 355.06

dVE, mVE = Get_Lambda (tVE)
dSS, mSS = Get_Lambda (tSS)
dAE, mAE = Get_Lambda (tAE)
dWS, mWS = Get_Lambda (tWS)

print ("\nVernal Equinox  : t-t0 =  %.2f lambda = %03d°%02d′" %(tVE-t0, dVE, mVE))
print (  "Summer Solstice : t-t0 = %.2f lambda = %03d°%02d′" %(tSS-t0, dSS, mSS))
print (  "Autumnal Equinox: t-t0 = %.2f lambda = %03d°%02d′" %(tAE-t0, dAE, mAE))
print (  "Winter Solstice : t-t0 = %.2f lambda = %03d°%02d′" %(tWS-t0, dWS, mWS))

print ("\nSpring = %.2f Summer = %.2f Autumn = %.2f Winter = %.2f\n" % (tSS-tVE, tAE-tSS, tWS-tAE, yr-tWS+tVE))
