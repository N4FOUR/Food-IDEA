import json
import streamlit as st

# load menu data
with open("recipes.json", "r") as file: recipes = json.load(file)
st.title("Find My Food")

# input
# input_style = input('Style :')
# input_ingrediants = [ingrediant for ingrediant in input('Ingrediants :').split()]
all_style = ['Thai', 'Japan', 'USA']
with st.container(border=True):
    food_style = st.multiselect("Users", all_style, default=all_style)
input_ingrediants = st.chat_input("Ingrediants")
# filter menu
# food_style = list(filter(lambda recipe: recipe["style"] == input_style.capitalize(), recipes))

# match recipe
# def match_recipe(recipe, ingrediants):
#     recipe_ingrediants = recipe["ingredients"]
#     score = 0
#     for ingrediant in ingrediants:
#         if ingrediant in recipe_ingrediants:
#             score += 1
#     return score, recipe['name'], [ingrediant for ingrediant in recipe_ingrediants if ingrediant not in ingrediants]

# result = sorted(list(map(lambda recipe: match_recipe(recipe, input_ingrediants), food_style)), reverse=True)

# # output
# def convert_result(result):
#     result_list = list()
#     for menu in result:
#         score, name, missing = menu
#         result_list.append({'name': name, 'score': score, 'missing': missing})
#     return result_list

# reccommended_menu = convert_result(result)
