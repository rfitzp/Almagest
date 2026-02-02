# Script to calculate lunar parallax table

import math

degtorad = math.pi/180.
radtodeg = 180./math.pi

# Lunar parameters
i  = 5.161
eM = 0.054881

f = open("Parallax.txt", "w")

for arg in range (0, 92, 2):

    delta = 56.98   * math.cos (arg*degtorad)
    zeta  = 100.*eM * math.cos (arg*degtorad)

    print ("%03d/%03d %06.3f %05.3f  (%03d)/(%03d)" % (arg, 180-arg, delta, zeta, 180+arg, 360-arg))

    print ("%03d/%03d & $%06.3f$ & $%05.3f$ & (%03d)/(%03d)\\\\" % (arg, 180-arg, delta, zeta, 180+arg, 360-arg), file=f)

f.close()    
