import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Habit:
    def __init__(self, name, periodicity, points, is_bonus=False):
        self.name = name
        self.periodicity = periodicity  
        self.created_at = datetime.now().isoformat()
        self.points = points
        self.is_bonus = is_bonus


    def complete(self, user):
        today = datetime.now().date()

        if user.has_completed_today(self.name):
            return f"Oops! {self.name} has already been completed today."

        if self.is_bonus:
            current_week = today.strftime('%W-%Y')
            if user.bonus_claimed.get(self.name) == current_week:
                return f"Oops! {self.name} has already been claimed this week."
            user.bonus_claimed[self.name] = current_week

        user.track_completion(self.name, today, self.periodicity)
        points_earned = self.calculate_points(user)
        user.points += points_earned

        return f"Good job, {user.username}! You completed '{self.name}' and earned {points_earned} points."

    def calculate_points(self, user):
        return self.points + user.get_bonus_points(self.name)

    def to_dict(self):
        return {
            'name': self.name,
            'periodicity': self.periodicity,
            'created_at': self.created_at,
            'points': self.points,
            'is_bonus': self.is_bonus
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["periodicity"], data["points"], data["is_bonus"])


