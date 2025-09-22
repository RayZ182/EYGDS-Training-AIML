def  even_odd(num):
    if num%2 == 0:
        return f" {num} is Even"
    else:
        return f"{num} is Odd"

number = int(input("Enter a number: "))
print(even_odd(number))