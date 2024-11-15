#! /usr/bin/env python

encstring = ""
encstring = "757c7d51676673607b66737e33617c7d"

print "757c7d51"
print hex(int("757c7d51", 16))

encstring = encstring.decode('hex')
#encstring = encstring[::-1]

out = ''

print ''.join([ chr(ord(x) ^ 18) for x in encstring])