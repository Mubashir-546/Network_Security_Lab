from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA Keys
key = RSA.generate(2048)

public_key = key.publickey()
private_key = key

encryptor = PKCS1_OAEP.new(public_key)
decryptor = PKCS1_OAEP.new(private_key)

plaintext = input("Enter plaintext: ")

ciphertext = encryptor.encrypt(plaintext.encode())

print("Encrypted (Hex):")
print(ciphertext.hex())

decrypted = decryptor.decrypt(ciphertext)

print("Decrypted Text:", decrypted.decode())