import random
print('I am thinking of a number between 1 and 20')
i = random.randint(1, 20)

for y in range(1,4):
    print('Take a guess.')
    x = int(input())

    if x < i:
        print("Your guess is too low.")
    elif x > i:
        print("Your guess number is too high.")
    else:
        print("Good job! You guessed my number in " + str(y)  +" guesses")

print(" ")
print("You have tried 3 times.Please try again later!")