import pytest
from classes.habit import Habit
from classes.user import User
from classes.household import Household

@pytest.fixture
def habit():
    return Habit(name="Exercise", periodicity="daily", points=5)

@pytest.fixture
def user():
    household = Household("Test Household")
    return User("test_user", household)


