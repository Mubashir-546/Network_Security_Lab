from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'1234567890abcdef'  # 16 bytes

cipher = AES.new(key, AES.MODE_ECB)

plaintext = input("Enter plaintext: ")

encrypted = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

print("Encrypted (Hex):", encrypted.hex())

decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)

print("Decrypted Text:", decrypted.decode())