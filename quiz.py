import random

top_of_range = input("input a number to begin: ")

if top_of_range.isdigit():
    top_of_range = int(top_of_range)

    if top_of_range <= 0:
        print('do not be a fool.')
        quit()
else:
    print('Please type a number next time.')
    quit()

random_number = random.randint(0, top_of_range)
guesses = 0

while True:
    guesses += 1
    user_guess = input("have a go ")
    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print('Please type a number next time.')
        continue

    if user_guess == random_number:
        print("na juju you use, how you take know?")
        break
    elif user_guess > random_number:
        print("thisone  high pass am oo")
    else:
        print("this one low pass am well well")

print("You got it in", guesses, "guesses")