import json
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Food IDEA", layout="wide")
st.title("🍽️ Food IDEA — Food Recommendation")

# load data
DATA_PATH = Path("recipes.json")
if not DATA_PATH.exists():
    st.error("recipes.json not found. Put recipes.json in the same folder as this app.")
    st.stop()

with open(DATA_PATH, "r", encoding="utf-8") as f:
    recipes = json.load(f)

# normalize recipe internal: flatten ingredients to lowercase stripped
for r in recipes:
    r["ingredients"] = [ing.strip().lower() for ing in r.get("ingredients", [])]
    r["style"] = r.get("style", "").strip()

# UI controls
all_styles = sorted(list({r["style"] for r in recipes if r.get("style")}))
selected_styles = st.multiselect("Choose style(s) (leave empty for all)", all_styles, default=all_styles)

ing_input = st.text_input("Enter your ingredients (comma separated). Example: pork, carrot, egg")
min_match = st.slider(
    "Minimum matched ingredients",
    min_value=1,
    max_value=5,   # กำหนดช่วงที่เลือกได้
    value=1,       # ค่าเริ่มต้น
    help="Only show recipes with at least this many matching ingredients"
)
show_missing = st.checkbox("Show missing ingredients", value=True)
max_results = st.number_input("Max results to show", min_value=1, max_value=50, value=10)

def parse_ingredients(text):
    if not text:
        return []
    parts = [p.strip().lower() for p in text.replace("/", " ").replace("(", " ").replace(")", " ").split(",")]
    parts = [p for p in parts if p]
    # also split by spaces if user didn't separate by comma
    final = []
    for p in parts:
        if " " in p and "," not in p:
            # keep whole token, because some ingredients are multiword ("coconut milk")
            final.append(p)
        else:
            final.append(p)
    # unique
    return sorted(list(dict.fromkeys(final)))

def score_recipe(recipe, user_ings):
    recipe_ings = recipe.get("ingredients", [])
    if not recipe_ings:
        return {"score":0, "ratio":0.0, "missing":recipe_ings}
    match_set = set(user_ings) & set(recipe_ings)
    score = len(match_set)
    ratio = score / len(recipe_ings)
    missing = [ing for ing in recipe_ings if ing not in user_ings]
    return {"score":score, "ratio":ratio, "missing":missing, "matches":sorted(list(match_set))}

# trigger search
if st.button("Recommend"):

    user_ings = parse_ingredients(ing_input)
    if not user_ings:
        st.warning("Please enter at least one ingredient.")
    else:
        # filter by style
        filtered = recipes
        if selected_styles:
            filtered = [r for r in recipes if r["style"] in selected_styles]

        results = []
        for r in filtered:
            sc = score_recipe(r, user_ings)
            if sc["score"] >= min_match:
                results.append({"recipe": r, "score": sc["score"], "ratio": sc["ratio"], "missing": sc["missing"], "matches": sc["matches"]})

        # sort results: primary by score desc, secondary by ratio desc, tertiary by recipe name
        results.sort(key=lambda x: (x["score"], x["ratio"], x["recipe"]["name"]), reverse=True)

        if not results:
            st.info("No matching recipes found. Try removing style filters or adding more ingredients.")
        else:
            st.success(f"Found {len(results)} matching recipes — showing top {min(len(results), max_results)}")
            show_count = min(len(results), max_results)
            for i in range(show_count):
                r = results[i]
                rec = r["recipe"]
                # card layout
                cols = st.columns([3,1])
                with cols[0]:
                    st.markdown(f"### {i+1}. {rec['name']}  ")
                    st.write(f"**Style:** {rec.get('style','-')}  •  **Category:** {rec.get('category','-')}  •  **Vegetarian:** {rec.get('vegetarian', False)}")
                    st.write(f"**Match score:** {r['score']}  •  **Match ratio:** {r['ratio']:.2f}")
                    if r["matches"]:
                        st.write(f"**Matched ingredients:** {', '.join(r['matches'])}")
                    if show_missing and r["missing"]:
                        st.caption(f"Missing ingredients: {', '.join(r['missing'])}")
                    # optional small recipe snippet
                with cols[1]:
                    st.write(" ")
                    st.write(" ")
                    st.write(" ")
                    st.metric(label="Score", value=r["score"], delta=f"{int(r['ratio']*100)}%")
                st.markdown("---")

# quick search by name
st.write("### Quick search")
q = st.text_input("Search recipe name (optional)")
if q:
    ql = q.strip().lower()
    matches = [r for r in recipes if ql in r["name"].lower()]
    if matches:
        for rec in matches:
            st.write(f"- **{rec['name']}** ({rec['style']}) — ingredients: {', '.join(rec['ingredients'])}")
    else:
        st.write("No recipe name match.")


