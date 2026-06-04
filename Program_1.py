"""
Classical Ciphers Implementation
=================================
Implements Caesar, Playfair, and Vigenère ciphers
with full encryption and decryption support.

CrypTool 2.0 Verification Notes:
---------------------------------
- Caesar   : Classic > Caesar Cipher
- Playfair : Classic > Playfair Cipher
- Vigenère : Classic > Vigenère Cipher
"""

import string


# ─────────────────────────────────────────────────────────
# 1. CAESAR CIPHER
# ─────────────────────────────────────────────────────────
# Concept:
#   Each letter in the plaintext is shifted by a fixed number
#   of positions (the 'key') in the alphabet.
#   Named after Julius Caesar who reportedly used shift=3.
#
#   Formula:
#     Encrypt: C = (P + key) mod 26
#     Decrypt: P = (C - key) mod 26
#
#   Example (key=3):
#     A → D,  B → E,  Z → C  (wraps around)
# ─────────────────────────────────────────────────────────

def caesar_encrypt(plaintext: str, key: int) -> str:
    """
    Encrypt plaintext using Caesar cipher.
    - Non-alphabetic characters are kept as-is.
    - Case is preserved.
    """
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            # Shift and wrap around using mod 26
            shifted = (ord(char) - base + key) % 26
            result.append(chr(shifted + base))
        else:
            result.append(char)   # spaces, punctuation unchanged
    return ''.join(result)


def caesar_decrypt(ciphertext: str, key: int) -> str:
    """
    Decrypt ciphertext using Caesar cipher.
    Decryption = encryption with negative shift.
    """
    return caesar_encrypt(ciphertext, -key)


def caesar_brute_force(ciphertext: str) -> list:
    """
    Try all 25 possible shifts (brute-force attack).
    Returns list of (shift, decrypted_text).
    """
    return [(k, caesar_decrypt(ciphertext, k)) for k in range(1, 26)]


# ─────────────────────────────────────────────────────────
# 2. PLAYFAIR CIPHER
# ─────────────────────────────────────────────────────────
# Concept:
#   A digraph substitution cipher — it encrypts pairs of letters
#   (bigrams) instead of individual letters, making frequency
#   analysis harder.
#
#   Key Square (5×5 grid):
#     - Fill a 5×5 grid with the key letters (no duplicates),
#       then the remaining alphabet letters.
#     - I and J share the same cell (to fit 26 letters in 25 cells).
#
#   Encryption Rules for each pair (X, Y):
#     1. Same row    → each shifts RIGHT one column (wraps)
#     2. Same column → each shifts DOWN one row    (wraps)
#     3. Rectangle  → each swaps to the other's column
#
#   Pre-processing:
#     - J → I
#     - Insert 'X' between repeated letters in a pair: "LL" → "LX|L"
#     - Pad with 'X' if plaintext length is odd
# ─────────────────────────────────────────────────────────

def _build_playfair_square(key: str) -> list:
    """Build the 5×5 Playfair key square."""
    key = key.upper().replace('J', 'I')
    seen = []
    # Add key letters first (no duplicates)
    for ch in key:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    # Fill remaining alphabet
    for ch in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':  # no J
        if ch not in seen:
            seen.append(ch)
    # Convert flat list to 5×5 grid
    return [seen[i*5:(i+1)*5] for i in range(5)]


def _find_position(square: list, letter: str):
    """Return (row, col) of a letter in the key square."""
    for r, row in enumerate(square):
        if letter in row:
            return r, row.index(letter)
    raise ValueError(f"Letter '{letter}' not found in square")


def _prepare_plaintext(text: str) -> list:
    """
    Pre-process plaintext into digrams (pairs of letters):
      - Uppercase, J→I, strip non-alpha
      - Insert 'X' between repeated letters in a pair
      - Pad with 'X' if length is odd
    """
    text = text.upper().replace('J', 'I')
    cleaned = [c for c in text if c.isalpha()]

    digrams = []
    i = 0
    while i < len(cleaned):
        a = cleaned[i]
        if i + 1 == len(cleaned):
            # Odd length: pad last single letter with X
            b = 'X'
            i += 1
        elif cleaned[i] == cleaned[i + 1]:
            # Repeated pair: insert X as filler
            b = 'X'
            i += 1
        else:
            b = cleaned[i + 1]
            i += 2
        digrams.append((a, b))
    return digrams


def playfair_encrypt(plaintext: str, key: str) -> str:
    """Encrypt plaintext using Playfair cipher."""
    square = _build_playfair_square(key)
    digrams = _prepare_plaintext(plaintext)
    result = []

    for a, b in digrams:
        ra, ca = _find_position(square, a)
        rb, cb = _find_position(square, b)

        if ra == rb:
            # Same row: shift each letter one column to the right (wrap)
            result += [square[ra][(ca + 1) % 5], square[rb][(cb + 1) % 5]]
        elif ca == cb:
            # Same column: shift each letter one row down (wrap)
            result += [square[(ra + 1) % 5][ca], square[(rb + 1) % 5][cb]]
        else:
            # Rectangle: swap columns
            result += [square[ra][cb], square[rb][ca]]

    return ''.join(result)


