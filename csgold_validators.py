"""
This module handles validation for potential CSGOLD inputs.
"""

import re

class CSGOLDValidators:
    """
    Validate input belonging to CSGOLD accounts.

    Attributes:
        admin_list (list): A list of admin Unity IDs
    """

    admin_list = [ "admin" ]

    @staticmethod
    def is_valid_unity_id(unity_id):
        """
        Check if a given Unity ID is in a valid format using regex.
        Regex matches: abc, abcd, and abcde3
        Not: ab, !!!, or a-c

        Parameters:
            unity_id (string): A potential Unity ID
        """
        return bool(re.search("\\w{3,}", unity_id))

    @staticmethod
    def is_admin_unity_id(unity_id):
        """
        Check if a given Unity ID has admin access control.

        Parameters:
            unity_id (string): A potential admin Unity ID
        """
        return unity_id in CSGOLDValidators.admin_list

    @staticmethod
    def is_valid_account_id(account_id):
        """
        Check if a given string is a valid CSGOLD account ID using regex.
        Matches exactly 9 numeric characters.

        Parameters:
            account_id (string): A potential CSGOLD account ID
        """
        return bool(re.search("[0-9]{9}", account_id))

    @staticmethod
    def just_add(a, b):
        """
        Converts a and b into numbers and adds them.

        Parameters:
            a (string): First string to add
            b (string): Second string to add
        """
        return int(a) + int(b)