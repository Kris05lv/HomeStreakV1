import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class User:
    def __init__(self, username, household, points=0):
        self.username = username
        self.household = household
        self.habits_completed = {}  
        self.streaks = {}  
        self.bonus_claimed = {}  
        self.points = points

    def has_completed_today(self, habit_name):
        today = datetime.now().date()
        return habit_name in self.habits_completed and self.habits_completed[habit_name][-1] == today

    def track_completion(self, habit_name, date, periodicity):
        if habit_name not in self.habits_completed:
            self.habits_completed[habit_name] = []
            self.streaks[habit_name] = 0

        self.habits_completed[habit_name].append(date)
        self.update_streak(habit_name, periodicity)

    def update_streak(self, habit_name, periodicity):
        completions = self.habits_completed[habit_name]
        if len(completions) < 2:
            self.streaks[habit_name] = 1
            return

        streak = 1
        for i in range(1, len(completions)):
            delta = (completions[i] - completions[i - 1]).days
            if (periodicity == 'daily' and delta == 1) or (periodicity == 'weekly' and delta == 7):
                streak += 1
            else:
                streak = 1 
            if streak % 7 == 0:
                self.points += 5  

        self.streaks[habit_name] = streak

    def get_bonus_points(self, habit_name):
        return 5 if self.streaks.get(habit_name, 0) % 7 == 0 else 0

    def to_dict(self):
        return {
            'username': self.username,
            'household': self.household.name if hasattr(self.household, 'name') else str(self.household),
            'habits_completed': {
                habit: [date.strftime("%Y-%m-%d") for date in dates]
                for habit, dates in self.habits_completed.items()
            },
            'streaks': self.streaks,
            'bonus_claimed': self.bonus_claimed,
            'points': self.points
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"])
        user.habits_completed = {
            habit: [datetime.strptime(date, "%Y-%m-%d").date() for date in dates]
            for habit, dates in data["habits_completed"].items()
        }
        user.streaks = data["streaks"]
        user.bonus_claimed = data["bonus_claimed"]
        user.points = data["points"]
        return user