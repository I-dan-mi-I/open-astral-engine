from .level1_attack import spells as level1_attack_spells
from .level1_def import spells as level1_def_spells
from .base_classes import SpellsDict

__update__ = "07.05.2022"

spells = SpellsDict()
spells.update(level1_attack_spells.copy())
spells.update(level1_def_spells.copy())


class Level0Skip:
    __sname__ = "Пропуск хода"
    __description__ = "Пропуск хода"
    __number__ = "х"
    __level__ = 1
    __priority__ = 0
    __distribution_type__ = ""
    __type__ = ("directed", "ally")
    __mp__ = 0
    __synergy__ = ""

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def move(self) -> str:
        return f"{self.player.name} бездействует, пропуская ход."


def get_player_spells_dict(game, player_class) -> SpellsDict:
    player: SpellsDict = spells.copy()
    player.game = game
    player.player = player_class
    player.convert_to_player()
    return player
