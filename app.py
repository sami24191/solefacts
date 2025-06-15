import streamlit as st
import json
from utils.search_post import search_posts  # make sure function name matches

# Load Reddit data
with open("data/solefacts_tagged_data.json", "r") as f:
    reddit_posts = json.load(f)

st.title("SoleFacts: Search Running Shoe Feedback")

query = st.text_input("What do you want to know?")

if query:
    # Pass user query as a fallback filter for model
    results = search_posts(
        posts=reddit_posts,
        model=query,
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
            st.markdown(f"- **{title}** [🔗 link]({url})")
            st.markdown(f"  _Tags:_ `{tags}`\n")
    else:
        st.info("No results found for that query.")
