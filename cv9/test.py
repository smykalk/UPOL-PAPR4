from random import randint

numbers = [1,2,3,4,5,6,7,8,9]

# Funkce map vrací iterátor a tedy jej musíme převést na list
numbers = list(map(lambda: randint(1,100), numbers)) # -> [1, 4, 9, 16, 25, 36, 49, 64, 81]

print(numbers)