# Script to calculate altitude and parallactic angle of points on ecliptic circle

import math

degreetorad = math.pi /180.
radtodegree = 180. /math.pi

def rad_to_deg_min(theta):
    """
    Convert angle in radians to (degrees, minutes),
    with minutes rounded to nearest integer.
    Returns (deg, min).
    """

    # Convert to total degrees
    total_deg = math.degrees(theta)

    # Separate degrees and fractional part
    deg  = int(math.floor(total_deg)) if total_deg >= 0 else int(math.ceil(total_deg))
    frac = abs(total_deg - deg)

    # Minutes
    minutes = round(frac * 60)

    # Handle rounding overflow (e.g., 59.6 -> 60)
    if minutes == 60:
        deg += 1 if total_deg >= 0 else -1
        minutes = 0

    return deg, minutes

def frac_hours_to_hm(t):
    """
    Convert fractional hours to (hours, minutes),
    rounding minutes to nearest integer.

    Works for positive or negative values.

    Example:
        2.25  -> (2,  15)
       -1.75  -> (-1, 45)
    """

    total_minutes = round(t * 60)

    hours   = int(total_minutes // 60)
    minutes = abs(total_minutes % 60)

    return hours, minutes

# Set inclination of Ecliptic to equatiorial plane
epsilon = (23. + 26./60.) * degreetorad
sine    = math.sin (epsilon)
cose    = math.cos (epsilon)
tane    = math.tan (epsilon)

# Set latitude
f = open("Altitude80.txt", "w")

L    = 80. * degreetorad
cosL = math.cos (L)
sinL = math.sin (L)
tanL = math.tan (L)

# Loop over zodiacal signs
for sign in range (12):

    lam = 30. * sign * degreetorad

    sinl = math.sin (lam)
    cosl = math.cos (lam)

    dlt = math.asin (sine * sinl)
    alp = math.atan2 (cose * sinl, cosl)
    
    sind = math.sin (dlt)
    cosd = math.cos (dlt)
    tand = math.tan (dlt)

    # Loop over hours
    for t in range (13):
        
        trad = 15. * t * degreetorad + 1.e-15
        
        cost = math.cos (trad)
        sint = math.sin (trad)
        
        alt = math.asin (sinL * sind + cosL * cosd * cost)
  
        if alt > -1.e-8:

            azmp = math.atan2 (  cosd * sint, cosL * sind - sinL * cosd * cost)
            azmm = math.atan2 (- cosd * sint, cosL * sind - sinL * cosd * cost)
        
            cosAp = math.cos (azmp)
            sinAp = math.sin (azmp)

            cosAm = math.cos (azmm)
            sinAm = math.sin (azmm)
        
            cosatp = math.cos (alp - trad)
            sinatp = math.sin (alp - trad)
            
            cosatm = math.cos (alp + trad)
            sinatm = math.sin (alp + trad)
            
            mup = math.acos (- cosAp * sine * cosatp - sinAp * (cosL * cose + sinL * sine * sinatp))
            mum = math.acos (- cosAm * sine * cosatm - sinAm * (cosL * cose + sinL * sine * sinatm))
            
            zqp = sinL * cose - cosL * sine * sinatp
            zqm = sinL * cose - cosL * sine * sinatm
            
            if zqp < 0.:
                mup = 2.*math.pi - mup
            if zqm < 0.:
                mum = 2.*math.pi - mum
                    
            altd, altm = rad_to_deg_min (alt)
            mupd, mupm = rad_to_deg_min (mup)
            mumd, mumm = rad_to_deg_min (mum)
                    
            print ("%02d:%02d  %02d°%02d′  %03d°%02d′  %03d°%02d′" % (t, 0, altd, altm, mupd, mupm, mumd, mumm))

            print ("%02d:%02d & $%02d^\circ %02d'$ & $%03d^\circ %02d'$ & $%03d^\circ %02d'$\\\\" % (t, 0, altd, altm, mupd, mupm, mumd, mumm), file=f)

    # Calculate quantities at zero altitude         
    if abs (tanL * tand) < 1.:

        thrad = math.acos (- tanL * tand)
        th    = thrad /(15. * degreetorad)
        
        cost = math.cos (thrad)
        sint = math.sin (thrad)
        
        alt = math.asin (sinL * sind + cosL * cosd * cost)
        
        azmp = math.atan2 (  cosd * sint, cosL * sind - sinL * cosd * cost)
        azmm = math.atan2 (- cosd * sint, cosL * sind - sinL * cosd * cost)
        
        cosAp = math.cos (azmp)
        sinAp = math.sin (azmp)

        cosAm = math.cos (azmm)
        sinAm = math.sin (azmm)
        
        cosatp = math.cos (alp - thrad)
        sinatp = math.sin (alp - thrad)
        
        cosatm = math.cos (alp + thrad)
        sinatm = math.sin (alp + thrad)
        
        mup = math.acos (- cosAp * sine * cosatp - sinAp * (cosL * cose + sinL * sine * sinatp))
        mum = math.acos (- cosAm * sine * cosatm - sinAm * (cosL * cose + sinL * sine * sinatm))
        
        zqp = sinL * cose - cosL * sine * sinatp
        zqm = sinL * cose - cosL * sine * sinatm
        
        if zqp < 0.:
            mup = 2.*math.pi - mup
        if zqm < 0.:
            mum = 2.*math.pi - mum
                    
        altd, altm = rad_to_deg_min (alt)
        mupd, mupm = rad_to_deg_min (mup)
        mumd, mumm = rad_to_deg_min (mum)
                  
        thh, thm = frac_hours_to_hm (th)
                  
        print ("%02d:%02d  %02d°%02d′  %03d°%02d′  %03d°%02d′" % (thh, thm, altd, altm, mupd, mupm, mumd, mumm))

        print ("%02d:%02d & $%02d^\circ %02d'$ & $%03d^\circ %02d'$ & $%03d^\circ %02d'$\\\\" % (thh, thm, altd, altm, mupd, mupm, mumd, mumm), file=f)

    print ("\n")
    print ("\n", file=f)

f.close ()    
