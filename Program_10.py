p = 11
q = 13

n = p * q
phi = (p-1)*(q-1)

e = 7
d = 103

msg = int(input("Message: "))

cipher = pow(msg, e, n)

plain = pow(cipher, d, n)

print("Encrypted:", cipher)
print("Decrypted:", plain)