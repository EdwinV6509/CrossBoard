#Initialize a standard class for workouts and their inputs.
class Workout():
    def __init__(self, title, date, w_type, purpose, distance_volume, notes, spikes, gym, identifier):
        self.title = title
        self.date = date
        self.w_type = w_type
        self.purpose = purpose
        self.distance_volume = distance_volume
        self.notes = notes

        self.spikes = spikes
        self.gym = gym

        self.identifier = identifier

    #Return a printable string.
    def __str__(self):
        return f"\n{self.title} on {self.date}:\n {self.w_type} || {self.purpose} || {self.distance_volume} || {self.notes}\n Spikes: {self.spikes} || Gym Workout: {self.gym}\n {self.identifier}\n"