import pytest
from classes.user import User
from classes.household import Household
from classes.habit import Habit

@pytest.fixture
def household():
    return Household("Test Household")

@pytest.fixture
def user(household):
    return User("test_user", household)

def test_add_points(user):
    user.add_points(10)
    assert user.points == 10
