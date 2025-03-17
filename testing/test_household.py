import pytest
from classes.household import Household
from classes.user import User

@pytest.fixture
def household():
    return Household("Test Household")

@pytest.fixture
def user(household):
    return User("test_user", household)

def test_add_member(household, user):
    household.add_member(user)
    assert len(household.members) == 1
