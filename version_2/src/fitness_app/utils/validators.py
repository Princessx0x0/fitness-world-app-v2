"""
Validation utilities for Fitness App v2.0

This module contains validation classes for user input validation
across the application.
"""

from typing import Tuple


class MenuValidator:
    """
    Handles validation for menu choices and user interface input.

    This class contains static methods for validating menu selections
    and other UI-related input validation.
    """

    @staticmethod
    def validate_menu_choice(choice: str, min_choice: int = 1, max_choice: int = 3) -> int:
        """
        Validate menu choice is within valid range.

        Args:
            choice (str): User's menu choice as string
            min_choice (int): Minimum valid choice. Defaults to 1
            max_choice (int): Maximum valid choice. Defaults to 3

        Returns:
            int: Validated choice as integer

        Raises:
            ValueError: If choice is invalid or out of range
        """
        if not isinstance(choice, str):
            raise ValueError("Choice must be a string")

        try:
            choice_int = int(choice.strip())
        except ValueError:
            raise ValueError("Please enter a valid number")

        if choice_int < min_choice or choice_int > max_choice:
            raise ValueError(
                f"Please choose a number between {min_choice}-{max_choice}")

        return choice_int

    @staticmethod
    def validate_yes_no(response: str) -> bool:
        """
        Validate yes/no response and convert to boolean.

        Args:
            response (str): User's yes/no response

        Returns:
            bool: True for yes responses, False for no responses

        Raises:
            ValueError: If response is not a valid yes/no
        """
        if not isinstance(response, str):
            raise ValueError("Response must be a string")

        cleaned = response.strip().lower()

        yes_responses = ['y', 'yes', 'true', '1']
        no_responses = ['n', 'no', 'false', '0']

        if cleaned in yes_responses:
            return True
        elif cleaned in no_responses:
            return False
        else:
            raise ValueError("Please respond with yes (y) or no (n)")


class UserValidator:
    """
    Handles validation for user-related data.

    This class contains static methods for validating usernames, names,
    age, weight, and other user profile information.
    """

    @staticmethod
    def validate_username(username: str) -> str:
        """
        Validate and clean username.

        Args:
            username (str): Username to validate

        Returns:
            str: Cleaned username (lowercased, stripped)

        Raises:
            ValueError: If username is invalid
        """
        if not isinstance(username, str):
            raise ValueError("Username must be a string")

        cleaned = username.strip().lower()

        if len(cleaned) < 3:
            raise ValueError("Username too short (minimum 3 characters)")
        elif len(cleaned) > 20:
            raise ValueError("Username too long (maximum 20 characters)")
        elif not cleaned.isalnum():
            raise ValueError("Username can only contain letters and numbers")

        return cleaned

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Validate and clean full name.

        Args:
            name (str): Name to validate

        Returns:
            str: Cleaned name (title cased, stripped)

        Raises:
            ValueError: If name is invalid
        """
        if not isinstance(name, str):
            raise ValueError("Name must be a string")

        cleaned = name.strip().title()

        if len(cleaned) < 2:
            raise ValueError("Name too short (minimum 2 characters)")
        elif len(cleaned) > 50:
            raise ValueError("Name too long (maximum 50 characters)")
        elif not cleaned.replace(" ", "").isalpha():
            raise ValueError("Name can only contain letters and spaces")

        return cleaned

    @staticmethod
    def validate_age(age_str: str) -> int:
        """
        Validate age input and convert to integer.

        Args:
            age_str (str): Age as string input

        Returns:
            int: Validated age as integer

        Raises:
            ValueError: If age is invalid
        """
        if not isinstance(age_str, str):
            raise ValueError("Age must be provided as string")

        try:
            age = int(age_str.strip())
        except ValueError:
            raise ValueError("Age must be a valid number")

        if age < 13:
            raise ValueError("Age too young (minimum 13 years)")
        elif age > 100:
            raise ValueError("Age too high (maximum 100 years)")

        return age

    @staticmethod
    def validate_weight(weight_str: str) -> float:
        """
        Validate weight input and convert to float.

        Args:
            weight_str (str): Weight as string input

        Returns:
            float: Validated weight as float

        Raises:
            ValueError: If weight is invalid
        """
        if not isinstance(weight_str, str):
            raise ValueError("Weight must be provided as string")

        try:
            weight = float(weight_str.strip())
        except ValueError:
            raise ValueError("Weight must be a valid number")

        if weight <= 2:
            raise ValueError("Weight must be greater than 2kg")
        elif weight > 1000:
            raise ValueError("Weight too high (maximum 1000kg)")

        return weight
