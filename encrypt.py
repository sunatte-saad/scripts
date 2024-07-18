from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import json
#key=get_random_bytes(32)
#print (key)

salt=b'c\x9a\x84-\xeb\xb9\xa2\xf4j\x12Z\xb8\x8eJ\xa7\xc5\x92 \xe2C7\xf8\x87<\xc8i\xf2\xcf)\xc3(]'
password='password'
key=PBKDF2(password,salt,dkLen=32)
cipher =AES.new(key, AES.MODE_CBC)

message =b"{'key':'value'}"

cipher=AES.new(key, AES.MODE_CBC)

ciphered_data=cipher.encrypt(pad(message, AES.block_size))

with open ('ciphered.bin','wb') as f:
    f.write(cipher.iv)
    f.write(ciphered_data)

with open ('ciphered.bin','rb') as f:
    iv=f.read(16)
    ciphered_data=f.read()

cipher=AES.new(key, AES.MODE_CBC, iv)
deciphered_data=unpad(cipher.decrypt(ciphered_data), AES.block_size)   
print(deciphered_data)
 
with open ('key.bin','wb') as f:
    f.write(key)


#for files, just read the files in b and then use the similar functions
