from .level1_attack import spells as level1_attack_spells
from .level1_def import spells as level1_def_spells
from .base_classes import SpellsDict

#Spells Lib
#Example of spell object

# @spells.append # This decorator is used to include a spell in the dictionary.
# class LevelXAttackY (LevelXDefY):
#     __sname__ = "Spell Name"
#     __description__ = """Spell Description"""
#     __number__ = "Y" # This number is also used as a spell dictionary key.
#     __level__ = X
#     __priority__ = 0 # The more, the higher the spell will be in the execution queue.
#     __distribution_type__ = "a" # Spell type used to distribute one- and two-level spells, not used for three-level spells and skills (remains at "")
#     __type__ = ("directed", "enemy") # Spell type by direction
#     __mp__ = 3 # MP cost used to determine if a spell can be used. If your spell is free, put -100.
#     __mp_loss__ = __mp__ # The actual MP cost is often the same as __mp__, but if your spell is free, put 0.
#     __synergy__ = "synergy description"
#
#     def __init__(self, game, player):
#         self.game = game
#         self.player = player
#
#     def move(self, target=None) -> str:
# Used to calculate the spell, keep in mind that you yourself need
# to add the damage to the target's mine_damage attribute,
# as well as the mp cost to the caster's mp_loss attribute.
#         if target is None:
#             target = self.player.move_direction
#
#         target.main_damage = damage
#         self.player.mp_loss = self.__mp_loss__
#
# Return spell
#
#         if list(set(target_effects) & {"Каменный еж", "Огонек", "Висп"}) and damage != 0:
#             counter_move = target.spells.all_spells[self.__number__](self.game, target)
#             counter_move(self.player)
#
# Removing a used spell from a caster's array of spells
#
#         self.player.spells.remove(self)
#
# The string returned by the function that is used in the game message.
#
#         return f"{self.player.name} выпускает {arrow_name} стрелу по {target_name} (№11)"

__update__ = "09.05.2022"

spells = SpellsDict()
spells.update(level1_attack_spells.copy())
spells.update(level1_def_spells.copy())


# Utility spell to skip a turn
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

# Returns the player's spell dictionary
def get_player_spells_dict(game, player_class) -> SpellsDict:
    player: SpellsDict = spells.copy()
    player.game = game
    player.player = player_class
    player.convert_to_player()
    return player
