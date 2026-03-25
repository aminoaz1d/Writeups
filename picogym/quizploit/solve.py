from pwn import *

io = remote(args.HOST, args.PORT)

io.sendline(b"64-bit")
io.sendline(b"dynamic")
io.sendline(b"not stripped")
io.sendline(b"0x15")
io.sendline(b"0x90")
io.sendline(b"yes")
io.sendline(b"fgets")
io.sendline(b"win")
io.sendline(b"buffer overflow")
io.sendline(b"%d" % (0x90-0x15))
io.sendline(b"NX")
io.sendline(b"ROP")
io.sendline(b"0x401176")

io.interactive()
