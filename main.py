import workout
import workout_storage
import search_functions
import input_validation

import uuid

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
    spikes = input_validation.validate_yesno("Spikes:")
    gym = input_validation.validate_yesno("Gym:")

    identifier = uuid.uuid4()

    #Send data variables to workout.workout() for storage and handling.
    workout_info = workout.Workout(title, date, w_type, purpose, distance_volume, notes, spikes, gym, identifier)
    
    #Print function's formatted output and data table for testing purposes.
    print(workout_info)
    return workout_info

#Defines function for creating a new workout.
def new_workout(workout_data):
    workout_object = workout_input()
    workout_data.append(workout_object)

#Defines function for viewing a formatted list of all workouts.
def view_all_workouts(workout_data):
    if not workout_data:
        print("\nNo workouts have been created.\n")
        return
        
    for workout in workout_data:
        print(workout)

#Edit workout function.
def edit_workout(workout_data):
    workout_to_edit = search_functions.search_initialization(workout_data)

    if workout_to_edit is None:
        return

    if len(workout_to_edit) > 1:
        workout_to_edit = search_functions.handle_multiple_results(workout_to_edit)

    if not workout_to_edit:
        print("\nOperation Cancelled")
        return

    if not workout_to_edit:
        return
    
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

    FIELDS = {
            MENU["title"]: ("title", "\nNew Title:\t"),
            MENU["date"]: ("date", "\nNew Date:\t"),
            MENU["type"]: ("w_type", "\nNew Type:\t"),
            MENU["purpose"]: ("purpose", "\nNew Purpose:\t"),
            MENU["distance_volume"]: ("distance_volume", "\nNew Volume:\t"),
            MENU["notes"]: ("notes", "\nNew Notes:\t")
        }

    YES_NO_FIELDS = {
        MENU["spikes"]: ("spikes", "\nSpikes:"),
        MENU["gym"]: ("gym", "\nGym:")
    }

    running = True
    user_choice = None
    option_range = (MENU["exit"], MENU["gym"] + 1)
    menu_text = ("\nSelect the aspect of the workout would you like to edit, or type '0' to exit.\n\tTitle (1) || Date (2) || Type (3) || Purpose (4) || Volume (5) || Notes (6) ||  Spikes (7) || Gym (8)\n")
    
    while running:
        #Ensure user_choice is a valid integer input and within the valid range before moving on.
        user_choice = input_validation.validate_menu_input(user_choice, option_range, menu_text) 

        if user_choice == MENU["exit"]:
            print("\nExited Successfully.")
            running = False
            return

        if user_choice in FIELDS:
            attr, prompt = FIELDS[user_choice]
            new_value = input(prompt)
            setattr(workout_to_edit, attr, new_value)
            print("\nUpdated Workout:\n" + str(workout_to_edit))
            user_choice = None

        elif user_choice in YES_NO_FIELDS:
            attr, prompt = YES_NO_FIELDS[user_choice]
            new_value = input_validation.validate_yesno(prompt)
            setattr(workout_to_edit, attr, new_value)
            print("\nUpdated Workout:\n" + str(workout_to_edit))
            user_choice = None
        
#Workout deletion function.
def delete_workout(workout_data):
    workout_to_delete = search_functions.search_initialization(workout_data)

    if workout_to_delete is None:
        return

    if len(workout_to_delete) > 1:
        workout_to_delete = search_functions.handle_multiple_results(workout_to_delete)

    if not workout_to_delete:
        print("\nOperation Cancelled")
        return

    confirmation = input_validation.validate_yesno("\nAre you sure you would like to delete this workout?")

    if not confirmation:
        print("\nOperation Cancelled")
        return

    workout_data.remove(workout_to_delete)
    print("\nWorkout Deleted")

def main():
    print("\nWelcome to CrossBoard!\nPlease select a choice to begin:")

    #Load data from JSON and/or initialize workout_data.
    workout_data = workout_storage.json_to_workouts("workout_data.json")

    MENU = {
        "new_workout": 1,
        "view_workouts": 2,
        "search_workouts": 3,
        "edit": 4,
        "delete": 5,
        "exit": 6
    }

    running = True
    user_choice = None
    option_range = (MENU["new_workout"], MENU["exit"] + 1)
    menu_text = ("\n\t1: New Workout\n\t2: View All Workouts\n\t3: Search Workout\n\t4: Edit Workout\n\t5: Delete Workout\n\t6: Exit")

    #Initialize menu loop.
    while running:
        #Ensure user_choice is a valid integer input and within the valid range before moving on.
        user_choice = input_validation.validate_menu_input(user_choice, option_range, menu_text)
            
        #New Workout.
        if user_choice == MENU["new_workout"]:
            new_workout(workout_data)
            user_choice = None

        #View Workouts.
        elif user_choice == MENU["view_workouts"]:
            view_all_workouts(workout_data)
            user_choice = None
            
        #Search Workout.
        elif user_choice == MENU["search_workouts"]:
            search_functions.search_initialization(workout_data)
            user_choice = None

        #Edit Program.
        elif user_choice == MENU["edit"]:
            edit_workout(workout_data)
            user_choice = None

        #Delete Program.
        elif user_choice == MENU["delete"]:
            delete_workout(workout_data)
            user_choice = None

        #Exit Program. (Save to JSON)
        elif user_choice == MENU["exit"]:
            print("\nThanks for using CrossBoard!\n")
            workout_storage.workouts_to_json("workout_data.json", workout_data)
            running = False
            return

if __name__ == "__main__":
    main()