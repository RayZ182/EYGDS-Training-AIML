try:
    value = int(input("Enter a number: "))
    print(10/value)
except ValueError:
    print("Enter a valid number!")
except ZeroDivisionError:
    print("Cannot be divided by zero!")
finally:
    print("Execution Complete!")