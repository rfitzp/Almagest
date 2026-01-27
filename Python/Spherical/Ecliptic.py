# Script to output declinations and right ascensions of points on the ecliptic circle

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

with open("Ecliptic.txt", "w") as f:

    # Loop over degrees
    for degree in range (0, 32, 2):
        
        lam1 = (00. + degree) * degreetorad
        lam2 = (30. + degree) * degreetorad
        lam3 = (60. + degree) * degreetorad
        
        cosl1 = math.cos (lam1)
        cosl2 = math.cos (lam2)
        cosl3 = math.cos (lam3)
        
        sinl1 = math.sin (lam1)
        sinl2 = math.sin (lam2)
        sinl3 = math.sin (lam3)
        
        sind1 = sine * sinl1
        sind2 = sine * sinl2
        sind3 = sine * sinl3
        
        sina1 = cose * sinl1
        sina2 = cose * sinl2
        sina3 = cose * sinl3
        
        delta1 = math.asin (sind1)
        delta2 = math.asin (sind2)
        delta3 = math.asin (sind3)
        
        alpha1 = math.atan2 (sina1, cosl1)
        alpha2 = math.atan2 (sina2, cosl2)
        alpha3 = math.atan2 (sina3, cosl3)
        
        degd1, mind1 = rad_to_deg_min (delta1)
        degd2, mind2 = rad_to_deg_min (delta2)
        degd3, mind3 = rad_to_deg_min (delta3)
        
        dega1, mina1 = rad_to_deg_min (alpha1)
        dega2, mina2 = rad_to_deg_min (alpha2)
        dega3, mina3 = rad_to_deg_min (alpha3)
        
        print ("%+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′"
               % (degree, degd1, mind1, dega1, mina1, degree, degd2, mind2, dega2, mina2, degree, degd3, mind3, dega3, mina3), file=f)

    print ("\n", file=f)

    for degree in range (0, 32, 2):

        lam1 = (90.  + degree) * degreetorad
        lam2 = (120. + degree) * degreetorad
        lam3 = (150. + degree) * degreetorad
        
        cosl1 = math.cos (lam1)
        cosl2 = math.cos (lam2)
        cosl3 = math.cos (lam3)
        
        sinl1 = math.sin (lam1)
        sinl2 = math.sin (lam2)
        sinl3 = math.sin (lam3)
        
        sind1 = sine * sinl1
        sind2 = sine * sinl2
        sind3 = sine * sinl3
        
        sina1 = cose * sinl1
        sina2 = cose * sinl2
        sina3 = cose * sinl3
        
        delta1 = math.asin (sind1)
        delta2 = math.asin (sind2)
        delta3 = math.asin (sind3)
        
        alpha1 = math.atan2 (sina1, cosl1)
        alpha2 = math.atan2 (sina2, cosl2)
        alpha3 = math.atan2 (sina3, cosl3)
        
        degd1, mind1 = rad_to_deg_min (delta1)
        degd2, mind2 = rad_to_deg_min (delta2)
        degd3, mind3 = rad_to_deg_min (delta3)
        
        dega1, mina1 = rad_to_deg_min (alpha1)
        dega2, mina2 = rad_to_deg_min (alpha2)
        dega3, mina3 = rad_to_deg_min (alpha3)
        
        print ("%+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′"
               % (degree, degd1, mind1, dega1, mina1, degree, degd2, mind2, dega2, mina2, degree, degd3, mind3, dega3, mina3), file=f)

    print ("\n", file=f)

    for degree in range (0, 32, 2):

        lam1 = (180. + degree) * degreetorad
        lam2 = (210. + degree) * degreetorad
        lam3 = (240. + degree) * degreetorad
    
        cosl1 = math.cos (lam1)
        cosl2 = math.cos (lam2)
        cosl3 = math.cos (lam3)

        sinl1 = math.sin (lam1)
        sinl2 = math.sin (lam2)
        sinl3 = math.sin (lam3)
    
        sind1 = sine * sinl1
        sind2 = sine * sinl2
        sind3 = sine * sinl3
        
        sina1 = cose * sinl1
        sina2 = cose * sinl2
        sina3 = cose * sinl3
        
        delta1 = math.asin (sind1)
        delta2 = math.asin (sind2)
        delta3 = math.asin (sind3)
        
        alpha1 = math.atan2 (sina1, cosl1)
        alpha2 = math.atan2 (sina2, cosl2)
        alpha3 = math.atan2 (sina3, cosl3)
        
        if alpha1 < 0.:
            alpha1 += 2.*math.pi
        if alpha2 < 0.:
            alpha2 += 2.*math.pi
        if alpha3 < 0.:
            alpha3 += 2.*math.pi
    
        degd1, mind1 = rad_to_deg_min (delta1)
        degd2, mind2 = rad_to_deg_min (delta2)
        degd3, mind3 = rad_to_deg_min (delta3)
    
        dega1, mina1 = rad_to_deg_min (alpha1)
        dega2, mina2 = rad_to_deg_min (alpha2)
        dega3, mina3 = rad_to_deg_min (alpha3)
    
        print ("%+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′"
               % (degree, degd1, mind1, dega1, mina1, degree, degd2, mind2, dega2, mina2, degree, degd3, mind3, dega3, mina3), file=f)
    
    print ("\n", file=f)

    for degree in range (0, 32, 2):

        lam1 = (270. + degree) * degreetorad
        lam2 = (300. + degree) * degreetorad
        lam3 = (330. + degree) * degreetorad
        
        cosl1 = math.cos (lam1)
        cosl2 = math.cos (lam2)
        cosl3 = math.cos (lam3)
        
        sinl1 = math.sin (lam1)
        sinl2 = math.sin (lam2)
        sinl3 = math.sin (lam3)
        
        sind1 = sine * sinl1
        sind2 = sine * sinl2
        sind3 = sine * sinl3
        
        sina1 = cose * sinl1
        sina2 = cose * sinl2
        sina3 = cose * sinl3
        
        delta1 = math.asin (sind1)
        delta2 = math.asin (sind2)
        delta3 = math.asin (sind3)
        
        alpha1 = math.atan2 (sina1, cosl1)
        alpha2 = math.atan2 (sina2, cosl2)
        alpha3 = math.atan2 (sina3, cosl3)
        
        if alpha1 < 0.:
            alpha1 += 2.*math.pi
        if alpha2 < 0.:
            alpha2 += 2.*math.pi
        if alpha3 < 0.:
            alpha3 += 2.*math.pi
    
        degd1, mind1 = rad_to_deg_min (delta1)
        degd2, mind2 = rad_to_deg_min (delta2)
        degd3, mind3 = rad_to_deg_min (delta3)
        
        dega1, mina1 = rad_to_deg_min (alpha1)
        dega2, mina2 = rad_to_deg_min (alpha2)
        dega3, mina3 = rad_to_deg_min (alpha3)
        
        print ("%+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′  %+03d°  %+03d°%02d′  %03d°%02d′"
               % (degree, degd1, mind1, dega1, mina1, degree, degd2, mind2, dega2, mina2, degree, degd3, mind3, dega3, mina3), file=f)
    
        
