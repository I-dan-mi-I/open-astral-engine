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
        super().__init__("This spell is not in the player's spell dictionary.")


class NotEnoughMpToMove(Exception):
    def __init__(self):
        super().__init__("The spell requested by the caster requires more MP than he has.")


class NoAbilityToMove(Exception):
    def __init__(self):
        super().__init__("The caster is unable to make a move.")


class SpellNeedDirection(Exception):
    def __init__(self):
        super().__init__("The requested spell does not have an explicit direction.")


class WrongDirection(Exception):
    def __init__(self):
        super().__init__("Wrong indication of move direction.")


class SpecifiedPlayerIsDead(Exception):
    def __init__(self):
        super().__init__("The target indicated by the caster is dead.")
