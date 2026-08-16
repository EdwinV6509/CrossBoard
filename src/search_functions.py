import input_validation

import uuid

#  Identifies user input and determines which search function to use.


def search_initialization(workout_data):
    # Establish the menu choices, which attributes they equate to, and what type of data they would affect.
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
        9: ("uuid", "uuid", 9),
    }

    option_range = (MENU[0][2], MENU[9][2] + 1)
    menu_text = "\nSelect the method by which you would like to search available workouts or type '0' to exit.\n\tTitle (1) || Date (2) || Type (3) || Purpose (4) || Volume (5) || Notes (6) ||  Spikes (7) || Gym (8) || UUID (9)"

    while True:
        user_choice = input_validation.validate_menu_input(option_range, menu_text)

        if user_choice:
            selection = MENU[user_choice]
            break

    if selection[1] == None:
        print("\nExited Successfully.")
        return

    if selection[1] == "field":
        return workout_search_field(workout_data, selection[0])

    if selection[1] == "binary":
        return workout_search_binary(workout_data, selection[0])

    if selection[1] == "uuid":
        return workout_search_uuid(workout_data)


# Search by field where value is unrestricted string input.


def workout_search_field(workout_data, field):
    search_term = input("\nEnter search term:\t").strip()
    results = []

    for workout in workout_data:
        workout_field_value = getattr(workout, field, None)

        if workout_field_value is None:
            continue

        if not isinstance(workout_field_value, str):
            workout_field_value = str(workout_field_value)

        if search_term.lower() in workout_field_value.lower():
            results.append(workout)

    return handle_returned_results(results, field, search_term)


# Search by boolean where value is restricted by validate_yesno().


def workout_search_binary(workout_data, field):
    search_term = input_validation.validate_yesno("\nEnter search value:\t")
    results = []

    for workout in workout_data:
        if search_term == getattr(workout, field):
            results.append(workout)

    return handle_returned_results(results, field, search_term)


# Defines function for searching for a specific workout using its UUID.


def workout_search_uuid(workout_data):
    try:
        identifier_choice = uuid.UUID(input("\nEnter Workout UUID:\t"))

    except (ValueError, TypeError):
        print("\nInvalid Input\n")
        return

    # Find workout that matches the identified UUID.
    for workout in workout_data:
        if workout.identifier == identifier_choice:
            print("\nWorkout found:" + str(workout))
            return workout

    print(f"\nNo workout found with UUID: {identifier_choice}")
    return


# Handle multiple returned results if functions are used within a search.


def handle_multiple_results(results):
    print("\nMultiple workouts have been found:\n")
    menu_options = []

    iteration = 1

    for workout in results:
        print(str(iteration) + ")" + str(workout))
        menu_options.append([workout, iteration])
        iteration += 1

    option_range = (-1, len(menu_options) + 1)
    menu_text = "\nSelect the workout you wish to target, or type '0' to exit:"

    while True:
        user_choice = input_validation.validate_menu_input(option_range, menu_text)

        if user_choice == 0:
            print("\nExited Successfully.")
            return

        if user_choice not in range(option_range[0], option_range[1]):
            print("\nInvalid Input")
            continue

        return menu_options[user_choice - 1][0]


# Handle returning search results and print accordingly.


def handle_returned_results(results, field, search_term):
    if results:
        print(
            f"\n{len(results)} workouts found for field '{field}' with search term '{search_term}':"
        )

        for workout in results:
            print(str(workout))

        # Results will be returned as a list containing a Workout object, using attributes is necessary.
        return results

    print(f"\nNo workout found for field '{field}' with search term '{search_term}'.\n")
    return
