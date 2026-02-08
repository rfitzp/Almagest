# Script to calculate lunar latitude anomaly

import math

degtorad = math.pi/180.
radtodeg = 180./math.pi

i = 5.128122

f = open("Latitude.txt", "w")

for arg in range (0, 92, 2):

    beta = math.asin (math.sin (i*degtorad) * math.sin (arg*degtorad)) * radtodeg

    print ("%03d/%03d %.3f (%03d)/(%03d)" % (arg, 180-arg, beta, 180+arg, 360-arg))

    print ("%03d/%03d & $%.3f$ & (%03d)/(%03d)\\\\" % (arg, 180-arg, beta, 180+arg, 360-arg), file=f)

f.close()    
