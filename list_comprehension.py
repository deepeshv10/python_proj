# List comprehension practice
list1 = [i for i in "human"]
print(list1)  # o/p -> ['h', 'u', 'm', 'a', 'n']

# find all numbers less than 20 divisible by 2, and store in a list
nums = [i for i in range(21) if i%2==0]
print(nums) # o/p --> [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

# show all even and odd numbers less than/equal to 20 :
num = [f'{i} even' if i%2==0 else f'{i} odd' for i in range(21)]
print(num) # o/p -> ['0 even', '1 odd', '2 even', '3 odd', '4 even', '5 odd', '6 even', '7 odd', '8 even', '9 odd', '10 even', '11 odd', '12 even', '13 odd', '14 even', '15 odd', '16 even', '17 odd', '18 even', '19 odd', '20 even']
