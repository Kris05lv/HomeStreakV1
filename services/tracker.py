import json
import logging

class Tracker:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.data = self.get_data()

    def get_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            logging.warning(f"Data file '{self.filename}' not found or corrupt.")
            return {"users": [], "habits": [], "households": []}

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

    def add_user(self, user):
        self.data['users'].append(user.to_dict())
        self.save_data()

    def add_habit(self, habit):
        self.data['habits'].append(habit.to_dict())
        self.save_data()

    def add_household(self, household):
        self.data['households'].append(household.to_dict())
        self.save_data()
