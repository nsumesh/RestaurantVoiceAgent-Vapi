HOURS = {
    "Monday":    {"open": "12:00 PM", "close": "10:30 PM"},
    "Tuesday":   {"open": "12:00 PM", "close": "10:30 PM"},
    "Wednesday": {"open": "12:00 PM", "close": "10:30 PM"},
    "Thursday":  {"open": "12:00 PM", "close": "10:30 PM"},
    "Friday":    {"open": "12:00 PM", "close": "11:30 PM"},
    "Saturday":  {"open": "12:00 PM", "close": "11:30 PM"},
    "Sunday":    {"open": "12:00 PM", "close": "10:00 PM"},
}

MENU = {
    "Small Plates": [
        {
            "name": "House Black Daal",
            "description": "Our famous slow-cooked black lentils, simmered for 24 hours with tomato, ginger and a touch of cream.",
            "price": 9.00,
        },
        {
            "name": "Chicken Berry Britannia",
            "description": "Chilli chicken with pomegranate, crispy rice and a yoghurt dressing.",
            "price": 11.50,
        },
        {
            "name": "Pau Bhaji",
            "description": "Mumbai street-food classic: spiced vegetable mash served with warm, buttered pau buns.",
            "price": 8.50,
        },
        {
            "name": "Okra Fries",
            "description": "Crispy fried bhindi dusted with chaat masala and served with a tamarind dip.",
            "price": 7.00,
        },
        {
            "name": "Dishoom Chilli Cheese Toast",
            "description": "Thick slices of white bread loaded with cheddar, green chillies, cumin and coriander.",
            "price": 7.50,
        },
    ],
    "Grills": [
        {
            "name": "Lamb Chops",
            "description": "Tender chops marinated overnight in spiced yoghurt, char-grilled to perfection.",
            "price": 19.50,
        },
        {
            "name": "Chicken Tikka",
            "description": "Boneless chicken thighs in a smoky, mildly spiced yoghurt marinade.",
            "price": 15.00,
        },
        {
            "name": "Seekh Kebab",
            "description": "Minced lamb with ginger, green chilli and fresh herbs, skewered and grilled in the tandoor.",
            "price": 14.50,
        },
        {
            "name": "Paneer Tikka",
            "description": "Cubes of fresh paneer with peppers and onions in a vibrant pepper and coriander marinade.",
            "price": 13.00,
        },
    ],
    "Biryanis": [
        {
            "name": "Chicken Biryani",
            "description": "Slow-cooked chicken layered with fragrant basmati rice, saffron and fried onions. Served with raita.",
            "price": 18.00,
        },
        {
            "name": "Lamb Biryani",
            "description": "Tender slow-braised lamb shoulder with basmati rice, whole spices and rose water.",
            "price": 20.00,
        },
        {
            "name": "Vegetable Biryani",
            "description": "Seasonal vegetables and paneer layered with fragrant basmati, topped with crispy shallots.",
            "price": 15.00,
        },
    ],
    "Desserts": [
        {
            "name": "Gulab Jamun",
            "description": "Soft milk-solid dumplings soaked in rosewater and cardamom syrup, served warm.",
            "price": 6.50,
        },
        {
            "name": "Kulfi",
            "description": "Traditional Indian ice cream in pistachio or mango, served on a stick.",
            "price": 6.00,
        },
        {
            "name": "Shrikhand",
            "description": "Strained yoghurt sweetened with sugar and cardamom, topped with seasonal fruit.",
            "price": 6.50,
        },
    ],
}


def format_hours() -> str:
    lines = ["Dishoom opening hours:"]
    for day, times in HOURS.items():
        lines.append(f"  {day}: {times['open']} – {times['close']}")
    return "\n".join(lines)


def format_menu() -> str:
    lines = ["Dishoom menu:"]
    for section, items in MENU.items():
        lines.append(f"\n{section}:")
        for item in items:
            lines.append(
                f"  • {item['name']} — {item['description']} (£{item['price']:.2f})"
            )
    return "\n".join(lines)
