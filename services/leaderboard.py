from datetime import datetime
import logging
import json

DATA_FILE = "data.json"

class Leaderboard:
    def __init__(self):
        self.data = self.load_data()  
        self.rankings = self.data["leaderboard"]["rankings"]
        self.past_rankings = self.data["leaderboard"]["past_rankings"]
        self.top_performers = {}

    def load_data(self):
        """Load the full data.json file or create a default structure if empty."""
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if content:  
                    return json.loads(content)
                else:
                    logging.warning("data.json was empty, initializing default structure.")
                    return {
                        "households": {},
                        "habits": [],
                        "bonus_habits": [],
                        "leaderboard": {"rankings": {}, "past_rankings": []},
                        "streaks": {},
                    }
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.warning(f"Error loading data.json: {e}")
            return {
                "households": {},
                "habits": [],
                "bonus_habits": [],
                "leaderboard": {"rankings": {}, "past_rankings": []},
                "streaks": {},
            }


    def save_data(self):
        """Save leaderboard updates back to data.json."""
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    @staticmethod
    def update(user):
        from services.data_manager import DataManager
        """Update the leaderboard rankings after a user's points change."""
        data = DataManager.load_data()

        household_name = user.household
        if household_name not in data["leaderboard"]["rankings"]:
            data["leaderboard"]["rankings"][household_name] = {}

        data["leaderboard"]["rankings"][household_name][user.username] = user.points

        sorted_rankings = dict(sorted(
            data["leaderboard"]["rankings"][household_name].items(),
            key=lambda item: item[1],  
            reverse=True  
        ))
        data["leaderboard"]["rankings"][household_name] = sorted_rankings

        DataManager.save_data(data)

        logging.info(f"Leaderboard updated for {household_name}: {sorted_rankings}")

    def reset_monthly(self):
        """Resets rankings at the end of each month, storing past rankings."""
        now = datetime.now().strftime('%m-%Y')

        self.past_rankings.append({
            "month": now,
            "rankings": self.rankings.copy()
        })

        all_scores = [(user, points) for household in self.rankings.values() for user, points in household.items()]
        if all_scores:
            top_user, top_points = max(all_scores, key=lambda x: x[1])
            self.data["leaderboard"]["past_rankings"].append({"month": now, "top_user": top_user, "points": top_points})

        self.rankings.clear()
        self.save_data()

    def get_sorted_rankings(self, household_name):
        """Returns sorted rankings for a household."""
        if household_name not in self.rankings:
            logging.warning(f"No rankings found for household '{household_name}'.")
            return {}
        return dict(sorted(self.rankings[household_name].items(), key=lambda item: item[1], reverse=True))

    def get_top_performers(self):
        """Returns the top user for each month with their score."""
        return self.data["leaderboard"]["past_rankings"]
