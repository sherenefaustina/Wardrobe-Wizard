import random

OUTFITS = {

"college":{

"happy":[

{
"top":"Yellow Hoodie",
"bottom":"Blue Jeans",
"shoes":"White Sneakers",
"accessory":"Smart Watch"
},

{
"top":"Graphic Tee",
"bottom":"Cargo Pants",
"shoes":"Nike Sneakers",
"accessory":"Backpack"
}

],

"sad":[

{
"top":"Oversized Sweatshirt",
"bottom":"Joggers",
"shoes":"Running Shoes",
"accessory":"Cap"
}

],

"neutral":[

{
"top":"Polo Shirt",
"bottom":"Chinos",
"shoes":"Casual Sneakers",
"accessory":"Watch"
}

]

},

"party":{

"happy":[

{
"top":"Sequined Top",
"bottom":"Leather Pants",
"shoes":"Heels",
"accessory":"Handbag"
}

],

"neutral":[

{
"top":"Blazer",
"bottom":"Slim Fit Pants",
"shoes":"Loafers",
"accessory":"Luxury Watch"
}

]

},

"gym":{

"happy":[

{
"top":"Dry Fit Tee",
"bottom":"Track Pants",
"shoes":"Sports Shoes",
"accessory":"Fitness Band"
}

]

}

}


def generate_outfit(
occasion,
mood,
weather
):

    try:

        outfit = random.choice(
            OUTFITS[occasion][mood]
        )

    except:

        outfit = {
            "top":"Basic T-Shirt",
            "bottom":"Jeans",
            "shoes":"Sneakers",
            "accessory":"Watch"
        }

    outfit["weather"] = weather

    outfit["score"] = random.randint(
        85,
        98
    )

    return outfit