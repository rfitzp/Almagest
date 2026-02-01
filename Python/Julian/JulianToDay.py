def jd_to_gregorian(jd):
    """
    Convert Julian Day Number (integer) to Gregorian date.
    Returns (year, month, day).
    """

    l = jd + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    day = l - (2447 * j) // 80
    l = j // 11
    month = j + 2 - 12 * l
    year = 100 * (n - 49) + i + l

    return year, month, day

julian = input ("\nJulian day number ?? ")

jd = int (julian)

year, month, day = jd_to_gregorian (jd)

print ("\nJulian day %d is %02d/%02d/%4d \n" % (jd, day, month, year))
    
