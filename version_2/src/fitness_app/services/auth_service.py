"""
   Authentication service for Fitness App v2.0

   This module handles user authentication, account creation, session management,
   and security operations for the fitness application.
   """

from typing import Dict, Optional, Tuple, Any
from datetime import datetime
import hashlib
import json
import os


class AuthService:
    """
    Professional authentication service for managing user login and registration.

    This service handles all authentication-related operations including
    user registration, login validation, session management, and security.

    Attributes:
        current_user (Optional[str]): Username of currently logged in user
        session_active (bool): Whether a user session is currently active
        users_file_path (str): Path to the users data file
    """

    def __init__(self, users_file_path: str = "data/users.json") -> None:
        """
        Initialize the authentication service.

        Args:
            users_file_path (str): Path to users data file. Defaults to "data/users.json"
        """
        self.current_user: Optional[str] = None
        self.session_active: bool = False
        self.users_file_path: str = users_file_path
        self._ensure_users_file_exists()

    def _ensure_users_file_exists(self) -> None:
        """
        Ensure the users data file exists, create if it doesn't.

        Creates an empty JSON file with an empty user dictionary if the
        users file doesn't exist.
        """
        if not os.path.exists(self.users_file_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.users_file_path), exist_ok=True)

            # Create empty users file
            with open(self.users_file_path, 'w') as file:
                json.dump({}, file, indent=2)

    def _hash_password(self, password: str) -> str:
        """
        Hash a password using SHA-256 for secure storage.

        Args:
            password (str): Plain text password to hash

        Returns:
            str: Hashed password as hexadecimal string
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password (str): Plain text password to verify
            hashed_password (str): Stored hashed password

        Returns:
            bool: True if password matches, False otherwise
        """
        return self._hash_password(password) == hashed_password

    def _load_users(self) -> Dict[str, Any]:
        """
        Load user data from the JSON file.

        Returns:
            Dict[str, Any]: Dictionary containing all user data

        Raises:
            FileNotFoundError: If users file cannot be found
            json.JSONDecodeError: If users file contains invalid JSON
        """
        try:
            with open(self.users_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Users file not found: {self.users_file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in users file: {e}")

    def _save_users(self, users_data: Dict[str, Any]) -> None:
        """
        Save user data to the JSON file.

        Args:
            users_data (Dict[str, Any]): User data dictionary to save

        Raises:
            IOError: If file cannot be written
        """
        try:
            with open(self.users_file_path, 'w') as file:
                json.dump(users_data, file, indent=2)
        except IOError as e:
            raise IOError(f"Cannot write to users file: {e}")

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate a user with username and password.

        Args:
            username (str): Username to authenticate
            password (str): Plain text password

        Returns:
            Tuple[bool, str]: (success, message)
                - success: True if login successful, False otherwise
                - message: Success message or error description
        """
        try:
            users_data = self._load_users()

            # Check if username exists
            if username not in users_data:
                return False, "Username not found"

            # Verify password
            stored_hash = users_data[username]["password_hash"]
            if not self._verify_password(password, stored_hash):
                return False, "Invalid password"

            # Start session
            self.current_user = username
            self.session_active = True

            return True, f"Welcome back, {users_data[username]['name']}!"

        except Exception as e:
            return False, f"Login error: {str(e)}"

    def create_account(self, username: str, password: str, name: str,
                       age: int, weight: float, target_weight: Optional[float] = None,
                       weekly_workout_goal: int = 3) -> Tuple[bool, str]:
        """
        Create a new user account with provided information.

        Args:
            username (str): Unique username for the account
            password (str): Plain text password (will be hashed)
            name (str): Full name of the user
            age (int): Age in years
            weight (float): Current weight in kg
            target_weight (Optional[float]): Goal weight in kg. Defaults to current weight
            weekly_workout_goal (int): Weekly workout target. Defaults to 3

        Returns:
            Tuple[bool, str]: (success, message)
                - success: True if account created, False if error
                - message: Success message or error description
        """
        try:
            users_data = self._load_users()

            # Check if username already exists
            if username in users_data:
                return False, "Username already exists. Please choose a different username."

            # Set target weight to current weight if not provided
            if target_weight is None:
                target_weight = weight

            # Create new user data
            new_user = {
                "username": username,
                "password_hash": self._hash_password(password),
                "name": name,
                "age": age,
                "weight": weight,
                "target_weight": target_weight,
                "weekly_workout_goal": weekly_workout_goal,
                "workouts": [],
                "meals": [],
                "created_date": datetime.now().strftime("%B %d, %Y"),
                "last_login": datetime.now().strftime("%B %d, %Y at %I:%M %p")
            }

            # Add user to data and save
            users_data[username] = new_user
            self._save_users(users_data)

            # Auto-login the new user
            self.current_user = username
            self.session_active = True

            return True, f"Account created successfully! Welcome to Fitness World, {name}!"

        except Exception as e:
            return False, f"Account creation error: {str(e)}"

    def logout(self) -> Tuple[bool, str]:
        """
        Log out the current user and end the session.

        Returns:
            Tuple[bool, str]: (success, message)
                - success: True if logout successful, False if no active session
                - message: Logout confirmation or error message
        """
        if not self.session_active or self.current_user is None:
            return False, "No active session to logout"

        username = self.current_user
        self.current_user = None
        self.session_active = False

        return True, f"Successfully logged out. Goodbye!"

    def get_current_user(self) -> Optional[str]:
        """
        Get the username of the currently logged in user.

        Returns:
            Optional[str]: Username if session active, None otherwise
        """
        return self.current_user if self.session_active else None

    def is_session_active(self) -> bool:
        """
        Check if there is an active user session.

        Returns:
            bool: True if user is logged in, False otherwise
        """
        return self.session_active and self.current_user is not None

    def get_user_data(self, username: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get user data for specified user or current user.

        Args:
            username (Optional[str]): Username to get data for. 
                                    Defaults to current user if None

        Returns:
            Optional[Dict[str, Any]]: User data dictionary or None if user not found
        """
        try:
            users_data = self._load_users()
            target_user = username or self.current_user

            if target_user and target_user in users_data:
                return users_data[target_user]
            return None

        except Exception:
            return None

    def update_last_login(self) -> None:
        """
        Update the last login timestamp for the current user.
        """
        if not self.session_active or self.current_user is None:
            return

        try:
            users_data = self._load_users()
            users_data[self.current_user]["last_login"] = datetime.now().strftime(
                "%B %d, %Y at %I:%M %p")
            self._save_users(users_data)
        except Exception:
            pass  # Silently fail for non-critical operation
