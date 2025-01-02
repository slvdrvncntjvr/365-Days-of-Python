def calculator():
    print("Calculator")
    print("Enter two numbers and choose an operation.")
    
    try:
        
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
       
        print("\nOperations:")
        print("1: Addition (+)")
        print("2: Subtraction (-)")
        print("3: Multiplication (*)")
        print("4: Division (/)")
        
        
        operation = input("Choose an operation (1/2/3/4): ")
        
        
        if operation == "1":
            result = num1 + num2
            print(f"\nResult: {num1} + {num2} = {result}")
        elif operation == "2":
            result = num1 - num2
            print(f"\nResult: {num1} - {num2} = {result}")
        elif operation == "3":
            result = num1 * num2
            print(f"\nResult: {num1} * {num2} = {result}")
        elif operation == "4":
            if num2 != 0:
                result = num1 / num2
                print(f"\nResult: {num1} / {num2} = {result}")
            else:
                print("\nError: Division by zero is not allowed!")
        else:
            print("\nInvalid operation. Please choose a valid option.")

    except ValueError:
        print("\nError: Please enter valid numbers.")

if __name__ == "__main__":
    calculator()
