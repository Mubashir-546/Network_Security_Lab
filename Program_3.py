import numpy as np

key_matrix = np.array([[3, 3],
                       [2, 5]])

plaintext = input("Enter 2-letter text: ").upper()

P = np.array([[ord(plaintext[0]) - 65],
              [ord(plaintext[1]) - 65]])

C = np.dot(key_matrix, P) % 26

cipher = ""

for i in range(2):
    cipher += chr(C[i][0] + 65)

print("Cipher Text:", cipher)