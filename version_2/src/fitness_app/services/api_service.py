"""
API service for Fitness App v2.0

This module handles external API integrations for workout and nutrition data.
"""

import requests
import json
from typing import Dict, List, Optional, Any, Union
from time import sleep


class APIError(Exception):
    """Custom exception for API-related errors."""
    pass


class WorkoutAPIService:
    """
    Handles integration with external workout and exercise APIs.

    This service fetches exercise data, workout suggestions, and fitness
    information from the Wger Workout Manager API.
    """

    def __init__(self) -> None:
        """Initialize the workout API service."""
        self.base_url = "https://wger.de/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'FitnessApp/2.0 (Educational Project)',
            'Accept': 'application/json'
        })
        self.request_delay = 1  # this is to be respectful to the API

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """
        Make a request to the API with error handling and rate limiting.

        Args:
            endpoint (str): API endpoint to call
            params (Optional[Dict]): Query parameters

        Returns:
            Optional[Dict]: Response data or None if failed

        Raises:
            APIError: If request fails after retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        try:
            print(f"🔄 Making API request to: {endpoint}")
            sleep(self.request_delay)  # Rate limiting

            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                print(f"✅ API request successful!")
                return data
            elif response.status_code == 429:
                print("⚠️ Rate limited, waiting longer...")
                sleep(5)
                return self._make_request(endpoint, params)  # Retry once
            else:
                print(f"❌ API Error: {response.status_code} - {response.text}")
                raise APIError(f"API request failed: {response.status_code}")

        except requests.Timeout:
            print("❌ Request timed out")
            raise APIError("Request timed out")
        except requests.RequestException as e:
            print(f"❌ Network error: {e}")
            raise APIError(f"Network error: {e}")

    def get_exercise_categories(self) -> List[Dict[str, Any]]:
        """
        Fetch available exercise categories from the API.

        Returns:
            List[Dict]: List of exercise categories with id and name
        """
        try:
            data = self._make_request("exercisecategory/")
            if data and 'results' in data:
                categories = data['results']
                print(f"📋 Found {len(categories)} exercise categories")
                return categories
            return []

        except APIError as e:
            print(f"Failed to fetch categories: {e}")
            return self._get_fallback_categories()

    def _get_fallback_categories(self) -> List[Dict[str, Any]]:
        """
        Provide fallback categories if API is unavailable.

        Returns:
            List[Dict]: Default exercise categories
        """
        print("🔧 Using fallback exercise categories")
        return [
            {"id": 1, "name": "Abs"},
            {"id": 2, "name": "Arms"},
            {"id": 3, "name": "Back"},
            {"id": 4, "name": "Calves"},
            {"id": 5, "name": "Chest"},
            {"id": 6, "name": "Legs"},
            {"id": 7, "name": "Shoulders"},
            {"id": 8, "name": "Cardio"}
        ]

    def get_exercises_by_category(self, category_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch exercises for a specific category.

        Args:
            category_id (int): Category ID to fetch exercises for
            limit (int): Maximum number of exercises to return

        Returns:
            List[Dict]: List of exercise data or empty list if failed
        """
        try:
            params = {
                'category': category_id,
                'limit': limit,
                'language': 2  # English
            }

            data = self._make_request("exercise/", params)
            if data and 'results' in data:
                exercises = []

                # Process each exercise
                for exercise in data['results']:
                    # Get detailed info for each exercise
                    exercise_detail = self._make_request(
                        f"exerciseinfo/{exercise['id']}/")
                    if exercise_detail:
                        clean_exercise = self._clean_exercise_data(
                            exercise_detail)
                        exercises.append(clean_exercise)

                print(
                    f"✅ Retrieved {len(exercises)} exercises for category {category_id}")
                return exercises

            return []

        except APIError as e:
            print(f"Failed to fetch exercises: {e}")
            return self._get_fallback_exercises(category_id)

    def _clean_exercise_data(self, raw_data: Dict) -> Dict[str, Any]:
        """
        Extract and clean exercise data from API response.

        Args:
            raw_data (Dict): Raw API response

        Returns:
            Dict: Clean exercise data
        """
        # Extract name from translations (like we learned!)
        name = "Unknown Exercise"
        description = "No description available"

        if raw_data.get('translations'):
            first_translation = raw_data['translations'][0]
            name = first_translation.get('name', name)
            description = first_translation.get('description', description)
            # Clean HTML tags
            description = description.replace('<p>', '').replace(
                '</p>', '').replace('<br>', ' ')

        # Extract category name
        category = "Unknown"
        if raw_data.get('category'):
            category = raw_data['category'].get('name', category)

        # Extract equipment list
        equipment = []
        if raw_data.get('equipment'):
            equipment = [item['name'] for item in raw_data['equipment']]

        return {
            'id': raw_data.get('id'),
            'name': name,
            'description': description[:200] + "..." if len(description) > 200 else description,
            'category': category,
            'equipment': equipment,
            'difficulty': 'Medium'  # Default since API doesn't provide this
        }

    def get_food_data(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for food/nutrition data."""
        try:
            print(f"🍎 Searching for food: '{query}'...")
            sleep(self.request_delay)

            # For now, use fallback data since Edamam API needs real keys
            return self._get_fallback_foods(query)

        except Exception as e:
            print(f"❌ Food API Error: {e}")
            return self._get_fallback_foods(query)

    def _get_fallback_foods(self, query: str) -> List[Dict[str, Any]]:
        """Provide fallback food data when API is unavailable."""
        print("🔧 Using fallback food database")

        fallback_foods = {
            'apple': {'name': 'Apple', 'calories_per_100g': 52, 'protein': 0.3, 'carbs': 14, 'fat': 0.2},
            'chicken': {'name': 'Chicken Breast', 'calories_per_100g': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6},
            'rice': {'name': 'White Rice', 'calories_per_100g': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3},
            'banana': {'name': 'Banana', 'calories_per_100g': 89, 'protein': 1.1, 'carbs': 23, 'fat': 0.3},
            'potatoes': {'name': 'Potatoes', 'calories_per_100g': 77, 'protein': 2, 'carbs': 17, 'fat': 0.1},
            'salmon': {'name': 'Salmon', 'calories_per_100g': 208, 'protein': 22, 'carbs': 0, 'fat': 12}
        }

        # Try to match the query
        for key, food_data in fallback_foods.items():
            if key in query.lower():
                return [food_data]

        # Generic fallback for unknown foods
        return [{'name': f'{query.title()}', 'calories_per_100g': 100, 'protein': 5, 'carbs': 15, 'fat': 2, 'category': 'Generic food'}]
