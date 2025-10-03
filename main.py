import json
import streamlit as st

with open('recipes.json', 'r') as file: recipes = json.load(file)

st.title('Food IDEA')

AllStyle=sorted(list({item['style'] for item in recipes if item.get('style')}))
    
styles_input = st.multiselect('Food Style', AllStyle)
ingrediants_input = st.text_input('ingrediants')

def load_menu_f_style(styles_input):
    return [style for style in recipes if style['style'] in styles_input]

def load_ingrediant_f_filter(ingrediants_input):
    if ingrediants_input:
        return ingrediants_input.split(',')
    else:
        return []

def macth_ingrediant_f_result(menu):
    ingrediants=load_ingrediant_f_filter(ingrediants_input)
    item_for_return = list()
    missing_ingrediants = list()
    for item in menu:
        score=0
        if ingrediants in item['ingrediants']:
            item_for_return.append(item)
            for ing in ingrediants:
                if ing in item['ingrediants']:score+=1
        else:missing_ingrediants.append(item)
    return item_for_return, missing_ingrediants, score

if st.button('Get Menu'):
    if styles_input:menu=load_menu_f_style(styles_input)
    else:menu=AllStyle

    recommends, missing_ingrediants, score = macth_ingrediant_f_result(menu)

    for menu_list in recommends:
        with st.container(border=True):
            st.write(menu_list['name'])
            st.write(f'Style: {menu_list["style"]}')
            st.write(menu_list['Category'])
            st.write(f'Vegetarian: {menu_list["vegetarian"]}')
            st.caption(f'Match Score :{score}')
            misstext=''
            for ing in missing_ingrediants:misstext+=f'{ing}, '
            st.caption(f'You missing : {misstext}')
