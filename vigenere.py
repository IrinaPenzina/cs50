from cs50 import get_string
import sys

# to get a key word in command line
if len(sys.argv) != 2:
    print("Usage: python vigenere. py k")
    exit(1)
    # key word
k = sys.argv[1]
if k.isalpha() == False:
    print("Usage: python vigenere. py k")
    exit(1)
i = 0
j = 0
y = 0
# lenth of the key word
l = len(k)
# get the text to encipher
p = get_string("plaintext: ")
# enciphered text
print("ciphertext: ", end="")

# lenth of the plaintext
n = len(p)
for c in p:
    # index to count the letters in the key word
    y = (j + i) % l
    k_index = k[y].upper()
    if p[i].isupper():
        print((chr((ord(p[i]) - 65 + ord(k_index) - 65) % 26 + 65)), end="")
    elif p[i].islower():
        print((chr((ord(p[i]) - 97 + ord(k_index) - 65) % 26 + 97)), end="")
    # if not letters print it out as it is
    else:
        print(c, end="")
        j -= 1
    i += 1
print()