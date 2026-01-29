# Script to output ecliptic ascensions at various terrestrial latitudes

import math

degreetorad = math.pi /180.
radtodegree = 180. /math.pi

def rad_to_deg_min(theta):
    """
    Convert angle in radians to (degrees, minutes),
    with minutes rounded to nearest integer.
    Returns (deg, min).
    """

    # convert to total degrees
    total_deg = math.degrees(theta)

    # separate degrees and fractional part
    deg = int(math.floor(total_deg)) if total_deg >= 0 else int(math.ceil(total_deg))
    frac = abs(total_deg - deg)

    # minutes
    minutes = round(frac * 60)

    # handle rounding overflow (e.g., 59.6 -> 60)
    if minutes == 60:
        deg += 1 if total_deg >= 0 else -1
        minutes = 0

    return deg, minutes

# Set inclination of Ecliptic to equatiorial plane
epsilon = (23. + 26./60.) * degreetorad
sine    = math.sin (epsilon)
cose    = math.cos (epsilon)
tane    = math.tan (epsilon)

with open("Ascension85.txt", "w") as f:

    # Latitude 
    L    = 85. * degreetorad
    tanL = math.tan (L)

    # Range over ecliptic latitude
    for degree in range (0, 32, 2):

        lam1 = (0.   + degree) * degreetorad
        lam2 = (30.  + degree) * degreetorad
        lam3 = (60.  + degree) * degreetorad
        lam4 = (90.  + degree) * degreetorad
        lam5 = (120. + degree) * degreetorad
        lam6 = (150. + degree) * degreetorad

        sinl1 = math.sin (lam1)
        sinl2 = math.sin (lam2)
        sinl3 = math.sin (lam3)
        sinl4 = math.sin (lam4)
        sinl5 = math.sin (lam5)
        sinl6 = math.sin (lam6)

        tanl1 = math.tan (lam1)
        tanl2 = math.tan (lam2)
        tanl3 = math.tan (lam3)
        tanl4 = math.tan (lam4)
        tanl5 = math.tan (lam5)
        tanl6 = math.tan (lam6)

        f1 = tanl1 * cose
        f2 = tanl2 * cose
        f3 = tanl3 * cose
        f4 = tanl4 * cose
        f5 = tanl5 * cose
        f6 = tanl6 * cose

        g1 = sinl1 * sine * tanL / math.sqrt (1. - sinl1*sinl1 * sine*sine)
        g2 = sinl2 * sine * tanL / math.sqrt (1. - sinl2*sinl2 * sine*sine)
        g3 = sinl3 * sine * tanL / math.sqrt (1. - sinl3*sinl3 * sine*sine)
        g4 = sinl4 * sine * tanL / math.sqrt (1. - sinl4*sinl4 * sine*sine)
        g5 = sinl5 * sine * tanL / math.sqrt (1. - sinl5*sinl5 * sine*sine)
        g6 = sinl6 * sine * tanL / math.sqrt (1. - sinl6*sinl6 * sine*sine)

        if abs(g1) < 1.:
            alpha1 = math.atan (f1) - math.asin (g1)
        else:
            alpha1 = 0.
        if abs(g2) < 1.:
            alpha2 = math.atan (f2) - math.asin (g2)
        else:
            alpha2 = 0.
        if abs(g3) < 1.:
            alpha3 = math.atan (f3) - math.asin (g3)
        else:
            alpha3 = 0.
        if abs(g4) < 1.:
            alpha4 = math.atan (f4) - math.asin (g4)
        else:
            alpha4 = 0.
        if abs(g5) < 1.:
            alpha5 = math.atan (f5) - math.asin (g5)
        else:
            alpha5 = 0.
        if abs(g6) < 1.:
            alpha6 = math.atan (f6) - math.asin (g6)
        else:
            alpha6 = 0.

        if alpha1 < 0.:
            alpha1 += 2.*math.pi
        if alpha2 < 0.:
           alpha2 += 2.*math.pi       
        if alpha4 < 0.:
            alpha4 += math.pi
        if alpha5 < 0.:
            alpha5 += math.pi
        if alpha6 < 0.:
            alpha6 += math.pi   
  
        deg1, min1 = rad_to_deg_min (alpha1)
        deg2, min2 = rad_to_deg_min (alpha2)
        deg3, min3 = rad_to_deg_min (alpha3)
        deg4, min4 = rad_to_deg_min (alpha4)
        deg5, min5 = rad_to_deg_min (alpha5)
        deg6, min6 = rad_to_deg_min (alpha6)

        print ("%02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′"
               % (degree, deg1, min1, degree, deg2, min2, degree, deg3, min3, degree, deg4, min4, degree, deg5, min5, degree, deg6, min6), file=f)

    print ("\n", file=f)    

    for degree in range (0, 32, 2):

        lam1 = (180. + degree) * degreetorad
        lam2 = (210. + degree) * degreetorad
        lam3 = (240. + degree) * degreetorad
        lam4 = (270. + degree) * degreetorad
        lam5 = (300. + degree) * degreetorad
        lam6 = (330. + degree) * degreetorad
        
        sinl1 = math.sin (lam1)
        sinl2 = math.sin (lam2)
        sinl3 = math.sin (lam3)
        sinl4 = math.sin (lam4)
        sinl5 = math.sin (lam5)
        sinl6 = math.sin (lam6)
        
        tanl1 = math.tan (lam1)
        tanl2 = math.tan (lam2)
        tanl3 = math.tan (lam3)
        tanl4 = math.tan (lam4)
        tanl5 = math.tan (lam5)
        tanl6 = math.tan (lam6)
        
        f1 = tanl1 * cose
        f2 = tanl2 * cose
        f3 = tanl3 * cose
        f4 = tanl4 * cose
        f5 = tanl5 * cose
        f6 = tanl6 * cose
        
        g1 = sinl1 * sine * tanL / math.sqrt (1. - sinl1*sinl1 * sine*sine)
        g2 = sinl2 * sine * tanL / math.sqrt (1. - sinl2*sinl2 * sine*sine)
        g3 = sinl3 * sine * tanL / math.sqrt (1. - sinl3*sinl3 * sine*sine)
        g4 = sinl4 * sine * tanL / math.sqrt (1. - sinl4*sinl4 * sine*sine)
        g5 = sinl5 * sine * tanL / math.sqrt (1. - sinl5*sinl5 * sine*sine)
        g6 = sinl6 * sine * tanL / math.sqrt (1. - sinl6*sinl6 * sine*sine)

        if abs(g1) < 1.:
            alpha1 = math.atan (f1) - math.asin (g1)
        else:
            alpha1 = 0.
        if abs(g2) < 1.:
            alpha2 = math.atan (f2) - math.asin (g2)
        else:
            alpha2 = 0.
        if abs(g3) < 1.:
            alpha3 = math.atan (f3) - math.asin (g3)
        else:
            alpha3 = 0.
        if abs(g4) < 1.:
            alpha4 = math.atan (f4) - math.asin (g4)
        else:
            alpha4 = 0.
        if abs(g5) < 1.:
            alpha5 = math.atan (f5) - math.asin (g5)
        else:
            alpha5 = 0.
        if abs(g6) < 1.:
            alpha6 = math.atan (f6) - math.asin (g6)
        else:
            alpha6 = 0.

        if alpha4 < 0.:
            alpha4 += math.pi
        if alpha5 < 0.:
            alpha5 += math.pi
        if alpha6 < 0.:
            alpha6 += math.pi

        alpha5 -= math.pi
        alpha6 -= math.pi

        alpha1 += math.pi
        alpha2 += math.pi
        alpha3 += math.pi
        alpha4 += math.pi
        alpha5 += math.pi
        alpha6 += math.pi  
  
        deg1, min1 = rad_to_deg_min (alpha1)
        deg2, min2 = rad_to_deg_min (alpha2)
        deg3, min3 = rad_to_deg_min (alpha3)
        deg4, min4 = rad_to_deg_min (alpha4)
        deg5, min5 = rad_to_deg_min (alpha5)
        deg6, min6 = rad_to_deg_min (alpha6)

        print ("%02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′  %02d°  %03d°%02d′"
               % (degree, deg1, min1, degree, deg2, min2, degree, deg3, min3, degree, deg4, min4, degree, deg5, min5, degree, deg6, min6), file=f)
   
cosL = math.cos (L)

h = cosL/sine
x = 1. /tanL/tane

if abs(h) < 1.:

    lambdac = math.asin (h)
    alphac  = math.acos (x)

    deg, mnt = rad_to_deg_min (lambdac)
    dex, mnx = rad_to_deg_min (alphac)

    print ("%03d°%02d′ %03d°%02d′  %03d°%02d′ %03d°%02d′" % (deg, mnt, 360-dex-1, 60-mnx, 30-deg-1, 60-mnt, dex, mnx))
