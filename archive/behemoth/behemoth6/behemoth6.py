#! /usr/bin/env python

from pwn import *

SHELL_ASM = """
push 0x%s;
push 0x%s;
push 0x%s
mov ecx, esp;
xor eax, eax;
mov al, 0x4;
mov bl, 0x1;
mov dl, 0xa;
int 0x80;
""" % ( "ty\x00\x00"[::-1].encode('hex'), "oKit"[::-1].encode('hex'), "Hell"[::-1].encode('hex'))

print asm(SHELL_ASM)
