from .buff import effects as buff_effects
from .debuff import effects as debuff_effects
from .base_classes import EffectsDict

# Effects Lib
# Effect example:

# @effects.append # This decorator is used to include a effect in the dictionary.
# class BuffExample:
#
#     __ename__ = "Example"
#     __description__ = """description"""
#     __fluttering__ = False
#     __event__ = False
#     __duration__ = 0
#     __eindex__ = -1 # If __eindex__ != -1, then the effect is indexable.
#     __type__ = "buff" # Buff or Debuff
#     __synergy__ = """Synergy example"""
#
#     def __init__(self, game, player):
#         self.game = game
#         self.player = player
#
#     def act(self):
#         pass

__update__ = "09.05.2022"

effects = EffectsDict()
effects.update(buff_effects.copy())
effects.update(debuff_effects.copy())


def get_player_effects_dict(game, player_class) -> EffectsDict:
    player: EffectsDict = effects.copy()
    player.game = game
    player.player = player_class
    player.convert_to_player()
    return player
