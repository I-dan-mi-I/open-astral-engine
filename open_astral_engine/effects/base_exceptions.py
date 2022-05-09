class ObjectIsNotEffect(Exception):
    def __init__(self):
        super().__init__("The specified object is not a effect class.")


class NotPlayerEffectDict(Exception):
    def __init__(self):
        super().__init__("This is not the player's dictionary.")


class NegativeNumberOfRounds(Exception):
    def __init__(self):
        super().__init__(
            "You are trying to apply the effect on a negative number of rounds."
        )


class NegativeEffectIndex(Exception):
    def __init__(self):
        super().__init__(
            "You are trying to apply the effect with a negative index."
        )


class IncorrectIndexedEffectRequest(Exception):
    def __init__(self):
        super().__init__(
            "Error in building indexed effect."
        )


class IncorrectEffectRequest(Exception):
    def __init__(self):
        super().__init__(
            "Error in building effect."
        )
