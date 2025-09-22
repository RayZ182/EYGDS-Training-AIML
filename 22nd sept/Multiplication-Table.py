def multiplication_table(num):
    print(f"Multiplication table of {num}")
    for i in range(1,11):
        print(f"{num} * {i} = {num*i}")

number = int(input("Enter a number: "))
multiplication_table(number)