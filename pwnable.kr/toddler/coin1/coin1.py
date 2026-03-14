#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 9007
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
exe = './path/to/binary'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 9007)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================

REAL = 10
COUNTERFEIT = 9

def contains_counterfeit(coins):
    weight = get_weight(coins)
    return not ((weight % REAL) == 0)

def get_weight(coins):
    io.sendline(' '.join(coins).encode('latin1'))
    return int(io.readline())

def find_coin(num_coins):
    coins = [str(x) for x in range(num_coins)]
    return _find_coin(coins)

def _find_coin(coins):
    # UNWIND CASE - WE FOUND IT!
    if len(coins) == 1:
        return coins[0]

    # SEARCH CASE - RECURSE!

    mid = len(coins) // 2
    search_branch = None

    left = coins[:mid]
    right = coins[mid:]

    if contains_counterfeit(left):
        search_branch = left
    else:
        search_branch = right

    return _find_coin(search_branch)

io = start()

io.readuntil(b"- Ready? starting in 3 sec... -\n")
io.readline() # trash

for i in range(0, 100):
    # grab count convert to int
    line_num = io.readline().strip().split(b' ')
    num_coins = int(line_num[0].split(b'=')[1])
    log.info(f"num_coins = {num_coins} ... starting search")
    coin = find_coin(num_coins)
    log.info(f"found coin {coin}...let's try it")
    io.clean()
    lastline = b'9\n'
    while lastline == b'9\n':
      io.sendline(f"{coin}".encode('latin1'))
      lastline = io.readline()

io.interactive()
