# file get_ingredients.py

import os
import re

# Define current working directory to build filepath to read recipe files
def full_path(file_name: str) -> str:
    cwd = os.getcwd()
    dir_name = 'recipes_and_standards'
    return os.path.join(cwd, dir_name, file_name)

# Open the file to read
# with open(full_path, 'r') as file:
    # lines = file.readlines()

# list of recipe measurement units
UNITS_OF_MEASURE = ['g', 'gram', 'oz', 'ounce', 'lb', 'pound', 'ea', 'each', 'sm', 'small', 'med', 'medium', 'lg', 'large', 't', 'tsp', 'teaspoon', 'tbsp', 'tablespoon', 'c', 'cup', 'ml', 'l', 'qt', 'quart', 'liter', 'gal', 'gallon']


# ingredients_start = lines.index('**INGREDIENTS**  \n')
# ingredients_end = lines.index('  \n', ingredients_start)

ingredients_list = []

def search_for_recipe_files(directory: str) -> list:
    """
    Use the given string as a directory to get every file that has the word 'recipe' and ends with '.md'
    """
    recipe_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.md') and 'recipe' in filename:
            recipe_files.append(filename)
    return recipe_files

def recipe_ingredients_section(file_path: str) -> list:
    """
    Use the given string as a filepath to open a file and return its contents.

    Args: 
        file_path (str): The full filepath of the file

    Returns:
        list: A list of the lines containing the recipe ingredients.
    """
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if '**INGREDIENTS**  \n' in lines:
        ingredients_start = lines.index('**INGREDIENTS**  \n')
        if '  \n' in lines:
            ingredients_end = lines.index('  \n', ingredients_start)
            return lines[ingredients_start + 1 : ingredients_end]

def is_unit_of_measure(word: str) -> bool:
    """
    Check if the given word is in the list of UNITS_OF_MEASURE.

    Args:
        word (str): The word to search for in the list. Want to know if the word is a unit of measure.

    Returns:
        bool: True if the word is in the list, False otherwise.
    """

    # Check if the input parameter is of the correct type
    if not isinstance(word, str):
        raise TypeError("The word parameter must be a string.")

    # Check if the word is in the list and return the result
    # Iterate through the list of units of measure and check also for the plural version
    for unit in UNITS_OF_MEASURE:
        if word.lower() == unit:
            return True
        elif word.lower() == unit + 's':
            return True

    # If the above has not returned True, need to return False
    return False

def is_ingredient_in_list(ingredient: str, ingredients_list: list) -> bool:
    """
    Check if the given ingredient is in the list of ingredients.

    Args:
        ingredient (str): The ingredient to search for in the list.
        ingredients_list (list): The list of ingredients to search in.

    Returns:
        bool: True if the ingredient is in the list, False otherwise.
    """

    # Check if the input parameters are of the correct type
    if not isinstance(ingredient, str):
        raise TypeError("The ingredient parameter must be a string.")
    if not isinstance(ingredients_list, list):
        raise TypeError("The ingredients_list parameter must be a list.")

    # Check if the ingredient is in the list and return the result
    return ingredient in ingredients_list

def add_ingredient(ingredient: str, ingredients_list: list):
    """
    Add a given ingredient to the given list of ingredients.

    Args: 
        ingredient (str): The ingredient to add to the list.
        ingredients_list (list): The list of ingredients to add to.

    Returns:
        
    """

    # Check i fthe input parameters are of the correct type
    if not isinstance(ingredient, str):
        raise TypeError("The ingredient parameter must be a string.")
    if not isinstance(ingredients_list, list):
        raise TypeError("The ingredients_list parameter must be a list.")

    # First, call .title() method to capitalize each word before adding to the list
    ingredient = ingredient.lower()

    # Check to see if ingredient is not in the list
    if not is_ingredient_in_list(ingredient, ingredients_list):
    
        # Add the ingredient to the list
        ingredients_list.append(ingredient)

def join_words(word: str, words: list) -> str:
    """
    Get the index of the word in a list, and return a string of all words remaining after the index of the given word.

    Args: 
        word (str): The word to get the index of.
        words (list): The list of words to join.

    Returns:
        str: a string of the joined words
    """

    # Check if the input parameters are of the correct type
    if not isinstance(word, str):
        raise TypeError("The word parameter must be a string.")
    if not isinstance(words, list):
        raise TypeError("The words parameter must be a list.")

    # Check if the word is in the list
    if word in words:
        i = words.index(word) + 1
        return ' '.join(words[i:])


for recipe_file in search_for_recipe_files('recipes_and_standards'):
    
    if recipe_ingredients_section(full_path(recipe_file)) != None:
        for line in recipe_ingredients_section(full_path(recipe_file)):

            words = line.split()
            for word in words:

                if is_unit_of_measure(word):

                    ing = join_words(word, words)
                    
                    # remove unit conversions listed in parentheses i.e. 227 g (1 cup)
                    pattern = '[(]*[)]'
                    if re.search(pattern, ing):
                        ing = re.split(pattern, ing)[1].lstrip()

                    # remove commas i.e. red bell peppers, diced
                    pattern = ','
                    if pattern in ing:
                        ing = ing.split(pattern)[0]

                    # [] TODO: remove trailing ~ characters
                    # [] TODO: account for ingredients with an alternative ingredient listed after 'or'

                    add_ingredient(ing, ingredients_list)
            
print(ingredients_list)

