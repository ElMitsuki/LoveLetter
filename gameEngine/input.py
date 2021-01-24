def parse_string_to_int(string):
    """Parse string value to int handling exceptions.

    IN:
    string -- string to parse
    OUT:
    value -- int value or string value error

    """
    try:
        value = int(string)
    except ValueError:
        value = string + " not an integer"
    return value

def input_int(string = ""):
    """Input an integer verifying it is correct.

    Input while it is not correct.
    
    IN:
    string -- message to display for the input

    OUT:
    value -- the input value

    """
    correct_value = False 
    while not correct_value:
        value = parse_string_to_int(input(string))
        if isinstance(value, int):
            correct_value = True
        else:
            print("Valeur incorrecte, ressaisissez :")
    return value