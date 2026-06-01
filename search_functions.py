import input_validation

import uuid

#Identifies user input and determines which search function to use.
def search_initialization(workout_data):
    MENU = {
        0: ("exit", None, 0),
        1: ("title", "field", 1),
        2: ("date", "field", 2),
        3: ("w_type", "field", 3),
        4: ("purpose", "field", 4),
        5: ("distance_volume", "field", 5),
        6: ("notes", "field", 6),
        7: ("spikes", "binary", 7),
        8: ("gym", "binary", 8),
        9: ("uuid", "uuid", 9)
    }

    user_choice = None
    option_range = (MENU[0][2], MENU[9][2] + 1)
    menu_text = "\nSelect the method by which you would like to search available workouts or type '0' to exit.\n\tTitle (1) || Date (2) || Type (3) || Purpose (4) || Volume (5) || Notes (6) ||  Spikes (7) || Gym (8) || UUID (9)\n"

    while True:
        user_choice = input_validation.validate_menu_input(user_choice, option_range, menu_text)

        selection = MENU[user_choice]
        break

    if user_choice == MENU[0][2]:
        print("\nExited Successfully.")
        user_choice = None
        return

    if selection[1] == "field":
        return workout_search_field(workout_data, selection[0])
    
    if selection[1] == "binary":
        return workout_search_binary(workout_data, selection[0])
    
    if selection[1] == "uuid":
        return workout_search_uuid(workout_data)
        
#Defines function for searching for a specific workout using its UUID.
def workout_search_uuid(workout_data):
    try:
        identifier_choice = uuid.UUID(input("\nEnter Workout UUID:\t"))

    except (ValueError, TypeError):
        print("\nInvalid Input\n")
        return

    #Find workout that matches the identified UUID.
    for workout in workout_data:
        if workout.identifier == identifier_choice:
            print("\nWorkout found:\n" + str(workout))
            return workout
        
    print("\nNo workout found with that UUID.")
    return

#Handle returning search results and print accordingly.
def handle_returned_results(results):
    if results:
        print("\n" + str(len(results)) + " workouts found:")

        for workout in results:
            print(str(workout))

        return results
        
    print("\nNo workouts found.")
    return

#Search by field where value is unrestricted string input.
def workout_search_field(workout_data, field):
    search_term = input("\nEnter search term:")
    results = []

    for workout in workout_data:
        if search_term.lower() in getattr(workout, field).lower():
            results.append(workout)
    
    return handle_returned_results(results)

#Search by boolean where value is restricted by validate_yesno().
def workout_search_binary(workout_data, field):
    search_term = input_validation.validate_yesno("\nEnter search value:")
    results = []

    for workout in workout_data:
        if search_term == getattr(workout, field):
            results.append(workout)
        
    return handle_returned_results(results)

#Handle multiple returned results if functions are used within a search.
def handle_multiple_results(results):
    print("\nMultiple workouts have been found:\n")
    menu_options = []

    iteration = 1

    for workout in results:
        print(str(iteration) + ")\n" + str(workout))
        menu_options.append([workout, iteration])
        iteration += 1

    user_choice = None
    option_range = (-1, len(menu_options) + 1)
    menu_text = "\nSelect the workout you wish to target, or type '0' to exit:\n"

    while True:
        user_choice = input_validation.validate_menu_input(user_choice, option_range, menu_text)

        if user_choice == 0:
            print("\nExited Successfully.")
            user_choice = None
            return user_choice
        
        return menu_options[user_choice - 1][0]
