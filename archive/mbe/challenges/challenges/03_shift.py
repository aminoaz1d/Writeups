#! /usr/bin/env python

def shift(param_1):
    res = ""
    for c in param_1:
        res += chr(ord(c) - 3)
    return res
    
print shift("Sdvvzrug#RN$$$#=,")
print shift("Lqydolg#Sdvvzrug$")