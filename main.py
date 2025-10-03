import json
import streamlit as st

# load dataset 
with open('recipes.json', 'r') as file: recipes = json.load(file) 

st.title('Food IDEA') # title text

# filter style for multiselect
AllStyle=sorted(list({item['style'] for item in recipes if item.get('style')}))

# user input
styles_input = st.multiselect('อาหารของประเทศ / ไม่เลือกระบบจะดึงมาจากทุกอัน', AllStyle)
ingrediants_input = st.text_input('วัตถุดิบที่มี เช่น แป้งสาลี, ไข่, นม, น้ำตาล, เนย')

# filter style for user selected style
def _filter_menu_style(styles_input):
    if styles_input: return [style for style in recipes if style['style'] in styles_input]
    else: return recipes

# convert ingrediants input for easy use
def _filter_user_ingrediants(ingrediants_input):
    if ingrediants_input:
        return [str(ing).lower() for ing in ingrediants_input.split(',')]
    else:
        return []

# filter menu for recommend result
def _menu_filter_for_rdm(menu, userinput):
    match_ing_list = [ing for ing in menu['ingredients'] if ing in userinput]
    if match_ing_list:return menu
    else: return None

# button for Start filter
if st.button('Enter'):
    for menu in _filter_menu_style(styles_input):
        recommend_menu = _menu_filter_for_rdm(menu, _filter_user_ingrediants(ingrediants_input))
        if recommend_menu:
            missing_ing = [ing for ing in recommend_menu["ingredients"] if ing not in _filter_user_ingrediants(ingrediants_input)]
            # output
            with st.container(border=True):
                st.write(f'{recommend_menu["style"]} : {recommend_menu["name"]}')
                st.text(f'ประเภท : {recommend_menu['category']}')
                st.text(f'มังสวิรัติ : {recommend_menu["vegetarian"]}')
                st.caption(f'วัตถุดิบ : {", ".join(recommend_menu["ingredients"])}')
                st.caption(f'วัตถุดิบที่ขาด : {", ".join(missing_ing)}' if missing_ing else 'วัตถุดิบที่ขาด : None')
