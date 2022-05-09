from .buff import effects as buff_effects
from .debuff import effects as debuff_effects
from .base_classes import EffectsDict

__update__ = "07.05.2022"

effects = EffectsDict()
effects.update(buff_effects.copy())
effects.update(debuff_effects.copy())


def get_player_effects_dict(game, player_class) -> EffectsDict:
    player: EffectsDict = effects.copy_as_spellclass()
    player.game = game
    player.player = player_class
    player.convert_to_player()
    return player
