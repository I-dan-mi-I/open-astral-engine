from .level1_attack import spells as level1_attack_spells
from .level1_def import spells as level1_def_spells
from .base_classes import SpellsDict

__update__ = '07.05.2022'

spells = SpellsDict()
spells.update(level1_attack_spells.copy())
spells.update(level1_def_spells.copy())


def get_player_spells_dict() -> SpellsDict:
    player = spells.copy_as_spellclass()
    player.convert_to_player()
    return player
