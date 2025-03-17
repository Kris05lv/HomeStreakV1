import json
import logging
from datetime import datetime, timedelta
from services.leaderboard import Leaderboard
from classes.user import User

logging.basicConfig(level=logging.INFO)

class DataManager:
    FILE_PATH = "data.json"

    @staticmethod
    def load_data():
        """Loads data from JSON file or initializes default structure."""
        try:
            with open(DataManager.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {
                "households": {}, 
                "habits": [], 
                "bonus_habits": [],  
                "leaderboard": {"rankings": {}, "past_rankings": []},
                "streaks": {}  
            }
        
        if "bonus_habits" not in data:
            data["bonus_habits"] = []
        if "streaks" not in data:
            data["streaks"] = {}  
        return data

    @staticmethod
    def save_data(data):
        """Saves data to JSON file."""
        with open(DataManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def create_household(household_name):
        """Creates a new household if it doesn't already exist."""
        data = DataManager.load_data()
        if household_name in data["households"]:
            logging.warning(f"Household '{household_name}' already exists.")
            return
        data["households"][household_name] = {"members": [], "points": {}}
        DataManager.save_data(data)

    @staticmethod
    def save_user(user):
        """Adds a user to an existing household."""
        data = DataManager.load_data()
        if user.household not in data["households"]:
            logging.error(f"Household '{user.household}' does not exist. Please create it first.")
            return
        if user.username in data["households"][user.household]["members"]:
            logging.warning(f"User '{user.username}' is already in household '{user.household}'.")
            return
        data["households"][user.household]["members"].append(user.username)
        data["households"][user.household]["points"][user.username] = 0  

        if user.username not in data["streaks"]:
            data["streaks"][user.username] = {}  

        DataManager.save_data(data)
       

    @staticmethod
    def save_habit(habit):
        """Saves a new habit (regular or bonus) to the database."""
        data = DataManager.load_data()
        habit_dict = habit.to_dict()

        if any(h["name"] == habit.name for h in data["habits"]):
            logging.warning(f"Habit '{habit.name}' already exists.")
            return

        if habit.is_bonus:
            data["bonus_habits"].append(habit_dict)
        else:
            data["habits"].append(habit_dict)

        DataManager.save_data(data)

    @staticmethod
    def save_bonus_habit(habit):
        """Saves a bonus habit to the database."""
        data = DataManager.load_data()
        habit_dict = habit.to_dict()  
        if any(h["name"] == habit.name for h in data["bonus_habits"]):
            logging.warning(f"Bonus habit '{habit.name}' already exists.")
            return
        data["bonus_habits"].append(habit_dict)  
        DataManager.save_data(data)

    @staticmethod
    def complete_habit(username, habit_name):
        """Marks a habit as completed, tracks streaks, updates points, and leaderboard."""
        data = DataManager.load_data()

        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if not habit:
            logging.error(f"Habit '{habit_name}' not found.")
            return False

        household_name = None
        for household, details in data["households"].items():
            if username in details["members"]:
                household_name = household
                break
        if not household_name:
            logging.error(f"User '{username}' not found in any household.")
            return False

        if "streaks" not in data:
            data["streaks"] = {}
        if username not in data["streaks"]:
            data["streaks"][username] = {}

        last_completed = habit.get("last_completed_at")
        now = datetime.now()
        reset_threshold = timedelta(days=1 if habit["periodicity"] == "daily" else 7)

        if last_completed:
            last_completed_date = datetime.fromisoformat(last_completed)
            if now - last_completed_date > reset_threshold:
                data["streaks"][username][habit_name] = 1
            else:
                data["streaks"][username][habit_name] += 1
        else:
            data["streaks"][username][habit_name] = 1  

        streak_bonus = (data["streaks"][username][habit_name] // 7) * 10
        points = habit["points"] + streak_bonus

        user_data = data["households"][household_name]["points"]
        user_data[username] += habit["points"]
        DataManager.save_data(data)

        user = User(username, household_name, data["households"][household_name]["points"][username])
        Leaderboard().update(user)

        logging.info(f"Habit '{habit_name}' completed by {username}. Streak: {data['streaks'][username][habit_name]}. Points earned: {points}.")
        return True


    @staticmethod
    def claim_bonus_habit(username, habit_name):
        """Claim a bonus habit (only once per period)."""
        data = DataManager.load_data()

        household_name = None
        for household, details in data["households"].items():
            if username in details["members"]:
                household_name = household
                break

        if not household_name:
            logging.warning(f"User '{username}' not found.")
            return False

        habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        if not habit or not habit.get("is_bonus", False):
            logging.warning(f"Habit '{habit_name}' is not a bonus habit.")
            return False

        current_period = datetime.now().strftime("%Y-%m-%d") if habit["periodicity"] == "daily" else datetime.now().strftime("%Y-%W")

        if "completed_habits" not in data:
            data["completed_habits"] = {}
        if current_period not in data["completed_habits"]:
            data["completed_habits"][current_period] = {}

        print(f"DEBUG: Current Period = {current_period}")
        print(f"DEBUG: Completed Habits = {data['completed_habits']}")

        if habit_name in data["completed_habits"][current_period]:
            logging.warning(f"Bonus habit '{habit_name}' has already been claimed this period.")
            return False

        user_data = data["households"][household_name]["points"]
        user_data[username] += habit["points"]
    
        data["completed_habits"][current_period][habit_name] = username  
        DataManager.save_data(data)

        user = User(username, household_name, user_data[username])
        Leaderboard().update(user)

        logging.info(f"Bonus Habit '{habit_name}' claimed by {username}. Points: {habit['points']}.")
        return True

                 
    @staticmethod
    def reset_monthly_scores():
        """Resets user scores at the beginning of each month."""
        data = DataManager.load_data()
        for household in data["households"].values():
            for user in household["points"]:
                household["points"][user] = 0
        DataManager.save_data(data)

    @staticmethod
    def load_habits():
        """Loads all habits (regular and bonus)."""
        data = DataManager.load_data()
        return data.get("habits", []) + data.get("bonus_habits", [])
    
    @staticmethod
    def get_habit(habit_name):
        """Fetch a single habit from stored data."""
        data = DataManager.load_data()
    
        habit = next((h for h in data["habits"] if h["name"] == habit_name), None)
        if habit:
            return habit
    
        habit = next((h for h in data["bonus_habits"] if h["name"] == habit_name), None)
        return habit

    @staticmethod
    def reset_habits():
        """Reset habits based on their periodicity (daily/weekly)."""
        data = DataManager.load_data()
        for habit in data["habits"] + data["bonus_habits"]:
            if habit["periodicity"] == "daily":
                habit["last_completed_at"] = None
            elif habit["periodicity"] == "weekly":
                habit["last_completed_at"] = None
        DataManager.save_data(data)

    @staticmethod
    def clear_data():
        """Clears the contents of the data.json file."""
        with open(DataManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump({
                "households": {},
                "habits": [],
                "bonus_habits": [],
                "leaderboard": {"rankings": {}, "past_rankings": []}
            }, file, indent=4)
        logging.info("data.json has been cleared.")

    from datetime import datetime, timedelta

