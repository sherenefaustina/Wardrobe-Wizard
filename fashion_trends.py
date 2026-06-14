import random

TRENDING_COLORS = [
    {
        "name":"Mocha Mousse",
        "hex":"#A47864"
    },
    {
        "name":"Lavender",
        "hex":"#C8A2C8"
    },
    {
        "name":"Emerald Green",
        "hex":"#50C878"
    },
    {
        "name":"Cherry Red",
        "hex":"#DE3163"
    },
    {
        "name":"Powder Blue",
        "hex":"#B0E0E6"
    }
]

TRENDING_STYLES = [
    "Quiet Luxury",
    "Streetwear",
    "Coquette",
    "Old Money",
    "Oversized Fashion",
    "Minimalist Chic",
    "Y2K Revival",
    "Athleisure"
]

SEASONAL = {
    "Summer":
    "Breathable cotton outfits, pastel shades, linen shirts and airy dresses.",

    "Winter":
    "Layered jackets, sweaters, trench coats and boots.",

    "Spring":
    "Floral patterns, light fabrics and bright cheerful colors.",

    "Autumn":
    "Earth-tone outfits, cardigans and textured knitwear."
}


def get_fashion_trends():

    return {
        "colors": TRENDING_COLORS,
        "styles": TRENDING_STYLES,
        "seasonal": SEASONAL
    }


def calculate_trend_score(category):

    base_scores = {
        "tops": 88,
        "bottoms": 82,
        "dresses": 95,
        "shoes": 79,
        "accessories": 85
    }

    return base_scores.get(category,80)