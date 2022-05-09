class ObjectIsNotSpell(Exception):
    def __init__(self):
        super().__init__("The specified object is not a spell class.")


class NotPlayerSpellsDict(Exception):
    def __init__(self):
        super().__init__("This is not the player's dictionary.")


class AnUnfinishedDictionary(Exception):
    def __init__(self):
        super().__init__(
            "There are no starting spells in this dictionary to initialize the game."
        )
