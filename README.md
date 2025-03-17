# Home-Streak

This is a fun command-line habit tracker designed to promote healthy habits within the family through game-like point system. The tracker allows individual users to join a household and compete amongst each other by gaining points for each habit they complete.

Features

    •	Track daily and weekly habits
    •	Earn points for every habit you complete
    •	Bonus habits that are worth more points and work on a first-come, first-served basis
    •	Rewards for steaks
    •	Household leaderboard that allows you to compete with your family members
    •	Persistent JSON data storage 
    •	Simple and efficient habit management through the Command-Line Interface (CLI)
    •	Analytics module to gain insights into habits

Installation

    Prerequisites:
    
        Ensure you have Python 3.11+ and a pip package manager installed.

    Setup
    
    1.	Clone the repository:
	        git clone https://github.com/Kris05lv/Home-Streak.git
         
    2.	Create a virtual environment (optional but recommended)
            python -m venv venv
            
        •	Activate your environment
        
	        .\venv\Scripts\activate (Windows)
	        source venv/bin/activate (macOS/Linux)
         
    3.	Install dependencies
	        pip install -r dependencies.txt

Usage

    Run the application
        python cli.py [OPTIONS] COMMAND [ARGS]

    Options Habit Tracker CLI
        To show this message and exit use --help 

    Commands:
    
        Create a new household.  
        •	create-household      
        Add a user to a household.  
        •	add-user              
        Add a habit with periodicity and points.  
        •	add-habit             
        Add a bonus habit worth extra points that works on a first-come first-serve system.
        •	add-bonus-habit       
        Mark a habit as completed and update streaks. 
        •	complete-habit        
        List all habits in the system.  
        •	list-habits           
        View the leaderboard rankings for a household. 
        •	view-leaderboard      
        View past leaderboard rankings. 
        •	view-past-rankings    
        View the top performers of past months. 
        •	view-top-performers    
        Reset all users' monthly scores.
        •	reset-monthly-scores  
        Clear all data in the system (reset data.json). 
        •	clear-data   

Future enhancements:

    1. Add bonus points for extra completions. 
          i.e. you eat 2 fruits instead of the 1 required.
    2. Enhance user management.
          Implementing authentication
    3. Adding notifications.
    4. Multi-device and cloud syncing.
    5. Adding achievements and badges as rewards

