"""
Authentication menu for Fitness App v2.0
"""

from typing import Optional
import sys
from ..services.auth_service import AuthService
from ..utils.validators import UserValidator, MenuValidator


class AuthMenu:
    """Authentication menu handler."""

    def __init__(self) -> None:
        """Initialize auth menu."""
        self.auth_service = AuthService()

    def show_auth_menu(self) -> Optional[str]:
        """Show authentication menu."""
        print("\n🏋️ WELCOME TO FITNESS WORLD v2.0! 🏋️")

        while True:
            print("\n=== Authentication Menu ===")
            print("1. Login")
            print("2. Create Account")
            print("3. Exit")

            choice = input("Choose (1-3): ")

            if choice == "1":
                return self.handle_login()
            elif choice == "2":
                return self.handle_signup()
            elif choice == "3":
                print("Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice!")

    def handle_login(self) -> Optional[str]:
        """Handle user login."""
        print("\n=== User Login ===")

        try:
            # Get username
            username = input("Enter username: ").strip()
            if not username:
                print("❌ Username cannot be empty")
                return None

            # Get password
            password = input("Enter password: ").strip()
            if not password:
                print("❌ Password cannot be empty")
                return None

            # Attempt login
            success, message = self.auth_service.login(username, password)

            if success:
                print(f"✅ {message}")
                return username
            else:
                print(f"❌ {message}")

                # Offer to create account if username not found
                if "Username not found" in message:
                    create = input(
                        "Would you like to create an account? (y/n): ")
                    if create.lower() in ['y', 'yes']:
                        return self.handle_signup()

                return None

        except Exception as e:
            print(f"❌ Login error: {e}")
            return None

    def handle_signup(self) -> Optional[str]:
        """Handle account creation."""
        print("\n=== Create New Account ===")

        try:
            # Get username
            username_input = input("Enter username (3-20 characters): ")
            username = UserValidator.validate_username(username_input)

            # Get password
            while True:
                password = input("Enter password (min 6 characters): ").strip()
                if len(password) < 6:
                    print("❌ Password must be at least 6 characters long")
                    continue

                confirm_password = input("Confirm password: ").strip()
                if password != confirm_password:
                    print("❌ Passwords don't match. Please try again.")
                    continue

                print("✅ Password confirmed!")
                break

            # Get name
            name_input = input("Enter your full name: ")
            name = UserValidator.validate_name(name_input)

            # Get age
            age_input = input("Enter your age: ")
            age = UserValidator.validate_age(age_input)

            # Get weight
            weight_input = input("Enter weight (kg): ")
            weight = UserValidator.validate_weight(weight_input)

            # Create account
            success, message = self.auth_service.create_account(
                username=username,
                password=password,
                name=name,
                age=age,
                weight=weight
            )

            if success:
                print(f"✅ {message}")
                return username
            else:
                print(f"❌ {message}")
                return None

        except ValueError as e:
            print(f"❌ {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
