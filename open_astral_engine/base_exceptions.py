class OddNumberOfPlayers(Exception):
    def __init__(self):
        super().__init__("Please add or remove a player (bot).")


class DefunctPlayer(Exception):
    def __init__(self):
        super().__init__("The name of a non-existent player was specified.")


class ExistingPlayer(Exception):
    def __init__(self):
        super().__init__("The player you specified already exists.")


class NonDictionarySpell(Exception):
    def __init__(self):
        super().__init__("NaN")


class NotEnoughMpToMove(Exception):
    def __init__(self):
        super().__init__("NaN")


class NoAbilityToMove(Exception):
    def __init__(self):
        super().__init__("NaN")


class SpellNeedDirection(Exception):
    def __init__(self):
        super().__init__("NaN")


class WrongDirection(Exception):
    def __init__(self):
        super().__init__("NaN")


class SpecifiedPlayerIsDead(Exception):
    def __init__(self):
        super().__init__("NaN")
