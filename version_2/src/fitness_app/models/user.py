"""
User model for Fitness App v2.0

This module contains the User class that represents a fitness app user
with their profile information, goals, and tracking capabilities.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime


class User:
    """
    Represents a fitness app user with profile information and tracking capabilities.

    This class manages user data including personal information, fitness goals,
    workout history, and meal planning data.

    Attributes:
        username (str): Unique identifier for the user
        name (str): Full name of the user
        age (int): Age in years
        weight (float): Current weight in kilograms
        target_weight (float): Goal weight in kilograms
        weekly_workout_goal (int): Target number of workouts per week
        workouts (List[Dict[str, Any]]): List of completed workouts
        meals (List[Dict[str, Any]]): List of saved meal plans
        created_date (str): Date when account was created
        last_login (str): Last login timestamp
    """

    def __init__(
        self,
        username: str,
        name: str,
        age: int,
        weight: float,
        target_weight: Optional[float] = None,
        weekly_workout_goal: int = 3,
        workouts: Optional[List[Dict[str, Any]]] = None,
        meals: Optional[List[Dict[str, Any]]] = None,
        created_date: Optional[str] = None,
        last_login: Optional[str] = None
    ) -> None:
        """
        Initialize a new User instance.

        Args:
            username (str): Unique username for the user
            name (str): Full name of the user
            age (int): Age in years
            weight (float): Current weight in kg
            target_weight (Optional[float]): Goal weight in kg. Defaults to current weight
            weekly_workout_goal (int): Weekly workout target. Defaults to 3
            workouts (Optional[List[Dict]]): Existing workout history
            meals (Optional[List[Dict]]): Existing meal plans
            created_date (Optional[str]): Account creation date
            last_login (Optional[str]): Last login timestamp
        """
        self.username = username
        self.name = name
        self.age = age
        self.weight = weight
        self.target_weight = target_weight if target_weight is not None else weight
        self.weekly_workout_goal = weekly_workout_goal
        self.workouts = workouts if workouts is not None else []
        self.meals = meals if meals is not None else []
        self.created_date = created_date or datetime.now().strftime("%B %d, %Y")
        self.last_login = last_login or datetime.now().strftime("%B %d, %Y at %I:%M %p")

    def add_workout(self, workout_data: Dict[str, Any]) -> None:
        """
        Add a completed workout to user's history.

        Args:
            workout_data (Dict[str, Any]): Workout information containing
                type, category, duration, intensity, and date
        """
        self.workouts.append(workout_data.copy())

    def add_meal_plan(self, meal_plan_data: Dict[str, Any]) -> None:
        """
        Add a meal plan to user's saved plans.

        Args:
            meal_plan_data (Dict[str, Any]): Meal plan information
        """
        self.meals.append(meal_plan_data.copy())

    def update_weight(self, new_weight: float) -> None:
        """
        Update user's current weight.

        Args:
            new_weight (float): New weight in kg
        """
        self.weight = new_weight

    def get_total_workout_time(self) -> int:
        """
        Calculate total workout time across all logged workouts.

        Returns:
            int: Total workout time in minutes
        """
        return sum(workout.get('duration', 0) for workout in self.workouts)

    def get_workouts_by_category(self) -> Dict[str, int]:
        """
        Count workouts by category.

        Returns:
            Dict[str, int]: Dictionary mapping category names to workout counts
        """
        category_counts = {}
        for workout in self.workouts:
            category = workout.get('category', 'unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        return category_counts

    def get_weight_progress(self) -> Dict[str, Any]:
        """
        Calculate weight progress towards goal.

        Returns:
            Dict[str, Any]: Dictionary containing progress information
        """
        difference = abs(self.weight - self.target_weight)
        direction = "lose" if self.weight > self.target_weight else "gain"
        at_goal = self.weight == self.target_weight

        return {
            "current": self.weight,
            "target": self.target_weight,
            "difference": difference,
            "direction": direction,
            "at_goal": at_goal,
            "progress_message": self._get_progress_message(at_goal, difference, direction)
        }

    def _get_progress_message(self, at_goal: bool, difference: float, direction: str) -> str:
        """
        Generate a friendly progress message.

        Args:
            at_goal (bool): Whether user is at their goal weight
            difference (float): Weight difference from goal
            direction (str): Direction to move ("lose" or "gain")

        Returns:
            str: Friendly progress message
        """
        if at_goal:
            return "🎉 Congratulations! You're at your target weight!"
        else:
            return f"💪 Keep going! You need to {direction} {difference}kg to reach your goal."

    def get_profile_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of user profile and progress.

        Returns:
            Dict[str, Any]: Dictionary containing complete profile summary
        """
        return {
            "basic_info": {
                "username": self.username,
                "name": self.name,
                "age": self.age,
                "member_since": self.created_date,
                "last_active": self.last_login
            },
            "fitness_data": {
                "current_weight": self.weight,
                "target_weight": self.target_weight,
                "weekly_goal": self.weekly_workout_goal,
                "weight_progress": self.get_weight_progress()
            },
            "activity_stats": {
                "total_workouts": len(self.workouts),
                "total_workout_time": self.get_total_workout_time(),
                "workouts_by_category": self.get_workouts_by_category(),
                "meal_plans_saved": len(self.meals)
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert User instance to dictionary for JSON serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the user
        """
        return {
            "username": self.username,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "target_weight": self.target_weight,
            "weekly_workout_goal": self.weekly_workout_goal,
            "workouts": self.workouts.copy(),
            "meals": self.meals.copy(),
            "created_date": self.created_date,
            "last_login": self.last_login
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """
        Create User instance from dictionary data (from JSON).

        Args:
            data (Dict[str, Any]): Dictionary containing user data

        Returns:
            User: New User instance
        """
        return cls(
            username=data["username"],
            name=data["name"],
            age=data["age"],
            weight=data["weight"],
            target_weight=data.get("target_weight"),
            weekly_workout_goal=data.get("weekly_workout_goal", 3),
            workouts=data.get("workouts", []),
            meals=data.get("meals", []),
            created_date=data.get("created_date"),
            last_login=data.get("last_login")
        )

    def __str__(self) -> str:
        """String representation for debugging."""
        return f"User(username='{self.username}', name='{self.name}', age={self.age})"

    def __repr__(self) -> str:
        """Developer representation for debugging."""
        return (f"User(username='{self.username}', name='{self.name}', "
                f"workouts={len(self.workouts)}, meals={len(self.meals)})")
