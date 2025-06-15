# utils/search_post.py

def search_posts(posts, model=None, feature=None, user_type=None, sentiment=None, limit=5):
    """
    Filter Reddit posts based on model name, feature, user type, and sentiment.

    Args:
        posts (list): List of post dictionaries.
        model (str): Optional shoe model filter.
        feature (str): Optional feature filter (e.g., "heel support").
        user_type (str): Optional user persona filter (e.g., "overpronator").
        sentiment (str): "positive" or "negative" — uses basic thresholds.
        limit (int): Maximum number of results to return.

    Returns:
        list: Filtered and formatted post results.
    """
    results = []

    for post in posts:
        tags = post.get("tags", {})
        match = True

        if model and model.lower() not in [m.lower() for m in tags.get("model_mentions", [])]:
            match = False
        if feature and feature.lower() not in [f.lower() for f in tags.get("feature_mentions", [])]:
            match = False
        if user_type and user_type.lower() not in [u.lower() for u in tags.get("user_type", [])]:
            match = False
        if sentiment == "positive" and tags.get("sentiment", 0) < 0.5:
            match = False
        if sentiment == "negative" and tags.get("sentiment", 0) > -0.5:
            match = False

        if match:
            results.append({
                "title": post.get("title", ""),
                "url": post.get("url", ""),
                "tags": tags,
                "score": tags.get("sentiment")
            })

    # Debug output for console/logs
    print(f"🔍 Found {len(results)} matching posts\n")
    for i, r in enumerate(results[:limit]):
        print(f"{i+1}. {r['title']}")
        print(f"   Tags: {r['tags']}")
        print(f"   URL: {r['url']}")
        print("-" * 80)

    return results
