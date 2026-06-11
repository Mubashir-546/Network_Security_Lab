def encrypt(text, rails):
    fence = [[] for _ in range(rails)]

    row = 0
    direction = 1

    for char in text:
        fence[row].append(char)

        row += direction

        if row == rails - 1:
            direction = -1
        elif row == 0:
            direction = 1

    cipher = ""

    for rail in fence:
        cipher += "".join(rail)

    return cipher


def decrypt(cipher, rails):

    # Create empty pattern matrix
    pattern = [['' for _ in range(len(cipher))]
               for _ in range(rails)]

    row = 0
    direction = 1

    # Mark zig-zag positions
    for col in range(len(cipher)):
        pattern[row][col] = '*'

        row += direction

        if row == rails - 1:
            direction = -1
        elif row == 0:
            direction = 1

    # Fill marked positions with ciphertext
    index = 0

    for r in range(rails):
        for c in range(len(cipher)):
            if pattern[r][c] == '*' and index < len(cipher):
                pattern[r][c] = cipher[index]
                index += 1

    # Read zig-zag pattern
    result = ""

    row = 0
    direction = 1

    for col in range(len(cipher)):
        result += pattern[row][col]

        row += direction

        if row == rails - 1:
            direction = -1
        elif row == 0:
            direction = 1

    return result


text = input("Enter text: ")
rails = int(input("Enter number of rails: "))

cipher = encrypt(text, rails)
print("Encrypted Text:", cipher)

plain = decrypt(cipher, rails)
print("Decrypted Text:", plain)