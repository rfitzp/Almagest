# Script to output equation of time table

import math

degreetorad = math.pi /180.
radtodegree = 180. /math.pi

e       = 0.016711
epsilon = (23. + 26./60.) * degreetorad

def min_to_minsec(minutes):
    """
    Convert fractional minutes to (minutes, seconds).
    Seconds rounded to nearest integer.
    Sign is carried by minutes.
    """

    sign = -1 if minutes < 0 else 1
    minutes = abs(minutes)

    m = int(minutes)
    s = round((minutes - m) * 60)

    # handle rounding overflow (e.g., 59.9 -> 60)
    if s == 60:
        m += 1
        s = 0

    m *= sign

    return m, s

def Get_Deltat (lam):

    lamr = lam * degreetorad

    M  = lam + 77.213
    Mr = M * degreetorad
    
    Delta = lamr - math.atan2 (math.cos(epsilon) * math.sin(lamr), math.cos(lamr)) - 2.*e * math.sin (Mr)

    Deltad = Delta * radtodegree

    if Deltad > 180.:
        Deltad -= 360.

    Deltat = 60. * Deltad /15.

    mn, sec = min_to_minsec (Deltat)

    return mn, sec

# Loop over signs of Zodiac

print ("\n")
for sign in range (12):

    # Loop over degrees in sign
    for deg in range (0, 32, 2):
        
        lam = 30.*sign + deg

        mn, sc = Get_Deltat (lam)

        print ("%02d  %+03dᵐ%02dˢ" % (deg, mn, sc))

    print ("\n")
