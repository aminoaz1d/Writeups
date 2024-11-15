#! /usr/bin/env python


'''
5213848e48212ab0be1fd0cbde543d4d = 8e841352....
'''

import struct
from binascii import hexlify

user = raw_input("User: ") + '\n\0'

user = user + '\xcc' * (16 - len(user) + 1)

salt  = raw_input("Salt: ") + '\n\0'

salt = salt + '\xba' * (16 - len(salt) + 1)

user = user[:16]
salt = salt[:16]


hash = raw_input("Hash: ")

hash_arr = bytearray.fromhex(hash)

fixed_hash = hash_arr[0:4][::-1] + hash_arr[4:8][::-1] + hash_arr[8:12][::-1] + hash_arr[12:][::-1]

secret = bytearray(16)

for i in range(0, 16):
    tmp = (fixed_hash[i] ^ ord(user[i])) - ord(salt[i])
    tmp &= 0xFF
    secret[i] = tmp
    #print hex(tmp)
    
print 'Recovered secretpass: {}.{}.{}.{}'.format(hexlify(secret[:4][::-1]), hexlify(secret[4:8][::-1]), hexlify(secret[8:12][::-1]), hexlify(secret[12:][::-1]))
print   struct.unpack('<BBBBBBBBBBBBBBBB', secret)