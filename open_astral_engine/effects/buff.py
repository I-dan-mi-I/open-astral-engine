from .base_classes import EffectsDict

effects = EffectsDict()


@effects.append
class BuffExample:

    __ename__ = "Название Бафф"
    __description__ = """Описание"""
    __fluttering__ = False
    __event__ = False
    __duration__ = 0
    __eindex__ = -1
    __type__ = "buff"
    __synergy__ = """Синергии"""

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def act(self):
        pass
