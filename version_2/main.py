"""
Fitness App v2.0 - Main Entry Point

A professional fitness tracking application with user authentication,
workout logging, meal planning, and progress tracking.

Author: Princess Okafor
Version: 2.0
"""

"""
Fitness App v2.0 - Main Entry Point
"""

from typing import Optional
import sys
from src.fitness_app.ui.auth_menu import AuthMenu
from src.fitness_app.ui.main_menu import MainMenu  # ← ADD THIS IMPORT


def main() -> None:
    """Main application entry point."""
    print("🚀 Starting Fitness World v2.0...")

    try:
        # Initialize authentication menu
        auth_menu = AuthMenu()

        # Handle authentication flow
        current_user = auth_menu.show_auth_menu()

        if current_user:
            print(f"\n🎯 Authentication successful! User: {current_user}")

            # 🔥 LAUNCH THE MAIN MENU WITH API FEATURES!
            main_menu = MainMenu(current_user)
            main_menu.show_main_menu()

        else:
            print("\n👋 No user logged in. Exiting application.")

    except KeyboardInterrupt:
        print("\n\n🛑 Application interrupted by user.")
        print("👋 Thank you for using Fitness World!")

    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("🚨 Please contact support if this issue persists.")

    finally:
        print("\n🏁 Application ended.")
        sys.exit(0)


if __name__ == "__main__":
    main()
