"""
This module tests the validators with hypothesis data.
"""

from hypothesis import given, example
from hypothesis.strategies import text, integers
from csgold_validators import CSGOLDValidators as validators

@given(unity_id=text())
@example(unity_id="abc")
@example(unity_id="abcdefg8")
def test_is_valid_unity_id(unity_id):
    """
    Test the Unity ID validator with random text inputs.
    """
    result = validators.is_valid_unity_id(unity_id)
    print(unity_id, result)
    assert result is True or result is False

@given(unity_id=text())
@example("admin")
@example("")
def test_is_admin_unity_id(unity_id):
    """
    Test the admin validator with random text inputs.
    """
    result = validators.is_admin_unity_id(unity_id)
    print(unity_id, result)
    if unity_id == "admin":
        assert result is True
    assert result is True or result is False

@given(account_id=text())
@example("1234")
def test_is_valid_account_id(account_id):
    """
    Test the Account ID validator with random text inputs.
    """
    result = validators.is_valid_account_id(account_id)
    print(account_id, result)
    assert result is True or result is False

@given(a=integers(), b=integers())
def test_just_add(a, b):
    """
    Test the adding of two strings.
    """
    result = validators.just_add(a, b)
    print(a, b, result)
    assert isinstance(result, int)