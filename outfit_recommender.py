def recommend_outfit(weather, event):
    if weather == "hot" and event == "party":
        return "Sleeveless dress or crop top with shorts"
    elif weather == "cold" and event == "formal":
        return "Blazer with trousers or warm formal suit"
    elif weather == "rainy" and event == "gym":
        return "Quick-dry tracksuit with waterproof sneakers"
    # and so on...
