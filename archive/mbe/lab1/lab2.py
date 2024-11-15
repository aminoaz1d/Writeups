#! /usr/bin/env python

PASS = "kw6PZq3Zd;ekR[_1"

o = ''.join([ chr(ord(j) ^ (i+1)) for i,j in enumerate(PASS) ])

print o