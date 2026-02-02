# Script to calculate lunar anomalies

import math

degtorad = math.pi/180.
radtodeg = 180./math.pi

eM   = 0.054881

f = open ("Anomaly.txt", "w")

def Get_Moon_Anomaly (arg):
   
    
    q1 =   (2.*eM * math.sin (arg*degtorad) + 1.2379 * eM*eM * math.sin (2.*arg*degtorad)) * radtodeg
    q2 =   (0.4052 * eM * math.sin (arg*degtorad))                                         * radtodeg
    q3 =   (0.2094 * eM * (math.sin (2.*arg*degtorad) - 0.0527 * math.sin (arg*degtorad))) * radtodeg
    q4 = -  0.0589 * eM * math.sin (arg*degtorad)                                          * radtodeg
    q5 = -  0.0364 * eM * math.sin (arg*degtorad)                                          * radtodeg

    return q1, q2, q3, q4, q5

for arg in range (0, 92, 2):

    q1, q2, q3, q4, q5  = Get_Moon_Anomaly (arg)
    q6, q7, q8, q9, q10 = Get_Moon_Anomaly (90+arg)

    print ("%03d(%03d) & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$ & %03d(%03d) & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$\\\\"
           % (arg, 360-arg, q1, q2, q3, q4, q5, 90+arg, 270-arg, q6, q7, q8, q9, q10), file=f)

f.close ()    
