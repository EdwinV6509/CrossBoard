#Verify that the user has input a valid menu option choice.
def validate_menu_input(user_choice, option_range, menu_text):
    while user_choice is None:
        print(menu_text)

        try:
            user_choice = int(input())

            if (user_choice in range(option_range[0], option_range[1])):
                return user_choice
            else:
                print("\nInvalid Input\n")

        except (TypeError, ValueError):
            print("\nInvalid Input\n")

#Verify that the user has input Y or N correctly and handle invalid input.
def validate_yesno(prompt):
    value = None

    while value is None:
        try:
            value = input(f"{prompt} ('Y'/'N'):\t")
            
            if str(value.upper()) == "Y":
                value = True
            elif str(value.upper()) == "N":
                value = False
            else:
                print("Invalid Input")
                value = None

        except (TypeError, ValueError):
            print("Invalid Input")
            value = None
    
    return value