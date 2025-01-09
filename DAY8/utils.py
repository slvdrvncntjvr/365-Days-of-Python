def get_valid_input(prompt, expected_type, valid_range=None):
    """
    Get valid input from the user.
    :param prompt: The prompt message.
    :param expected_type: The expected data type of the input.
    :param valid_range: A range of valid values (optional).
    :return: A valid user input.
    """
    while True:
        try:
            value = expected_type(input(prompt))
            if valid_range and value not in valid_range:
                raise ValueError
            return value
        except ValueError:
            print(f"Invalid input! Please enter a valid {expected_type.__name__}.")
