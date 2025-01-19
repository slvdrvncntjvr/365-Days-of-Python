import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients"

def suggest_recipes(ingredients):
    """
    Fetch recipes from the Spoonacular API based on ingredients.
    """
    if not API_KEY:
        raise ValueError("API key is missing! Ensure it's set in the .env file.")

    try:
        # Convert the list of ingredients into a comma-separated string
        ingredients_str = ",".join(ingredients)
        
        # Make API request
        response = requests.get(
            BASE_URL,
            params={
                "ingredients": ingredients_str,
                "number": 5,  # Number of recipes to return
                "apiKey": API_KEY,
            },
        )
        
        # Handle response
        if response.status_code == 200:
            recipes = response.json()
            return [{"title": recipe["title"], "image": recipe["image"]} for recipe in recipes]
        else:
            print(f"Error: Unable to fetch recipes (Status Code: {response.status_code})")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
