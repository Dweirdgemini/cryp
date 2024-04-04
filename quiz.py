import random 


top_of_range = input('please input a range of numbers to begin:')

if top_of_range.isdigit():
    top_of_range = int(top_of_range)

    if top_of_range <= 0:
     print('Tsuch a fool this one')
    quit()
else:
   print('please type a number larger than 0 next time')
   quit()

   random_number = random.radiant(0, top_of_range)
   guesses = 0

   while True:
      guesses += 1
      user_guess = input('make a guess:')