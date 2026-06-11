def generate_key_matrix(key):
    key = key.upper().replace("J", "I")

    matrix = []
    used = set()

    for ch in key:
        if ch not in used and ch.isalpha():
            matrix.append(ch)
            used.add(ch)

    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col


def encrypt_pair(matrix, a, b):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]

    elif c1 == c2:
        return matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]

    else:
        return matrix[r1][c2] + matrix[r2][c1]


key = input("Enter key: ")
plaintext = input("Enter plaintext: ").upper()

matrix = generate_key_matrix(key)

print("Key Matrix:")
for row in matrix:
    print(row)

cipher = ""

for i in range(0, len(plaintext), 2):
    a = plaintext[i]
    b = plaintext[i+1] if i+1 < len(plaintext) else "X"

    cipher += encrypt_pair(matrix, a, b)

print("Cipher Text:", cipher)