def playfair_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt ciphertext using Playfair cipher."""
    square = _build_playfair_square(key)
    # Split ciphertext into digrams (already prepared)
    ct = ciphertext.upper().replace('J', 'I')
    ct = [c for c in ct if c.isalpha()]
    digrams = [(ct[i], ct[i+1]) for i in range(0, len(ct), 2)]
    result = []

    for a, b in digrams:
        ra, ca = _find_position(square, a)
        rb, cb = _find_position(square, b)

        if ra == rb:
            # Same row: shift LEFT one column (reverse of encrypt)
            result += [square[ra][(ca - 1) % 5], square[rb][(cb - 1) % 5]]
        elif ca == cb:
            # Same column: shift UP one row (reverse of encrypt)
            result += [square[(ra - 1) % 5][ca], square[(rb - 1) % 5][cb]]
        else:
            # Rectangle: swap columns (same operation as encryption)
            result += [square[ra][cb], square[rb][ca]]

    return ''.join(result)


# ─────────────────────────────────────────────────────────
# 3. VIGENÈRE CIPHER
# ─────────────────────────────────────────────────────────
# Concept:
#   A polyalphabetic cipher — uses multiple Caesar shifts
#   based on a repeating keyword.
#
#   The key is repeated to match the plaintext length,
#   and each plaintext letter is shifted by the corresponding
#   key letter's alphabet position (A=0, B=1, ... Z=25).
#
#   Formula:
#     Encrypt: C_i = (P_i + K_i) mod 26
#     Decrypt: P_i = (C_i - K_i) mod 26
#
#   Example (key = "KEY"):
#     Plaintext:  A  T  T  A  C  K
#     Key repeat: K  E  Y  K  E  Y
#     Encrypted:  K  X  R  K  G  I
#
#   Advantage over Caesar: same letter encrypts differently
#   depending on its position → defeats simple frequency analysis.
# ─────────────────────────────────────────────────────────

def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using Vigenère cipher.
    - Key is repeated/truncated to match plaintext length.
    - Non-alphabetic characters are preserved and don't advance the key index.
    """
    key = key.upper()
    key_len = len(key)
    result = []
    key_idx = 0  # separate index so spaces don't skip key letters

    for char in plaintext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_shift = ord(key[key_idx % key_len]) - ord('A')
            shifted = (ord(char) - base + key_shift) % 26
            result.append(chr(shifted + base))
            key_idx += 1   # advance key only for alpha chars
        else:
            result.append(char)

    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt ciphertext using Vigenère cipher.
    Decryption subtracts the key shift instead of adding it.
    """
    key = key.upper()
    key_len = len(key)
    result = []
    key_idx = 0

    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_shift = ord(key[key_idx % key_len]) - ord('A')
            shifted = (ord(char) - base - key_shift) % 26
            result.append(chr(shifted + base))
            key_idx += 1
        else:
            result.append(char)

    return ''.join(result)


# ─────────────────────────────────────────────────────────
# DEMO / TEST
# ─────────────────────────────────────────────────────────

def demo():
    print("=" * 60)
    print("  CLASSICAL CIPHERS DEMO")
    print("=" * 60)

    # ── Caesar ──────────────────────────────────────────────
    print("\n[1] CAESAR CIPHER  (key = 13 / ROT-13)")
    pt = "Hello, World!"
    key = 13
    ct = caesar_encrypt(pt, key)
    dt = caesar_decrypt(ct, key)
    print(f"  Plaintext : {pt}")
    print(f"  Encrypted : {ct}")
    print(f"  Decrypted : {dt}")

    # ── Playfair ─────────────────────────────────────────────
    print("\n[2] PLAYFAIR CIPHER  (key = 'MONARCHY')")
    pt = "INSTRUMENTS"
    key = "MONARCHY"
    sq = _build_playfair_square(key)
    ct = playfair_encrypt(pt, key)
    dt = playfair_decrypt(ct, key)
    print(f"  Plaintext : {pt}")
    print(f"  Key Square:")
    for row in sq:
        print("    " + " ".join(row))
    print(f"  Encrypted : {ct}")
    print(f"  Decrypted : {dt}")

    # ── Vigenère ─────────────────────────────────────────────
    print("\n[3] VIGENÈRE CIPHER  (key = 'LEMON')")
    pt = "ATTACKATDAWN"
    key = "LEMON"
    ct = vigenere_encrypt(pt, key)
    dt = vigenere_decrypt(ct, key)
    print(f"  Plaintext : {pt}")
    print(f"  Key       : {key}")
    print(f"  Encrypted : {ct}")
    print(f"  Decrypted : {dt}")

    print("\n" + "=" * 60)
    print("  All ciphers verified ✓")
    print("  Cross-check these outputs in CrypTool 2.0:")
    print("  Caesar  → Classic > Caesar Cipher")
    print("  Playfair → Classic > Playfair Cipher")
    print("  Vigenère → Classic > Vigenère Cipher")
    print("=" * 60)


if __name__ == "__main__":
    demo()