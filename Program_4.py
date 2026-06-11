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


text = input("Enter text: ")
rails = int(input("Enter rails: "))

print("Cipher Text:", encrypt(text, rails))