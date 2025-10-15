import msvcrt

# Prevent system from applying excess presses of <ENTER> that occurred before the raw_input line appears to current and future raw_inputs.
def safe_input(prompt):
    while msvcrt.kbhit():
        msvcrt.getch()
    return raw_input(prompt)

# type can be "int" or "float", or "str"
def get_input(type, message):

    # Define the way in which the message will be displayed.
    message_display = "\n{}\n---: ".format(message)

    # Define the warning message.
    warning_message =  "\n!!! {} required !!!".format(type)

    # Get initial input.
    input = safe_input(message_display) 

    # To avoid referenced before assignment error????
    input_as_correct_type = ''         

    if type == "int":     

        # Ensure that a float or integer is entered.
        while not input.replace('.', '', 1).isdigit():
            
            print(warning_message)
            input = safe_input(message_display)
        
        # Convert string input to float, then float to int.  Direct conversion to int not possible.
        input_as_correct_type = int(float(input))

    elif type == "float":     

        # Ensure that a float or integer is entered.
        while not input.replace('.', '', 1).isdigit():
            
            print(warning_message)
            input = safe_input(message_display)
        
        # Convert string input to float.
        input_as_correct_type = float(input)
    
    elif type == "str":
       
        # Ensure that a letter string is entered.
        while input.replace('.', '', 1).isdigit():
            
            print(warning_message)
            input = safe_input(message_display) 

        # As the string to the output variable
        input_as_correct_type = input

    else:
        print("First argument must be 'int', 'float' or 'str'.")
    
    return input_as_correct_type


