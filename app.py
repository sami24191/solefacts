import streamlit as st
import json
from utils.search_post import search_post

# Load Reddit data
with open("data/solefacts_tagged_data.json", "r") as f:
    reddit_posts = json.load(f)

st.title("SoleFacts: Search Running Shoe Feedback")

query = st.text_input("What do you want to know?")

if query:
    # Pass the query string as the model filter
    results = search_post(
        posts=reddit_posts,
        model=query,           # 👈 using user input as the model keyword
        feature=None,
        user_type=None,
        sentiment=None
    )

    if results:
        st.markdown("### Results")
        for r in results:
            title = r.get("title", "[No title]")
            url = r.get("url", "#")
            tags = r.get("tags", {})
            st.markdown(f"**{title}** [🔗 link]({url})")
            st.markdown(f"_Tags:_ `{tags}`")
            st.markdown("---")
    else:
        st.info("No results found for that query.")
