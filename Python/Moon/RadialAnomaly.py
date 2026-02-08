# Script to calculate radial lunar anomalies

import math

degtorad = math.pi/180.
radtodeg = 180./math.pi

eM = 0.054881

f = open ("RadialAnomaly.txt", "w")

def Get_Moon_Anomaly (arg):
      
    q1 = - (0.9894 * eM * math.cos (arg*degtorad) + 0.4915 * eM*eM * math.cos (2.*arg*degtorad)) 
    q2 = - (0.1751 * eM * math.cos (arg*degtorad))                                     
    q3 = - (0.1399 * eM * (math.cos (2.*arg*degtorad) - 0.0368 * math.cos (arg*degtorad)))    
    q4 =    0.0023 * eM * math.cos (arg*degtorad)                                               
    q5 = - 0.00015 * eM * math.cos (arg*degtorad)        
    
    return -100*q1, 100*q2, -100*q3, -100*q4, -100*q5

for arg in range (0, 92, 2):

    q1, q2, q3, q4, q5  = Get_Moon_Anomaly (arg)
    q6, q7, q8, q9, q10 = Get_Moon_Anomaly (90+arg)

    print ("%03d(%03d) & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$ & %03d(%03d) & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$ & $%+.3f$\\\\"
           % (arg, 360-arg, q1, q2, q3, q4, q5, 90+arg, 270-arg, q6, q7, q8, q9, q10), file=f)

f.close ()    
