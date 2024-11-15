#! /usr/bin/env python

username = raw_input("Username: ")
#serial = raw_input("Serial: ")

LEN_EDX_EAX = 64
MASK32 = 0xffffffff
MASK_EDX_FROM_MUL = 0xffffffff00000000

if len(username) <= 5:
    print "username too short"
    #exit()
    
seed = (ord(username[3]) ^ 0x1337) + 0x5eeded

print "seed: " + hex(seed) + " %d" % seed

for i in xrange(0, len(username)):
    print username[i]
    print "beginseed: %d" % seed
    ecx = ord(username[i]) ^ seed
    
    
    # MUL
    edx_eax = ecx * 0x88233b2b
    '''
    print edx_eax
    bin_edx_eax = bin(edx_eax)[2:]
    bin_edx_eax = ('0' * (LEN_EDX_EAX - len(bin(edx_eax)[2:]))) + bin_edx_eax
    print "conv: %d" % int(bin_edx_eax, 2)
    
    edx = bin_edx_eax[:32]
    eax = bin_edx_eax[32:]
    print bin_edx_eax
    print edx + eax
    edx = int(edx, 2)
    eax = int(eax, 2)
    
    print "edx check"
    print bin(edx)
    print bin((edx_eax & MASK_EDX_FROM_MUL) >> 32)
    '''
    edx = (edx_eax & MASK_EDX_FROM_MUL) >> 32
    
    eax = ecx
    
    # SUB
    eax = (eax - edx) & MASK32
    
    # SHR
    eax = eax >> 1
    
    # ADD
    eax += edx
    
    # SHR
    eax = eax >> 0xa
    
    # IMUL - MASK32 keeps us w/in 32 bits
    eax = (eax * 0x539) & MASK32
    
    # SUB ecx, eax
    ecx -= eax
    
    seed += ecx
    
    print "currseed: %d" % seed
    
print seed