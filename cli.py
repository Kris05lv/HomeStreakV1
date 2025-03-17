import click
import logging
from services.data_manager import DataManager
from services.leaderboard import Leaderboard
from classes.user import User 
from classes.habit import Habit


logging.basicConfig(level=logging.INFO)
leaderboard = Leaderboard()

@click.group()
def cli():
    """Habit Tracker CLI"""
    pass

@click.command()
@click.argument("household_name")
def create_household(household_name):
    """Create a new household."""
    DataManager.create_household(household_name)
    click.echo(f"Household '{household_name}' created.")

@click.command()
@click.argument("username")
@click.argument("household_name")
def add_user(username, household_name):
    """Add a user to a household."""
    from classes.user import User  
    user = User(username, household_name)
    DataManager.save_user(user)
    click.echo(f"User '{username}' added to household '{household_name}'.")

@click.command()
@click.argument("name")
@click.argument("periodicity", type=click.Choice(["daily", "weekly"]))
@click.argument("points", type=int)
def add_habit(name, periodicity, points):
    """Add a habit with periodicity and points."""
    habit = Habit(name, periodicity, points)
    DataManager.save_habit(habit)
    click.echo(f"Habit '{name}' added as a {periodicity} habit worth {points} points.")


@click.command()
@click.argument("name")
@click.argument("periodicity", type=click.Choice(["daily", "weekly"]))
@click.argument("points", type=int)
def add_bonus_habit(name, periodicity, points):
    """Add a bonus habit with extra points."""
    habit = Habit(name, periodicity, points, is_bonus=True)
    DataManager.save_bonus_habit(habit)
    click.echo(f"Bonus Habit '{name}' added as a {periodicity} bonus habit worth {points} points!")


@click.command()
@click.argument("username")
@click.argument("habit_name")
def complete_habit(username, habit_name):
    """Mark a habit as completed and update streaks. Bonus habits are automatically claimed."""
    
    habit = DataManager.get_habit(habit_name)  
    if not habit:
        click.echo(f"Habit '{habit_name}' not found.")
        return

    if habit["is_bonus"]:
        success = DataManager.claim_bonus_habit(username, habit_name)
        if success:
            click.echo(f"Bonus Habit '{habit_name}' claimed by '{username}'.")
        else:
            click.echo(f"Bonus Habit '{habit_name}' is already taken or unavailable for this period.")
    else:
        success = DataManager.complete_habit(username, habit_name)
        if success:
            click.echo(f"'{habit_name}' completed by '{username}'. Points updated!")
        else:
            click.echo(f"'{habit_name}' could not be completed.")
   
@click.command()
def list_habits():
    """List all habits in the system."""
    habits = DataManager.load_habits()  
    if not habits:
        click.echo("No habits found.")
        return
    click.echo("Tracked Habits:")
    for habit in habits:
        click.echo(f"- {habit['name']} ({habit['periodicity']}, {habit['points']} points)")
        if habit['completions']:  
            click.echo(f"  Completions: {', '.join(habit['completions'])}")
        else:
            click.echo(f"  No completions yet.")

@click.command()
@click.argument("household_name")
def view_leaderboard(household_name):
    """View the leaderboard rankings for a household."""
    rankings = leaderboard.get_sorted_rankings(household_name)
    if not rankings:
        click.echo(f"No rankings available for household '{household_name}'.")
    else:
        click.echo(f"Leaderboard for '{household_name}':")
        for rank, (user, points) in enumerate(rankings.items(), start=1):
            click.echo(f"{rank}. {user}: {points} points")

@click.command()
def reset_monthly_scores():
    """Reset all users' monthly scores and track top performer."""
    leaderboard.reset_monthly()
    DataManager.reset_monthly_scores()
    click.echo("Monthly scores reset. Leaderboard archived.")

@click.command()
def view_top_performers():
    """View the top performers of past months."""
    top_performers = leaderboard.get_top_performers()
    if not top_performers:
        click.echo("No top performers recorded yet.")
    else:
        click.echo("Top Performers by Month:")
        for month, (user, points) in top_performers.items():
            click.echo(f"{month}: {user} with {points} points")

@click.command()
def view_past_rankings():
    """View past leaderboard rankings."""
    past_rankings = leaderboard.get_past_rankings()
    if not past_rankings:
        click.echo("No past rankings recorded.")
    else:
        for entry in past_rankings:
            click.echo(f"\n {entry['month']} Rankings:")
            for household, rankings in entry["rankings"].items():
                click.echo(f"Household: {household}")
                for user, points in rankings.items():
                    click.echo(f"   {user}: {points} points")

@click.command()
def clear_data():
    """Clear all data in the system (reset data.json)."""
    DataManager.clear_data()
    click.echo("All data has been cleared.")


cli.add_command(create_household)
cli.add_command(add_user)
cli.add_command(add_habit)
cli.add_command(complete_habit)
cli.add_command(view_leaderboard)
cli.add_command(reset_monthly_scores)
cli.add_command(view_top_performers)
cli.add_command(view_past_rankings)
cli.add_command(clear_data)
cli.add_command(list_habits)
cli.add_command(add_bonus_habit)

if __name__ == "__main__":
    cli()

