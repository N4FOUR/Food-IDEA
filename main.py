import json
import streamlit as st

with open('recipes.json', 'r') as file: recipes = json.load(file)

st.title('Food IDEA')

AllStyle=sorted(list({item['style'] for item in recipes if item.get('style')}))
    
styles_input = st.multiselect('Food Style', AllStyle)
ingrediants_input = st.text_input('ingrediants')

def _filter_menu_style(styles_input):
    return [style for style in recipes if style['style'] in styles_input]

def _filter_user_ingrediants(ingrediants_input):
    if ingrediants_input:
        return [str(ing).lower() for ing in ingrediants_input.split(',')]
    else:
        return []

def _menu_filter_for_rdm(menu, userinput):
    match_ing_list = [ing for ing in menu['ingredients'] if ing in userinput]
    if match_ing_list:return menu
    else: return None

if st.button('Enter'):
    for menu in _filter_menu_style(styles_input):
        recdm_food = _menu_filter_for_rdm(menu, _filter_user_ingrediants(ingrediants_input))
        if recdm_food:
            missing_ing = [ing for ing in recdm_food["ingredients"] if ing not in _filter_user_ingrediants(ingrediants_input)]
            with st.container(border=True):
                st.write(f'{recdm_food["style"]} : {recdm_food["name"]}')
                st.text(f'Category : {recdm_food['category']}')
                st.text(f'Vegetarian : {recdm_food["vegetarian"]}')
                st.caption(f'Ingrediants : {", ".join(recdm_food["ingredients"])}')
                st.caption(f'Missing Ingrediants : {", ".join(missing_ing)}' if missing_ing else 'Missing Ingrediants : None')
        else:
            st.write(f'Sorry, We dont have this ingredients in data')
