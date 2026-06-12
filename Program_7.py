from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

key = b'8bytekey'  # Exactly 8 bytes

cipher = DES.new(key, DES.MODE_ECB)

plaintext = input("Enter plaintext: ")

encrypted = cipher.encrypt(pad(plaintext.encode(), DES.block_size))

print("Encrypted (Hex):", encrypted.hex())

decrypted = unpad(cipher.decrypt(encrypted), DES.block_size)

print("Decrypted Text:", decrypted.decode())