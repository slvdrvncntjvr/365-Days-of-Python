print("Enter a number: ")
num = int(input())

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Numbers less than", num, "are:")
for number in numbers:
    if number < num:
        print(number)
print("Numbers greater than or equal to", num, "are:")
for number in numbers:
    if number >= num:
        print(number)
print("Numbers divisible by", num, "are:")
for number in numbers:
    if number % num == 0:
        print(number)
print("Numbers not divisible by", num, "are:")
for number in numbers:
    if number % num != 0:
        print(number)
print("Numbers equal to", num, "are:")
for number in numbers:
    if number == num:
        print(number)
print("Numbers not equal to", num, "are:")
for number in numbers:
    if number != num:
        print(number)
print("Numbers less than or equal to", num, "are:")
