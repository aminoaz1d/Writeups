from Crypto.Cipher import AES
import binascii
from base64 import b64decode

ORIGINAL_KEY = "rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw="
ORIGINAL_IV = "Q2hlY2tNYXRlcml4"

SAMPLE = input()


key = b64decode( ORIGINAL_KEY )
iv =  b64decode( ORIGINAL_IV )
data = b64decode( SAMPLE )
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
print(cipher.decrypt(data))