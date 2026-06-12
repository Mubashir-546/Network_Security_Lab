def extended_gcd(a, b):

    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(a, b % a)

    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

gcd, x, y = extended_gcd(a, b)

print("GCD =", gcd)
print("x =", x)
print("y =", y)