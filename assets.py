# contains information on which locations are where in the world map
MAP_SETUP = {"Swamp": {"E": "Forest"}, "Forest": {"W": "Swamp", "S": "Cauldron", "E": "Town"},
             "Cauldron": {"N": "Forest"}, "Town": {"W": "Forest", "N": "Cave", "E": "Graveyard"},
             "Cave": {"S": "Town"}, "Graveyard": {"W": "Town"}}

# contains information on which chapters have which titles
CHAPTER_TITLES = {"0": "Wounds", "1": "Ailments", "2": "Curses", "3": "Hauntings"}

# contains information on which chapters contain which Item recipes
RECIPES_BY_CHAPTER = {"0": ["Health Potion", "Goodberry"], "1": ["Antidote", "Awakening"],
                      "2": ["Evil Eye", "Amulet"], "3": ["Banishing Sigil", "Substitute Doll"]}

# contains information on which Items belong to which difficulty tier
ITEMS_BY_INGREDIENTS = {"FOUND": ["Purple Mushroom", "Forget-Me-Not", "Firefly", "Mandrake Root", "Green Mushroom",
                        "Spring Water", "Red Mushroom", "Glow Worm", "Skull"],
                        "BASIC": ["Goodberry", "Antidote",  "Evil Eye",],
                        "INTERMEDIATE": ["Health Potion", "Awakening", "Amulet"],
                        "ADVANCED": ["Banishing Sigil", "Substitute Doll"]}

# contains information on Location flavor text
LOCATION_FLAVOR = {"Swamp": ["Ew what's that smell?", "I'm sinking into the bog!",
                             "This spooky Swamp sure is muddy!", "Gross...let's be quick!"],
                   "Forest": ["It's quiet here. Too quiet. Spooky quiet.",
                              "These birds keep looking at me.", "Wait, those aren't birds!"],
                   "Cauldron": ["Home sweet home.", "Oops, I left the Cauldron on.",
                                "Another day, another dollar.", "Ugh, who is it now?"],
                   "Town": ["I don't think these people like me.", "Where is everybody?",
                            "'Everyone run; it's the witch!' Real original."],
                   "Cave": ["It's too dark in here.", "What was that noise?!",
                            "Whoops! Slipped on a rock!"],
                   "Graveyard": ["I think I heard a ghost calling my name!",
                                 "Whoops! Tripped over something. Don't look down.",
                                 "RIP everyone, I'll only be a minute, 'scuse me."]}

# contains information on valid inputs that will be displayed to the user
INPUTS_DISPLAY = ["Up Arrow - Move North", "Down Arrow - Move South", "Left Arrow - Move West",
                  "Right Arrow - Move East", "P - Pickup Item", "T - Trash Item", "H - Return to Cauldron",
                  "B - Read Recipe Book", "M - Mix Ingredients", "D - Deliver Order to Customer",
                  "Q - Quit the Game"]