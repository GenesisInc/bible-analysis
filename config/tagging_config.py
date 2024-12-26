# bible_analysis/config/tagging_config.py

""" tagging config """

# Keywords for detecting relationships
RELATIONSHIP_KEYWORDS = [
    "son of",
    "daughter of",
    "father of",
    "mother of",
    "descendant of",
    "ancestor of",
    "brother of",
    "sister of",
    "wife of",
    "husband of",
]

# Keywords for detecting events
EVENT_KEYWORDS = [
    "battle",
    "war",
    "celebration",
    "miracle",
    "travel",
    "gift",
    "purchase",
    "covenant",
    "sacrifice",
    "plague",
]

# Additional entity categories for future tagging
ADDITIONAL_CATEGORIES = {
    "miracles": [
        "parted sea",
        "healing",
        "resurrection",
        "manna",
    ],
    "directions": [
        "north",
        "south",
        "east",
        "west",
    ],
    "items": [
        "gold",
        "silver",
        "bronze",
        "sheep",
        "goats",
    ],
}

# Confidence threshold for lifespan detection
# LIFESPAN_CONFIDENCE_THRESHOLD = 0.75
LIFESPAN_CONFIDENCE_THRESHOLD = 0.25
