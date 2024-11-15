#!/usr/bin/env python

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct

backend = default_backend()

KEY = "\x00" * 16
IV = '\xcf\xfa\xed\xfe\xde\xc0\xad\xde\xfe\xca\xbe\xba\x0b\xb0\x55\x0a'

first_block = "\x00" * 16

for w in xrange(0, 0xffffffff):
    for x in xrange(0, 0xffffffff):
        for y in xrange(0, 0xffffffff):
            for z in xrange(0, 0xffffffff):
                packed = struct.pack(">IIII", w,x,y,z)
                data = first_block + packed

                cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=backend)
                encryptor = cipher.encryptor()

                ct = encryptor.update(data) + encryptor.finalize()

                hex = ct.encode('hex')
                
                if hex[32:38] == '371303':
                    print packed.encode('hex')
                    print hex[:32]
                    print hex[32:]
                    print hex[32:38]
                    print '-' * 80
                    exit()