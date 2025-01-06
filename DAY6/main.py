import calculator_utils  # Importing the utility module

def main():
    print("Welcome to the Modular Calculator!")
    print("Available operations: add, subtract, multiply, divide\n")

    while True:
        num1 = input("Enter the first number (or 'exit' to quit): ")
        if num1.lower() == "exit":
            print("Goodbye!")
            break

        num2 = input("Enter the second number: ")
        operation = input("Enter the operation (add, subtract, multiply, divide): ").lower()

        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            print("Invalid input! Please enter valid numbers.\n")
            continue

        result = calculator_utils.perform_operation(num1, num2, operation)
        if result is not None:
            print(f"The result is: {result}\n")
        else:
            print("Invalid operation! Please choose from add, subtract, multiply, divide.\n")

if __name__ == "__main__":
    main()
