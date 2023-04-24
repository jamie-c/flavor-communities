# file get_ingredients.py

import os
import markdown

cwd = os.getcwd()
file_name = 'cheesy_queso.md'
dir_name = 'recipes_and_standards'
full_path = os.path.join(cwd, dir_name, file_name)

UNITS_OF_MEASURE = ['g', 'gram', 'grams', 'oz', 'ounce', 'ounces', 'lb', 'pound', 'pounds', 'ea', 'each', 'sm', 'small', 'med', 'medium', 'lg', 'large', 't', 'tsp', 'teaspoon', 'tbsp', 'tablespoon', 'c', 'cup', 'cups', 'ml', 'l', 'qt', 'quart', 'quarts', 'liter', 'liters', 'gal', 'gallon', 'gallons']

with open(full_path, 'r') as file:
    lines = file.readlines()

ingredients_start = lines.index('**INGREDIENTS**  \n')
ingredients_end = lines.index('  \n', ingredients_start)

ingredients_list = []
for line in lines[ingredients_start+1:ingredients_end]:
    ingredients_list.append(line.strip())

print(ingredients_list)
