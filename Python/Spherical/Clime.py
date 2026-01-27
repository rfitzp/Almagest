# Script to list terrestrial climes in Earth's northern hemisphere

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

def day_fraction_to_hm(frac):
    """
    Convert fraction of a day to (hours, minutes),
    with minutes rounded to nearest integer.
    """

    total_minutes = round(frac * 24 * 60)

    hours = total_minutes // 60
    minutes = total_minutes % 60

    return hours, minutes

def year_fraction_to_days_hours(frac, days_in_year=365.25):
    """
    Convert fraction of a year to (days, hours),
    rounding hours to the nearest hour.
    
    Parameters:
        frac: fraction of a year (0..1)
        days_in_year: total days in the year (default 365)
    
    Returns:
        (days, hours) tuple, both integers
    """
    total_hours = frac * days_in_year * 24
    days = int(total_hours // 24)
    hours = int(round(total_hours % 24))

    # handle overflow (hours = 24 → add 1 day)
    if hours == 24:
        days += 1
        hours = 0

    return days, hours

# Set inclination of Ecliptic to equatiorial plane
epsilon = (23. + 26./60.) * degreetorad
sine    = math.sin (epsilon)
cose    = math.cos (epsilon)
tane    = sine /cose

with open("Clime.txt", "w") as f:

    # Loop over latitudes
    for L in range (0, 70, 5):

        Lat = L * degreetorad

        tanL = math.tan (Lat)

        SSday = 0.5 + math.asin (tanL * tane) /math.pi
        SSalt = math.pi/2. - abs (Lat - epsilon)

        if Lat > epsilon:
            sgn = 'S'
        else:
            sgn = 'N'

            EQalt = math.pi/2. - Lat
            
        WSalt = math.pi/2. - abs (Lat + epsilon)

        SSh, SSm = day_fraction_to_hm (SSday)
        SSd, SSs = rad_to_deg_min (SSalt)
        EQd, EQs = rad_to_deg_min (EQalt)
        WSd, WSs = rad_to_deg_min (WSalt)

        print ("%+03d°   %2dʰ%02dᵐ  %+03d°%02d′ %s  %+03d°%02d′ S  %+03d°%02d′ S" % (L, SSh, SSm, SSd, SSs, sgn, EQd, EQs, WSd, WSs), file=f)

    for L in range (70, 95, 5):

        Lat = L * degreetorad

        cosL = math.cos (Lat)

        SSday = 0.5 - math.asin (cosL / sine) /math.pi
        SSalt = math.pi/2. - abs (Lat - epsilon)

        if Lat > epsilon:
            sgn = 'S'
        else:
            sgn = 'N'

        EQalt = math.pi/2. - Lat

        WSalt = math.pi/2. - abs (Lat + epsilon)

        SSh, SSm = year_fraction_to_days_hours (SSday)
        SSd, SSs = rad_to_deg_min (SSalt)
        EQd, EQs = rad_to_deg_min (EQalt)
        WSd, WSs = rad_to_deg_min (WSalt)

        print ("%+03d°  %3dᵈ%02dʰ  %+03d°%02d′ %s  %+03d°%02d′ S  %+03d°%02d′ S" % (L, SSh, SSm, SSd, SSs, sgn, EQd, EQs, WSd, WSs), file=f)
    
