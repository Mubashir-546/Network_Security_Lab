def rc4(key, text):

    S = list(range(256))
    j = 0

    # KSA
    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    result = []

    # PRGA
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256

        S[i], S[j] = S[j], S[i]

        k = S[(S[i] + S[j]) % 256]

        result.append(chr(ord(char) ^ k))

    return ''.join(result)


key = input("Enter key: ")
plaintext = input("Enter plaintext: ")

cipher = rc4(key, plaintext)

print("Encrypted:", cipher.encode().hex())

decrypted = rc4(key, cipher)

print("Decrypted:", decrypted)