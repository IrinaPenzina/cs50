from cs50 import get_float

# get the number from the user
while True:
    f = get_float("Change owed: ")
    if f > 0:
        break
# initializing count
count = 0
# turning dollars into cents and rounding the number
coins = round(f * 100)
# while there are more than 25
while coins >= 25:
    coins -= 25
    count += 1  # it's ++ in python
# while there are more than 10
while coins >= 10:
    coins -= 10
    count += 1
# while there are more than 5
while coins >= 5:
    coins -= 5
    count += 1
# while there are more than 1
while coins >= 1:
    coins -= 1
    count += 1

print("You get: ", count)