#! /usr/bin/env python

last_name = raw_input("Last name: ")  
length = len(last_name)
serial = 0

"""
for index, character in enumerate(last_name):
    c1 = last_name[ (index - 1) % length ]
    c2 = last_name[index]
    i1 = ord(c1)
    i2 = ord(c2)
    
    print "%c ^ %c || %d ^ %d" % (c1,c2, i1, i2)
    serial += i1 ^ i2
    
print serial
"""

serial = 0
index = 0

while(True):
    if length <= index:
        break
        
    uint_dec_index = (index - 1) & 0xffffffff #simulate unsigned int from strlen
    c1 = last_name[ (uint_dec_index) % length ]
    c2 = last_name[index]
    i1 = ord(c1)
    i2 = ord(c2)
    
    print "%c ^ %c || %d ^ %d" % (c1,c2, i1, i2)
    serial = i1 ^ (i2 + serial) #addition has priority over XOR
    index += 1

print serial