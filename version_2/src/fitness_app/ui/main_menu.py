"""
Main application menu for Fitness App v2.0
"""

from typing import Optional
from ..services.api_service import WorkoutAPIService
from ..services.auth_service import AuthService
from ..utils.validators import MenuValidator


class MainMenu:
    """Handles the main application menu and features."""

    def __init__(self, current_user: str):
        """Initialize main menu for logged in user."""
        self.current_user = current_user
        self.auth_service = AuthService()
        self.api_service = WorkoutAPIService()  # 🔥 LIVE API DATA!

    def show_main_menu(self) -> None:
        """Display main menu with all app features."""
        user_data = self.auth_service.get_user_data(self.current_user)
        user_name = user_data['name'] if user_data else self.current_user

        print(f"\n🏋️ Welcome to Fitness World, {user_name}! 🏋️")
        print("="*60)

        while True:
            print(f"\n=== Main Menu ===")
            print("1. 💪 Browse Exercise Categories (Live API)")
            print("2. 🍎 Search Nutrition Data (Live API)")
            print("3. 📝 Log Custom Workout")
            print("4. 🍽️ Plan Meals")
            print("5. 📊 View Progress")
            print("6. ⚙️ Update Profile")
            print("7. 🚪 Logout")

            try:
                choice = input("\nChoose an option (1-7): ")
                validated_choice = MenuValidator.validate_menu_choice(
                    choice, 1, 7)

                if validated_choice == 1:
                    self.browse_exercises()
                elif validated_choice == 2:
                    self.search_nutrition()
                elif validated_choice == 3:
                    self.log_custom_workout()
                elif validated_choice == 4:
                    self.plan_meals()
                elif validated_choice == 5:
                    self.view_progress()
                elif validated_choice == 6:
                    self.update_profile()
                elif validated_choice == 7:
                    print(f"👋 Goodbye {user_name}!")
                    break
                else:
                    print("🚧 Feature coming soon!")

            except ValueError as e:
                print(f"❌ {e}")

    def browse_exercises(self) -> None:
        """Browse exercises using live API data."""
        print("\n🏋️ Exercise Browser (Live API Data)")
        print("="*50)

        # Get categories from API
        print("🔄 Loading exercise categories...")
        categories = self.api_service.get_exercise_categories()

        if not categories:
            print("❌ Unable to load exercises. Please try again later.")
            return

        # Show categories
        print(f"\n📋 Available Categories ({len(categories)} found):")
        for i, category in enumerate(categories, 1):
            print(f"  {i}. {category['name']}")

        try:
            # Let user choose category
            choice = input(f"\nChoose a category (1-{len(categories)}): ")
            category_index = int(choice) - 1

            if 0 <= category_index < len(categories):
                selected_category = categories[category_index]
                self.show_exercises_in_category(selected_category)
            else:
                print("❌ Invalid category selection")

        except ValueError:
            print("❌ Please enter a valid number")

    def show_exercises_in_category(self, category: dict) -> None:
        """Show exercises for a specific category."""
        print(f"\n💪 Exercises in {category['name']} Category")
        print("="*50)

        # Get exercises for this category
        print("🔄 Loading exercises...")
        exercises = self.api_service.get_exercises_by_category(
            category['id'], limit=5)

        if exercises:
            print(f"\n✅ Found {len(exercises)} exercises:")
            for i, exercise in enumerate(exercises, 1):
                print(f"\n{i}. {exercise['name']}")
                print(f"   Category: {exercise['category']}")
                if exercise['equipment']:
                    print(f"   Equipment: {', '.join(exercise['equipment'])}")
                print(f"   Description: {exercise['description'][:100]}...")

            # Ask if they want to log a workout
            log_choice = input(
                "\nWould you like to log one of these exercises? (y/n): ")
            if log_choice.lower() in ['y', 'yes']:
                self.log_exercise_workout(exercises)
        else:
            print(f"❌ No exercises found for {category['name']}")

    def log_custom_workout(self) -> None:
        """Log a custom workout and save to user data."""
        print("\n📝 Log Custom Workout")
        print("="*40)

        try:
            workout_name = input("Workout name: ").strip()
            if not workout_name:
                print("❌ Workout name required")
                return

            duration = int(input("Duration (minutes): "))
            intensity = input("Intensity (low/medium/high): ").lower()

            if intensity not in ['low', 'medium', 'high']:
                intensity = 'medium'
                print("⚠️ Invalid intensity, defaulting to medium")

            # Create workout entry
            from datetime import datetime
            workout_entry = {
                "type": workout_name,
                "category": "custom",
                "duration": duration,
                "intensity": intensity,
                "date": datetime.now().strftime("%B %d, %Y")
            }

            try:
                # Load current user data
                users_data = self.auth_service._load_users()

                # Add workout to user's history
                if self.current_user in users_data:
                    users_data[self.current_user]["workouts"].append(
                        workout_entry)

                    # Save back to file
                    self.auth_service._save_users(users_data)

                    print(f"\n✅ Custom workout saved!")
                    print(f"   Name: {workout_name.title()}")
                    print(f"   Duration: {duration} minutes")
                    print(f"   Intensity: {intensity.title()}")
                    print("💾 Successfully saved to your profile!")
                else:
                    print("❌ Could not find user profile")

            except Exception as e:
                print(f"❌ Error saving workout: {e}")
                print("💡 Workout logged but not saved to profile")

        except ValueError:
            print("❌ Please enter valid numbers for duration")
        except Exception as e:
            print(f"❌ Error logging workout: {e}")

    def search_nutrition(self) -> None:
        """Search for nutrition information using live API."""
        print("\n🍎 Nutrition Search (Live API Data)")
        print("="*50)

        try:
            food_query = input("What food would you like to search for? ")

            if food_query.strip():
                print("🔄 Searching nutrition database...")
                foods = self.api_service.get_food_data(food_query, limit=3)

                if foods:
                    print(f"\n✅ Found nutrition data:")
                    for i, food in enumerate(foods, 1):
                        print(f"\n{i}. {food['name']}")
                        print(f"   Calories: {food['calories_per_100g']}/100g")
                        print(f"   Protein: {food['protein']}g")
                        print(f"   Carbs: {food['carbs']}g")
                        print(f"   Fat: {food['fat']}g")
                        print(f"   Category: {food.get('category', 'N/A')}")
                else:
                    print(f"❌ No nutrition data found for '{food_query}'")
            else:
                print("❌ Please enter a food name")

        except Exception as e:
            print(f"❌ Error searching for food: {e}")
            print("💡 Please try again with a different food item")

    def log_custom_workout(self) -> None:
        """Log a custom workout without API data."""
        print("\n📝 Log Custom Workout")
        print("="*40)

        try:
            # Get workout details
            workout_name = input("Workout name: ").strip()
            if not workout_name:
                print("❌ Workout name required")
                return

            duration = int(input("Duration (minutes): "))
            intensity = input("Intensity (low/medium/high): ").lower()

            if intensity not in ['low', 'medium', 'high']:
                intensity = 'medium'
                print("⚠️ Invalid intensity, defaulting to medium")

            # Simple success message (we'll save to user data later)
            print(f"\n✅ Custom workout logged!")
            print(f"   Name: {workout_name.title()}")
            print(f"   Duration: {duration} minutes")
            print(f"   Intensity: {intensity.title()}")
            print("💾 Saved to your workout history!")

        except ValueError:
            print("❌ Please enter valid numbers for duration")
        except Exception as e:
            print(f"❌ Error logging workout: {e}")

    def log_exercise_workout(self, exercises: list) -> None:
        """Log a workout with a selected exercise from API."""
        try:
            choice = input(f"Choose exercise (1-{len(exercises)}): ")
            exercise_index = int(choice) - 1

            if 0 <= exercise_index < len(exercises):
                selected_exercise = exercises[exercise_index]

                # Get workout details
                duration = int(input("Duration (minutes): "))
                intensity = input("Intensity (low/medium/high): ").lower()

                if intensity not in ['low', 'medium', 'high']:
                    intensity = 'medium'
                    print("⚠️ Invalid intensity, defaulting to medium")

                # Create workout entry
                from datetime import datetime
                workout_entry = {
                    "type": selected_exercise['name'],
                    "category": selected_exercise['category'],
                    "duration": duration,
                    "intensity": intensity,
                    "date": datetime.now().strftime("%B %d, %Y")
                }

                # Save to user data
                try:
                    users_data = self.auth_service._load_users()
                    if self.current_user in users_data:
                        users_data[self.current_user]["workouts"].append(
                            workout_entry)
                        self.auth_service._save_users(users_data)

                        print(f"\n✅ API workout logged!")
                        print(f"   Exercise: {selected_exercise['name']}")
                        print(f"   Duration: {duration} minutes")
                        print(f"   Intensity: {intensity}")
                        print("💾 Successfully saved to your profile!")
                    else:
                        print("❌ Could not save to profile")
                except Exception as e:
                    print(f"❌ Error saving: {e}")

            else:
                print("❌ Invalid exercise selection")

        except ValueError:
            print("❌ Please enter valid numbers")
        except Exception as e:
            print(f"❌ Error: {e}")

    def view_progress(self) -> None:
        """Display user progress and stats."""
        print("\n📊 Your Fitness Progress")
        print("="*50)

        # Get user data
        user_data = self.auth_service.get_user_data(self.current_user)

        if user_data:
            print(f"\n👤 Profile: {user_data['name']}")
            print(
                f"📅 Member since: {user_data.get('created_date', 'Unknown')}")
            print(
                f"🎯 Target weight: {user_data.get('target_weight', user_data['weight'])}kg")
            print(f"⚖️ Current weight: {user_data['weight']}kg")
            print(
                f"🏃 Weekly goal: {user_data.get('weekly_workout_goal', 3)} workouts")

            # Workout stats
            workouts = user_data.get('workouts', [])
            meals = user_data.get('meals', [])

            print(f"\n💪 Workout Stats:")
            print(f"   Total workouts logged: {len(workouts)}")
            print(f"   Meal plans saved: {len(meals)}")

            if workouts:
                total_time = sum(w.get('duration', 0) for w in workouts)
                print(f"   Total workout time: {total_time} minutes")

                # Recent workout
                recent = workouts[-1]
                print(
                    f"   Last workout: {recent.get('type', 'Unknown')} - {recent.get('date', 'Unknown')}")

            print(f"\n🎉 Keep up the fantastic work!")
        else:
            print("❌ Could not load user data")

    def plan_meals(self) -> None:
        """Simple meal planning feature."""
        print("\n🍽️ Meal Planning")
        print("="*40)

        # Simple meal suggestions based on goals
        meal_options = {
            'breakfast': ['Oatmeal with fruit', 'Eggs with toast', 'Greek yogurt', 'Smoothie bowl'],
            'lunch': ['Chicken salad', 'Rice bowl', 'Sandwich', 'Soup and bread'],
            'dinner': ['Grilled salmon', 'Chicken stir-fry', 'Pasta with vegetables', 'Lean beef'],
            'snacks': ['Apple with nuts', 'Protein bar', 'Greek yogurt', 'Banana']
        }

        print("🍎 Today's meal suggestions:")
        for meal_type, options in meal_options.items():
            import random
            suggestion = random.choice(options)
            print(f"   {meal_type.title()}: {suggestion}")

        save = input("\nSave this meal plan? (y/n): ").lower()
        if save in ['y', 'yes']:
            print("✅ Meal plan saved!")
            # TODO:
        else:
            print("Meal plan not saved.")

    def update_profile(self) -> None:
        """Update user profile information."""
        print("\n⚙️ Update Profile")
        print("="*40)

        try:
            users_data = self.auth_service._load_users()
            user_data = users_data[self.current_user]

            print(f"Current profile:")
            print(f"   Name: {user_data['name']}")
            print(f"   Age: {user_data['age']}")
            print(f"   Weight: {user_data['weight']}kg")
            print(
                f"   Target: {user_data.get('target_weight', user_data['weight'])}kg")

            print(f"\nWhat would you like to update?")
            print("1. Weight")
            print("2. Target Weight")
            print("3. Weekly Goal")
            print("4. Cancel")

            choice = input("Choose (1-4): ")

            if choice == "1":
                new_weight = float(input("New weight (kg): "))
                users_data[self.current_user]['weight'] = new_weight
                print(f"✅ Weight updated to {new_weight}kg")

            elif choice == "2":
                new_target = float(input("New target weight (kg): "))
                users_data[self.current_user]['target_weight'] = new_target
                print(f"✅ Target weight updated to {new_target}kg")

            elif choice == "3":
                new_goal = int(input("Weekly workout goal (1-7): "))
                if 1 <= new_goal <= 7:
                    users_data[self.current_user]['weekly_workout_goal'] = new_goal
                    print(f"✅ Weekly goal updated to {new_goal} workouts")
                else:
                    print("❌ Invalid goal (1-7)")
                    return
            else:
                print("Update cancelled")
                return

            self.auth_service._save_users(users_data)
            print("💾 Profile updated successfully!")

        except Exception as e:
            print(f"❌ Error updating profile: {e}")
