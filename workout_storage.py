import workout

import uuid
import json

#Save inputted data to a given JSON file.
def workouts_to_json(file, data):
    json_data = []

    #For each workout in the given table, convert it's attribute data into a labelled dictionary.
    for workout in data:
        json_data.append({
            "title": workout.title,
            "date": workout.date,
            "w_type": workout.w_type,
            "purpose": workout.purpose,
            "distance_volume": workout.distance_volume,
            "notes": workout.notes,
            "spikes": workout.spikes,
            "gym": workout.gym,
            "identifier": str(workout.identifier)
        })

    #Dump this data onto the given JSON file.
    with open(file, "w") as json_file:
        json.dump(json_data, json_file, indent = 4)

#Rebuild given workout data from JSON file to a standard class "Workout" object.
def json_to_workouts(file):
    data_loaded = []

    #Open JSON file as a read-only file.
    with open(file, "r") as json_file:
        data = json.load(json_file)

    #For each workout in the data, run it throut workout.Workout to form it into a valid object and append it to the loaded data.
    for workout_item in data:
        data_loaded.append(
            workout.Workout(
                workout_item["title"], 
                workout_item["date"], 
                workout_item["w_type"],
                workout_item["purpose"], 
                workout_item["distance_volume"], 
                workout_item["notes"], 
                workout_item["spikes"], 
                workout_item["gym"], 
                uuid.UUID(workout_item["identifier"])
            )
        )

    return data_loaded