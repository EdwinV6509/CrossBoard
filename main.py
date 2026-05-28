import workout

import uuid

workout_data = []

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
            value = input(f"{prompt.capitalize()}? ('Y'/'N'):\t")
            
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

#Handles input for workout creation using workout.py.
def workout_input():
    #Initialize input variables
    title = input("\nWorkout Title:\t")
    date = input("Date:\t")
    w_type = input("Type:\t")
    purpose = input("Purpose:\t")
    distance_volume = input("Volume:\t")
    notes = input("Notes:\t")
 
    #Ensure spikes and gym inputs are valid yes/no responses.
    spikes = validate_yesno("Spikes")
    gym = validate_yesno("Gym")

    identifier = uuid.uuid4()

    #Send data variables to workout.workout() for storage and handling.
    workout_info = workout.Workout(title, date, w_type, purpose, distance_volume, notes, spikes, gym, identifier)
    
    #Print function's formatted output and data table for testing purposes.
    print(workout_info)
    #print(str(workout_info.data_table) + "\n")
    return workout_info

#Defines function for creating a new workout.
def new_workout():
    workout_object = workout_input()
    workout_data.append(workout_object)

#Defines function for viewing a formatted list of all workouts.
def view_all_workouts():
    if not workout_data:
        print("\nNo workouts have been created.\n")
    else:
        for workout in workout_data:
            print(workout)

#Defines function for searching for a specific workout using its UUID.
def workout_search():
    try:
        identifier_choice = uuid.UUID(input("\nEnter Workout UUID:\t"))

    except (ValueError, TypeError):
        print("\nInvalid Input\n")

        return None

    for workout in workout_data:
        if workout.identifier == identifier_choice:
            print("\nWorkout found:\n" + str(workout))
            return workout
        
    print("\nNo workout found with that UUID.")
    return None

#Edit workout function.
def edit_workout():
    workout_to_edit = workout_search()

    if not workout_to_edit:
        return None
    
    MENU = {
        "exit": 0,
        "title": 1,
        "date": 2,
        "type": 3,
        "purpose": 4,
        "distance_volume": 5,
        "notes": 6,
        "spikes": 7,
        "gym": 8
    }

    running = True

    while running:
        user_choice = None
        option_range = (MENU["exit"], MENU["gym"] + 1)
        menu_text = ("Type the aspect of the workout would you like to edit, or type '0' to exit.\n\tTitle (1) || Date (2) || Type (3) || Purpose (4) || Volume (5) || Notes (6) ||  Spikes (7) || Gym (8)\n")
        
        #Ensure user_choice is a valid integer input and within the valid range before moving on.
        user_choice = validate_menu_input(user_choice, option_range, menu_text) 

        if user_choice == MENU["exit"]:
            print("\nExited Successfully.")
            running = False
            return
        
        FIELDS = {
            MENU["title"]: ("title", "\nNew Title:\t"),
            MENU["date"]: ("date", "\nNew Date:\t"),
            MENU["type"]: ("w_type", "\nNew Type:\t"),
            MENU["purpose"]: ("purpose", "\nNew Purpose:\t"),
            MENU["distance_volume"]: ("distance_volume", "\nNew Volume:\t"),
            MENU["notes"]: ("notes", "\nNew Notes:\t")
        }

        YES_NO_FIELDS = {
            MENU["spikes"]: ("spikes", "\nSpikes"),
            MENU["gym"]: ("gym", "\nGym")
        }

        if user_choice in FIELDS:
            attr, prompt = FIELDS[user_choice]
            new_value = input(prompt)
            setattr(workout_to_edit, attr, new_value)
            print("\nUpdated Workout:\n" + str(workout_to_edit))

        elif user_choice in YES_NO_FIELDS:
            attr, prompt = YES_NO_FIELDS[user_choice]
            new_value = validate_yesno(prompt)
            setattr(workout_to_edit, attr, new_value)
            print("\nUpdated Workout:\n" + str(workout_to_edit))
        
#Workout deletion function.
def delete_workout():
    workout_to_delete = workout_search()

    if not workout_to_delete:
        return
    
    confirmation = validate_yesno("\nAre you sure you would like to delete this workout")

    if confirmation:
        workout_data.remove(workout_to_delete)

        print("\nWorkout Deleted")
    else:
        print("\nOperation Cancelled")

def main():
    print("\nWelcome to CrossBoard!\nPlease select a choice to begin:")
    running = True

    MENU = {
        "new_workout": 1,
        "view_workouts": 2,
        "search_workouts": 3,
        "edit": 4,
        "delete": 5,
        "exit": 6
    }

    #Initialize menu loop.
    while running:
        
        user_choice = None
        option_range = (MENU["new_workout"], MENU["exit"] + 1)
        menu_text = ("\n\t1: New Workout\n\t2: View All Workouts\n\t3: Search Workout\n\t4: Edit Workout\n\t5: Delete Workout\n\t6: Exit")

        #Ensure user_choice is a valid integer input and within the valid range before moving on.
        user_choice = validate_menu_input(user_choice, option_range, menu_text)
            
        #New Workout.
        if user_choice == MENU["new_workout"]:
            new_workout()
            user_choice = None

        #View Workouts.
        elif user_choice == MENU["view_workouts"]:
            view_all_workouts()
            user_choice = None
            
        #Search Workout.
        elif user_choice == MENU["search_workouts"]:
            workout_search()
            user_choice = None

        #Edit Program.
        elif user_choice == MENU["edit"]:
            edit_workout()
            user_choice = None

        #Delete Program.
        elif user_choice == MENU["delete"]:
            delete_workout()
            user_choice = None

        #Exit Program.
        elif user_choice == MENU["exit"]:
            print("\nThanks for using CrossBoard!\n")
            running = False

main()