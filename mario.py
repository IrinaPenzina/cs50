from cs50 import get_int


while True:
    n = get_int("Positive number: ")
    if 0 <= n <= 23:
        break

# hight
for i in range(n):
    # spaces
    for j in range(n - i - 1):
        print(" ", end="")
    # hashes
    for j in range(i + 2):
        print("#", end="")
    # new line
    print()
