import json
import streamlit as st

with open('recipes.json', 'r') as file: recipes = json.load(file)

st.title('Food IDEA')

AllStyle=sorted(list({item['style'] for item in recipes if item.get('style')}))
    
styles_input = st.multiselect('Food Style', AllStyle)
ingrediants_input = st.text_input('ingrediants')
# styles_input = input("Style: ")
# ingrediants_input = input("Ingrediants: ")

def load_menu_f_style(styles_input):
    return [style for style in recipes if style['style'] in styles_input]

def load_ingrediant_f_filter(ingrediants_input):
    if ingrediants_input:
        return [str(ing).lower() for ing in ingrediants_input.split(',')]
    else:
        return []

def menu_filter_for_rdm(menu, userinput):
    # print(menu)
    local_ingrediants = menu['ingredients']
    input_ing = userinput

    missing_ing = []
    match_ing = []

    for ing in local_ingrediants:
        if ing in input_ing:
            match_ing.append(ing)
        else:
            missing_ing.append(ing)
    if match_ing:return [menu, missing_ing, len(match_ing)]

    
if st.button('Get Menu'):
    menu_list = list()
    for menu in load_menu_f_style(styles_input):
        # print(menu_filter_for_rdm(menu, load_ingrediant_f_filter(ingrediants_input)))
        menu_list.append(menu_filter_for_rdm(menu, load_ingrediant_f_filter(ingrediants_input)))

    reccommend_list = sorted(menu_list, key=lambda x: x[-1] if x else 0, reverse=True)
    for item in reccommend_list:
        if item:
            dish=item[0]
            missing_ing=item[1]
            with st.container(border=True):
                st.write(dish['style'])
                st.write(dish['name'])
                st.caption(f'Match Score : {item[2]}')
                st.caption(f'Missing Ingrediants : {missing_ing}')

