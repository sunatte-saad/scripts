from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json

secret_key = b'c\x9a\x84-\xeb\xb9\xa2\xf4j\x12Z\xb8\x8eJ\xa7\xc5\x92 \xe2C7\xf8\x87<\xc8i\xf2\xcf)\xc3(]'
with open ('ciphered.bin','rb') as f:
    iv=f.read(16)

def encrypt_data(data):
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    json_data = json.dumps(data).encode('utf-8')
    padded_data = pad(json_data, AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def decrypt_data(encrypted_data):
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    json_data = json.loads(unpadded_data.decode('utf-8'))
    return json_data

data_to_encrypt = {'name': 'John Doe', 'age': 25, 'city': 'Example City'}

encrypted_data = encrypt_data(data_to_encrypt)
print("Encrypted data:", encrypted_data)

decrypted_data = decrypt_data(encrypted_data)
print("Decrypted data:", decrypted_data)
