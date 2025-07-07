"""
Workout model for Fitness App v2.0

This module contains the Workout class that represents individual workouts
and workout management functionality.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class WorkoutCategory(Enum):
    """Enumeration of available workout categories."""
    CARDIO = "cardio"
    STRENGTH = "strength"
    FLEXIBILITY = "flexibility"


class WorkoutIntensity(Enum):
    """Enumeration of workout intensity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Workout:
    """
    Represents a single workout session.

    This class manages individual workout data including type, duration,
    intensity, and performance metrics.

    Attributes:
        workout_type (str): Type of workout (e.g., "running", "push_ups")
        category (WorkoutCategory): Category enum (cardio, strength, flexibility)
        duration (int): Duration in minutes
        intensity (WorkoutIntensity): Intensity level enum
        date (str): Date when workout was performed
        calories_burned (Optional[int]): Estimated calories burned
        notes (Optional[str]): Additional workout notes
    """

    def __init__(
        self,
        workout_type: str,
        category: WorkoutCategory,
        duration: int,
        intensity: WorkoutIntensity,
        date: Optional[str] = None,
        calories_burned: Optional[int] = None,
        notes: Optional[str] = None
    ) -> None:
        """
        Initialize a new Workout instance.

        Args:
            workout_type (str): Type of workout
            category (WorkoutCategory): Workout category
            duration (int): Duration in minutes
            intensity (WorkoutIntensity): Intensity level
            date (Optional[str]): Workout date. Defaults to current date
            calories_burned (Optional[int]): Calories burned estimate
            notes (Optional[str]): Additional notes
        """
        self.workout_type = workout_type.lower().replace(" ", "_")
        self.category = category
        self.duration = duration
        self.intensity = intensity
        self.date = date or datetime.now().strftime("%B %d, %Y")
        self.calories_burned = calories_burned or self._estimate_calories()
        self.notes = notes or ""

    def _estimate_calories(self) -> int:
        """
        Estimate calories burned based on workout type, duration, and intensity.

        Uses average calorie burn rates for different workout types and
        adjusts based on intensity level.

        Returns:
            int: Estimated calories burned
        """
        # Base calories per minute for different workout types
        calorie_rates = {
            # Cardio workouts
            "running": 12,
            "cycling": 10,
            "swimming": 11,
            "walking": 5,
            "dancing": 7,
            "jumping_jacks": 8,

            # Strength workouts
            "push_ups": 6,
            "squats": 7,
            "deadlifts": 8,
            "bench_press": 6,
            "pull_ups": 8,
            "weight_lifting": 7,

            # Flexibility workouts
            "yoga": 3,
            "stretching": 2,
            "pilates": 4,
            "tai_chi": 3
        }

        # Get base rate or default
        base_rate = calorie_rates.get(self.workout_type, 5)

        # Intensity multipliers
        intensity_multipliers = {
            WorkoutIntensity.LOW: 0.8,
            WorkoutIntensity.MEDIUM: 1.0,
            WorkoutIntensity.HIGH: 1.3
        }

        # Calculate total calories
        multiplier = intensity_multipliers[self.intensity]
        total_calories = int(base_rate * self.duration * multiplier)

        return max(total_calories, 1)  # Minimum 1 calorie

    def update_duration(self, new_duration: int) -> None:
        """
        Update workout duration and recalculate calories.

        Args:
            new_duration (int): New duration in minutes
        """
        self.duration = new_duration
        self.calories_burned = self._estimate_calories()

    def update_intensity(self, new_intensity: WorkoutIntensity) -> None:
        """
        Update workout intensity and recalculate calories.

        Args:
            new_intensity (WorkoutIntensity): New intensity level
        """
        self.intensity = new_intensity
        self.calories_burned = self._estimate_calories()

    def add_notes(self, notes: str) -> None:
        """
        Add or update workout notes.

        Args:
            notes (str): Notes to add
        """
        self.notes = notes.strip()

    def get_workout_summary(self) -> Dict[str, Any]:
        """
        Get a comprehensive summary of the workout.

        Returns:
            Dict[str, Any]: Dictionary containing workout summary
        """
        return {
            "type": self.workout_type.replace("_", " ").title(),
            "category": self.category.value,
            "duration": f"{self.duration} minutes",
            "intensity": self.intensity.value.title(),
            "calories_burned": self.calories_burned,
            "date": self.date,
            "notes": self.notes if self.notes else "No notes added"
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Workout instance to dictionary for JSON serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of the workout
        """
        return {
            "type": self.workout_type,
            "category": self.category.value,
            "duration": self.duration,
            "intensity": self.intensity.value,
            "date": self.date,
            "calories_burned": self.calories_burned,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workout':
        """
        Create Workout instance from dictionary data (from JSON or API).

        Args:
            data (Dict[str, Any]): Dictionary containing workout data

        Returns:
            Workout: New Workout instance
        """
        return cls(
            workout_type=data["type"],
            category=WorkoutCategory(data["category"]),
            duration=data["duration"],
            intensity=WorkoutIntensity(data["intensity"]),
            date=data.get("date"),
            calories_burned=data.get("calories_burned"),
            notes=data.get("notes", "")
        )

    @classmethod
    def create_quick_workout(cls, workout_type: str, duration: int) -> 'Workout':
        """
        Create a quick workout with default settings.

        Args:
            workout_type (str): Type of workout
            duration (int): Duration in minutes

        Returns:
            Workout: New workout with medium intensity and auto-category
        """
        # Auto-detect category based on workout type
        cardio_types = ["running", "cycling", "swimming", "walking", "dancing"]
        strength_types = ["push_ups", "squats",
                          "deadlifts", "bench_press", "pull_ups"]

        if any(cardio in workout_type.lower() for cardio in cardio_types):
            category = WorkoutCategory.CARDIO
        elif any(strength in workout_type.lower() for strength in strength_types):
            category = WorkoutCategory.STRENGTH
        else:
            category = WorkoutCategory.FLEXIBILITY

        return cls(
            workout_type=workout_type,
            category=category,
            duration=duration,
            intensity=WorkoutIntensity.MEDIUM
        )

    def __str__(self) -> str:
        """String representation for display."""
        return f"{self.workout_type.replace('_', ' ').title()} - {self.duration}min ({self.intensity.value})"

    def __repr__(self) -> str:
        """Developer representation for debugging."""
        return (f"Workout(type='{self.workout_type}', category={self.category.value}, "
                f"duration={self.duration}, intensity={self.intensity.value})")
