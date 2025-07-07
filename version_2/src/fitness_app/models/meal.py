"""
Meal planning model for Fitness App v2.0

This module contains classes for meal planning, nutrition tracking,
and food management functionality.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class MealType(Enum):
    """Enumeration of meal types throughout the day."""
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class NutritionGoal(Enum):
    """Enumeration of nutrition goals."""
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    MAINTENANCE = "maintenance"
    ENDURANCE = "endurance"


class MealPlan:
    """
    Represents a daily meal plan with nutritional information.

    This class manages meal planning for a specific day, including
    all meals, nutritional calculations, and dietary goals.

    Attributes:
        day_number (int): Day number in the meal plan sequence
        date (str): Date for this meal plan
        meals (Dict[MealType, str]): Dictionary mapping meal types to food items
        nutrition_goal (NutritionGoal): User's nutrition goal for this plan
        target_calories (Optional[int]): Target calories for the day
        notes (str): Additional notes about the meal plan
    """

    def __init__(
        self,
        day_number: int,
        date: Optional[str] = None,
        nutrition_goal: NutritionGoal = NutritionGoal.MAINTENANCE,
        target_calories: Optional[int] = None,
        notes: str = ""
    ) -> None:
        """
        Initialize a new MealPlan instance.

        Args:
            day_number (int): Day number in the sequence
            date (Optional[str]): Date for meal plan. Defaults to current date
            nutrition_goal (NutritionGoal): Nutrition goal. Defaults to maintenance
            target_calories (Optional[int]): Daily calorie target
            notes (str): Additional notes
        """
        self.day_number = day_number
        self.date = date or datetime.now().strftime("%B %d, %Y")
        self.meals: Dict[MealType, str] = {}
        self.nutrition_goal = nutrition_goal
        self.target_calories = target_calories or self._calculate_default_calories()
        self.notes = notes
        self.created_time = datetime.now().strftime("%I:%M %p")

    def _calculate_default_calories(self) -> int:
        """
        Calculate default daily calorie target based on nutrition goal.

        Returns:
            int: Default calorie target
        """
        base_calories = {
            NutritionGoal.WEIGHT_LOSS: 1800,
            NutritionGoal.MUSCLE_GAIN: 2500,
            NutritionGoal.MAINTENANCE: 2200,
            NutritionGoal.ENDURANCE: 2800
        }
        return base_calories[self.nutrition_goal]

    def add_meal(self, meal_type: MealType, food_item: str) -> None:
        """
        Add a food item to a specific meal type.

        Args:
            meal_type (MealType): Type of meal (breakfast, lunch, etc.)
            food_item (str): Name of the food item
        """
        self.meals[meal_type] = food_item.strip().title()

    def remove_meal(self, meal_type: MealType) -> bool:
        """
        Remove a meal from the plan.

        Args:
            meal_type (MealType): Type of meal to remove

        Returns:
            bool: True if meal was removed, False if meal didn't exist
        """
        if meal_type in self.meals:
            del self.meals[meal_type]
            return True
        return False

    def update_meal(self, meal_type: MealType, new_food_item: str) -> None:
        """
        Update an existing meal with a new food item.

        Args:
            meal_type (MealType): Type of meal to update
            new_food_item (str): New food item
        """
        self.add_meal(meal_type, new_food_item)

    def get_meal(self, meal_type: MealType) -> Optional[str]:
        """
        Get the food item for a specific meal type.

        Args:
            meal_type (MealType): Type of meal to get

        Returns:
            Optional[str]: Food item or None if not set
        """
        return self.meals.get(meal_type)

    def get_all_meals(self) -> Dict[str, str]:
        """
        Get all meals in the plan formatted for display.

        Returns:
            Dict[str, str]: Dictionary mapping meal type names to food items
        """
        return {meal_type.value.title(): food_item
                for meal_type, food_item in self.meals.items()}

    def is_complete(self) -> bool:
        """
        Check if the meal plan has all main meals (breakfast, lunch, dinner).

        Returns:
            bool: True if all main meals are planned
        """
        main_meals = {MealType.BREAKFAST, MealType.LUNCH, MealType.DINNER}
        return main_meals.issubset(set(self.meals.keys()))

    def get_meal_count(self) -> int:
        """
        Get the total number of meals planned.

        Returns:
            int: Number of meals in the plan
        """
        return len(self.meals)

    def estimate_daily_calories(self) -> int:
        """
        Estimate total daily calories based on planned meals.

        Uses average calorie values for common food items.

        Returns:
            int: Estimated total daily calories
        """
        # Basic calorie estimates for common foods (per serving)
        calorie_estimates = {
            # Breakfast items
            "oatmeal": 150, "eggs": 140, "toast": 80, "pancakes": 200,
            "cereal": 120, "yogurt": 100, "fruit": 80, "smoothie": 180,

            # Lunch items
            "salad": 200, "sandwich": 300, "soup": 150, "pasta": 350,
            "rice_bowl": 400, "wrap": 280, "pizza": 450, "burger": 500,

            # Dinner items
            "chicken": 300, "fish": 250, "beef": 400, "pork": 350,
            "vegetarian_curry": 320, "stir_fry": 280, "salmon": 300,

            # Snacks
            "apple": 80, "nuts": 180, "protein_bar": 200, "chips": 150,
            "crackers": 120, "cheese": 100, "banana": 90
        }

        total_calories = 0
        for meal_type, food_item in self.meals.items():
            # Clean food name for lookup
            clean_food = food_item.lower().replace(" ", "_")
            calories = calorie_estimates.get(
                clean_food, 250)  # Default 250 if not found
            total_calories += calories

        return total_calories

    def get_calorie_status(self) -> Dict[str, Any]:
        """
        Get calorie tracking status compared to target.

        Returns:
            Dict[str, Any]: Calorie status information
        """
        estimated_calories = self.estimate_daily_calories()
        difference = estimated_calories - self.target_calories

        if abs(difference) <= 100:
            status = "on_track"
            message = "🎯 Perfect! You're on track with your calorie goal!"
        elif difference > 100:
            status = "over_target"
            message = f"⚠️ Over target by {difference} calories. Consider lighter meals."
        else:
            status = "under_target"
            message = f"📈 Under target by {abs(difference)} calories. Add a healthy snack!"

        return {
            "estimated_calories": estimated_calories,
            "target_calories": self.target_calories,
            "difference": difference,
            "status": status,
            "message": message,
            "percentage_of_target": round((estimated_calories / self.target_calories) * 100, 1)
        }

    def get_nutrition_recommendations(self) -> List[str]:
        """
        Get personalized nutrition recommendations based on goal and current plan.

        Returns:
            List[str]: List of nutrition recommendations
        """
        recommendations = []
        calorie_status = self.get_calorie_status()
        meal_count = self.get_meal_count()

        # Goal-specific recommendations
        if self.nutrition_goal == NutritionGoal.WEIGHT_LOSS:
            recommendations.extend([
                "💡 Focus on protein-rich foods to maintain muscle",
                "🥗 Include plenty of vegetables for nutrients and fiber",
                "💧 Drink water before meals to help with satiety"
            ])
        elif self.nutrition_goal == NutritionGoal.MUSCLE_GAIN:
            recommendations.extend([
                "💪 Aim for protein with every meal",
                "🍠 Include complex carbs for energy",
                "🥜 Add healthy fats like nuts and avocado"
            ])
        elif self.nutrition_goal == NutritionGoal.ENDURANCE:
            recommendations.extend([
                "⚡ Prioritize carbohydrates for sustained energy",
                "🏃‍♀️ Consider pre and post-workout nutrition",
                "💧 Focus on hydration throughout the day"
            ])

        # Meal count recommendations
        if meal_count < 3:
            recommendations.append(
                "⏰ Consider adding more meals for consistent energy")
        elif meal_count == 3:
            recommendations.append(
                "✅ Good meal frequency! Consider adding a healthy snack")

        # Calorie-based recommendations
        if calorie_status["status"] == "under_target":
            recommendations.append(
                "🍎 Add nutrient-dense snacks to meet your calorie goal")
        elif calorie_status["status"] == "over_target":
            recommendations.append(
                "🥬 Consider substituting some items with lighter alternatives")

        return recommendations

    def get_meal_plan_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the meal plan.

        Returns:
            Dict[str, Any]: Complete meal plan summary
        """
        return {
            "plan_info": {
                "day": self.day_number,
                "date": self.date,
                "created": self.created_time,
                "nutrition_goal": self.nutrition_goal.value.replace("_", " ").title()
            },
            "meals": self.get_all_meals(),
            "nutrition": self.get_calorie_status(),
            "recommendations": self.get_nutrition_recommendations(),
            "completion": {
                "is_complete": self.is_complete(),
                "meal_count": self.get_meal_count(),
                "missing_meals": self._get_missing_main_meals()
            },
            "notes": self.notes if self.notes else "No notes added"
        }

    def _get_missing_main_meals(self) -> List[str]:
        """
        Get list of missing main meals.

        Returns:
            List[str]: List of missing meal type names
        """
        main_meals = {MealType.BREAKFAST, MealType.LUNCH, MealType.DINNER}
        planned_meals = set(self.meals.keys())
        missing = main_meals - planned_meals
        return [meal.value.title() for meal in missing]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert MealPlan instance to dictionary for JSON serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the meal plan
        """
        return {
            "day": self.day_number,
            "date": self.date,
            "meals": {meal_type.value: food_item for meal_type, food_item in self.meals.items()},
            "nutrition_goal": self.nutrition_goal.value,
            "target_calories": self.target_calories,
            "notes": self.notes,
            "created_time": self.created_time
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MealPlan':
        """
        Create MealPlan instance from dictionary data (from JSON or API).

        Args:
            data (Dict[str, Any]): Dictionary containing meal plan data

        Returns:
            MealPlan: New MealPlan instance
        """
        meal_plan = cls(
            day_number=data["day"],
            date=data.get("date"),
            nutrition_goal=NutritionGoal(
                data.get("nutrition_goal", "maintenance")),
            target_calories=data.get("target_calories"),
            notes=data.get("notes", "")
        )

        # Restore meals
        meals_data = data.get("meals", {})
        for meal_type_str, food_item in meals_data.items():
            meal_type = MealType(meal_type_str)
            meal_plan.add_meal(meal_type, food_item)

        # Restore created time
        meal_plan.created_time = data.get(
            "created_time", meal_plan.created_time)

        return meal_plan

    @classmethod
    def create_quick_plan(cls, day_number: int, goal: NutritionGoal) -> 'MealPlan':
        """
        Create a quick meal plan with default structure.

        Args:
            day_number (int): Day number for the plan
            goal (NutritionGoal): Nutrition goal

        Returns:
            MealPlan: New meal plan with basic structure
        """
        plan = cls(day_number=day_number, nutrition_goal=goal)

        # Add placeholder meals based on goal
        if goal == NutritionGoal.WEIGHT_LOSS:
            plan.add_meal(MealType.BREAKFAST, "Oatmeal with fruit")
            plan.add_meal(MealType.LUNCH, "Garden salad with protein")
            plan.add_meal(MealType.DINNER, "Grilled chicken with vegetables")
        elif goal == NutritionGoal.MUSCLE_GAIN:
            plan.add_meal(MealType.BREAKFAST, "Protein smoothie with banana")
            plan.add_meal(MealType.LUNCH, "Chicken rice bowl")
            plan.add_meal(MealType.DINNER, "Salmon with sweet potato")
            plan.add_meal(MealType.SNACK, "Greek yogurt with nuts")
        else:  # Maintenance or Endurance
            plan.add_meal(MealType.BREAKFAST, "Eggs with toast")
            plan.add_meal(MealType.LUNCH, "Sandwich with side salad")
            plan.add_meal(MealType.DINNER, "Balanced dinner plate")

        return plan

    def __str__(self) -> str:
        """String representation for display."""
        return f"Day {self.day_number} Meal Plan - {self.date} ({self.get_meal_count()} meals)"

    def __repr__(self) -> str:
        """Developer representation for debugging."""
        return (f"MealPlan(day={self.day_number}, goal={self.nutrition_goal.value}, "
                f"meals={self.get_meal_count()}, calories={self.estimate_daily_calories()})")
