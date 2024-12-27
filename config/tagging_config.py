# bible_analysis/config/tagging_config.py

"""tagging config."""

# tagging_config.py

# Indicators for lifespan-related phrases
LIFESPAN_INDICATORS = {
    "lived for",
    "was",
    "amounted to",
    "became father to",
    "died at age",
    "were",
    "to be",
}

# Occupation keywords for matching
occupation_keywords = {
    "apothecary",
    "architect",
    "armor maker",
    "armor-bearer",
    "astrologer",
    "astronomer",
    "baker",
    "beggar",
    "blacksmith",
    "builder of city walls",
    "camel driver",
    "caretaker of sacred items",
    "carpenter",
    "charioteer",
    "chief of army",
    "choir member",
    "cook",
    "cupbearer",
    "cupmaker",
    "dancer",
    "dealer in purple cloth",
    "dyer",
    "elder",
    "executioner",
    "farmer",
    "fisher",
    "fisherman",
    "flock herder",
    "gatekeeper",
    "goldsmith",
    "governor",
    "harvester",
    "herder",
    "high priest",
    "horseman",
    "hunter",
    "judge",
    "king",
    "lawyer",
    "linen worker",
    "mason",
    "merchant",
    "metalworker",
    "midwife",
    "miller",
    "musician",
    "perfumer",
    "physician",
    "potter",
    "priest’s assistant",
    "priest",
    "prophet",
    "queen",
    "sandal maker",
    "scout",
    "scribe",
    "servant",
    "shepherd",
    "shipbuilder",
    "shipmaster",
    "singer",
    "slave",
    "slavegirl",
    "soldier",
    "spy",
    "stonecutter",
    "tax collector",
    "teacher",
    "temple servant",
    "tent weaver",
    "tent-dweller",
    "tentmaker",
    "trader",
    "vineyard keeper",
    "weaver",
    "winemaker",
}


# Keywords to exclude lifespan-related phrases
EXCLUSION_KEYWORDS = {"reigned", "gathered to", "length of", "satisfied with years"}

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
