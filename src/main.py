import workout
import workout_storage
import search_functions
import input_validation

import pyfiglet

import sys
import uuid

line_separate = "\n---------------------------------------\n"

# Main function handling menu navigation and user_input.


def main():
    # Introduce the program using ASCI art and a welcome message.
    ascii_art = pyfiglet.figlet_format("CrossBoard")
    print("\nWelcome to\n", ascii_art)
    print("\nPlease select a choice to begin:\n")

    # Load data from JSON and/or initialize workout_data.
    workout_data = workout_storage.json_to_workouts("workout_data.json")

    MENU = {
        "new_workout": 1,
        "view_workouts": 2,
        "search_workouts": 3,
        "edit": 4,
        "delete": 5,
        "exit": 6,
    }

    option_range = (MENU["new_workout"], MENU["exit"] + 1)
    menu_text = f"{line_separate}\n\t1: New Workout\n\t2: View All Workouts\n\t3: Search Workout\n\t4: Edit Workout\n\t5: Delete Workout\n\t6: Exit\n{line_separate}"

    # Initialize menu loop.
    while True:
        # Ensure user_choice is a valid integer input and within the valid range before moving on.
        user_choice = input_validation.validate_menu_input(option_range, menu_text)

        # New Workout.
        if user_choice == MENU["new_workout"]:
            new_workout(workout_data)

        # View Workouts.
        elif user_choice == MENU["view_workouts"]:
            view_all_workouts(workout_data)

        # Search Workout.
        elif user_choice == MENU["search_workouts"]:
            search_functions.search_initialization(workout_data)

        # Edit Program.
        elif user_choice == MENU["edit"]:
            edit_workout(workout_data)

        # Delete Program.
        elif user_choice == MENU["delete"]:
            delete_workout(workout_data)

        # Exit Program. (Save to JSON)
        elif user_choice == MENU["exit"]:
            print("\nExiting CrossBoard...")

            try:
                workout_storage.workouts_to_json("workout_data.json", workout_data)
                print("Workout data saved successfully.\n")
            except Exception as e:
                print(f"Error saving workout data: {e}")

            sys.exit("Program exited.")


# Handles input for workout creation using workout.py.


def workout_input():
    # Initialize input variables
    title = input("\nWorkout Title:\t")
    date = input("Date:\t")
    w_type = input("Type:\t")
    purpose = input("Purpose:\t")
    distance_volume = input("Volume:\t")
    notes = input("Notes:\t")

    # Ensure spikes and gym inputs are valid yes/no responses.
    spikes = input_validation.validate_yesno("Spikes:")
    gym = input_validation.validate_yesno("Gym:")

    identifier = uuid.uuid4()

    # Send data variables to workout.workout() for storage and handling.
    workout_info = workout.Workout(
        title, date, w_type, purpose, distance_volume, notes, spikes, gym, identifier
    )

    # Print function's formatted output and data table for testing purposes.
    print(workout_info)
    return workout_info


# Defines function for creating a new workout.


def new_workout(workout_data):
    # Takes input for the creation data and appends it to workout_data list as a workout object.
    workout_object = workout_input()
    workout_data.append(workout_object)
    print("Workout Created Successfully.\n")


# Defines function for viewing a formatted list of all workouts.


def view_all_workouts(workout_data):
    if not workout_data:
        print("\nNo workouts have been created.\n")
        return

    for workout in workout_data:
        print(workout)


# Edit workout function.


def edit_workout(workout_data):
    workout_to_edit = search_functions.search_initialization(workout_data)

    if not workout_to_edit or workout_to_edit is None:
        print("\nOperation Cancelled")
        return

    # Handling of workout selection if multiple results are returned from the search function.
    if len(workout_to_edit) > 1:
        workout_to_edit = search_functions.handle_multiple_results(workout_to_edit)

    # Convert a list of workouts to a single workout object if the user has selected a single workout from multiple results, though this is mostly a failsafe.
    if isinstance(workout_to_edit, list):
        workout_to_edit = workout_to_edit[0]

    # Establish menu options.
    MENU = {
        "exit": 0,
        "title": 1,
        "date": 2,
        "type": 3,
        "purpose": 4,
        "distance_volume": 5,
        "notes": 6,
        "spikes": 7,
        "gym": 8,
    }

    # Define fields that will be accessed for workout attributes. Differentiate between string input and yes/no input.
    FIELDS = {
        MENU["title"]: ("title", "\nNew Title:\t"),
        MENU["date"]: ("date", "\nNew Date:\t"),
        MENU["type"]: ("w_type", "\nNew Type:\t"),
        MENU["purpose"]: ("purpose", "\nNew Purpose:\t"),
        MENU["distance_volume"]: ("distance_volume", "\nNew Volume:\t"),
        MENU["notes"]: ("notes", "\nNew Notes:\t"),
    }

    YES_NO_FIELDS = {
        MENU["spikes"]: ("spikes", "\nSpikes:"),
        MENU["gym"]: ("gym", "\nGym:"),
    }

    option_range = (MENU["exit"], MENU["gym"] + 1)
    menu_text = "Select the aspect of the workout would you like to edit, or type '0' to exit.\n\tTitle (1) || Date (2) || Type (3) || Purpose (4) || Volume (5) || Notes (6) ||  Spikes (7) || Gym (8)"

    while True:
        # Ensure user_choice is a valid integer input and within the valid range before moving on.
        user_choice = input_validation.validate_menu_input(option_range, menu_text)

        if user_choice == MENU["exit"]:
            print("\nExited Successfully.\n")
            return

        # If the choice is a field input, prompt for a new value and set the attribute to the new value.
        if user_choice in FIELDS:
            attr, prompt = FIELDS[user_choice]
            new_value = input(prompt)
            setattr(workout_to_edit, attr, new_value)
            print("\nUpdated Workout:\n" + str(workout_to_edit))

        # If the choice is a yes/no input, prompt for a new value and set the attribute to the new value.
        elif user_choice in YES_NO_FIELDS:
            attr, prompt = YES_NO_FIELDS[user_choice]
            new_value = input_validation.validate_yesno(prompt)
            setattr(workout_to_edit, attr, new_value)
            print("\nUpdated Workout:\n" + str(workout_to_edit))


# Workout deletion function.


def delete_workout(workout_data):
    workout_to_delete = search_functions.search_initialization(workout_data)

    if not workout_to_delete or workout_to_delete is None:
        print("\nOperation Cancelled\n")
        return

    # Handling of workout selection if multiple results are returned from the search function.
    if len(workout_to_delete) > 1:
        workout_to_delete = search_functions.handle_multiple_results(workout_to_delete)

    # Convert a list of workouts to a single workout object if the user has selected a single workout from multiple results, though this is mostly a failsafe.
    if isinstance(workout_to_delete, list):
        workout_to_delete = workout_to_delete[0]

    print("\nWorkout to Delete:\n" + str(workout_to_delete))

    confirmation = input_validation.validate_yesno(
        "Are you sure you would like to delete this workout?"
    )

    if not confirmation:
        print("\nOperation Cancelled\n")
        return

    workout_data.remove(workout_to_delete)
    print("\nWorkout Deleted\n")


if __name__ == "__main__":
    main()
