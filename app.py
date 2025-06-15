import streamlit as st
import json
from utils.search_post import search_posts  # Make sure the function is named search_posts

# Load Reddit data
with open("data/solefacts_tagged_data.json", "r") as f:
    reddit_posts = json.load(f)

st.title("SoleFacts: Search Running Shoe Feedback")

query = st.text_input("What do you want to know?")

if query:
    # Use query as model keyword for now
    results = search_posts(
        posts=reddit_posts,
        model=query,         # User input drives the model filter
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
