import re

# Verify that the user has input a valid menu option choice.


def validate_menu_input(option_range, menu_text):
    while True:
        print(menu_text)

        user_choice = input()

        if re.search("^\d$", user_choice):
            if int(user_choice) in range(option_range[0], option_range[1]):
                return int(user_choice)

        print("Invalid Input")


# Verify that the user has input Y or N correctly and handle invalid input.


def validate_yesno(prompt):
    while True:
        value = input(f"{prompt} ('Y'/'N'):\t")

        if re.search("^y|n$", value, re.IGNORECASE):
            if str(value.upper()) == "Y":
                return True
            else:
                return False

        print("Invalid Input")
