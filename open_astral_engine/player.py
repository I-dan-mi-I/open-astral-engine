from .base_exceptions import (
    NonDictionarySpell,
    NotEnoughMpToMove,
    NoAbilityToMove,
    SpellNeedDirection,
    WrongDirection,
    SpecifiedPlayerIsDead,
)
from .spells import get_player_spells_dict
from .effects import get_player_effects_dict
from math import floor
from .team import AstralTeam


class AstralPlayer:
    """Astral Player class"""

    def __init__(
        self,
        game,
        name: str,
        hp: int = 30,
        mp: int = 30,
        max_hp: int = 30,
        max_mp: int = 40,
    ):
        # user identification data
        self.name: str = name
        self.team: AstralTeam = None

        self.bot: bool = False
        self.moved: bool = False
        self.move_ability: bool = True

        self.move_cancelation: bool = False

        # HP and MP limits
        self.max_hp: int = max_hp
        self.max_mp: int = max_mp

        # current hp and mp
        self.hp: int = hp
        self.mp: int = mp

        # spells and effects
        self.spells = get_player_spells_dict(game, self)
        self.effects = get_player_effects_dict(game, self)

        # game object
        self.game = game

        # move params
        self.move = None
        self.move_direction = None

        # round params
        self.main_mp_regeneration: int = 0
        self.additional_mp_regeneration: int = 0
        self.spell_mp_regeneration: int = 0
        self.mp_loss: int = 0
        self.mp_loss_multiplier: float = 1.0
        self.mp_loss_additional: int = 0
        self.main_damage: int = 0
        self.damage_over_time: int = 0
        self.effect_heal: int = 0
        self.spell_heal: int = 0
        self.armor: int = 0

    def kick(self):
        """Removes a user from the current game"""
        self.game.players.remove(self)

    def new_round(self):
        """Clears the current params"""
        if self.hp > 0:
            self.moved: bool = False
            self.move_ability: bool = True
        else:
            self.moved: bool = True
            self.move_ability: bool = False

        self.move = None
        self.move_direction = None

        if self.hp > 0:
            if 1 < self.game.round <= 5:
                self.main_mp_regeneration += 1
            elif 6 <= self.game.round <= 15:
                self.main_mp_regeneration += 2
            elif self.game.round >= 16:
                self.main_mp_regeneration += 3

        self.additional_mp_regeneration: int = 0
        self.spell_mp_regeneration: int = 0
        self.mp_loss: int = 0
        self.mp_loss_multiplier: float = 1.0
        self.mp_loss_additional: int = 0
        self.main_damage: int = 0
        self.damage_over_time: int = 0
        self.effect_heal: int = 0
        self.spell_heal: int = 0
        self.armor: int = 0

    def set_move(self, spell_name, direction=None) -> None:
        """Sets the current spell and direction of the caster.
        If the spell explicitly reflects the direction of the move, then it is not required."""
        if not self.moved and self.move_ability:
            another_player = (
                self.game.get_player_by_name(direction)
                if direction is not None
                else None
            )

            spell = self.spells[spell_name]

            if len(self.game.players) == 2 and another_player is None:
                if 'ally' in spell.__type__:
                    another_player = self
                elif 'enemy' in spell.__type__:
                    for team in list(self.game.teams.keys()):
                        if team != self.team:
                            another_player = self.game.teams[team][0]

            self.move = spell
            self.move_direction = another_player
            self.moved = True
        else:
            raise NoAbilityToMove

    def checker(self, spell_name, direction=None) -> None:
        """Checks if a spell can be used.
        If everything is fine, it returns nothing, otherwise it will trigger an error."""
        if not self.moved and self.move_ability:
            if spell_name not in list(self.spells.keys()):
                raise NonDictionarySpell
            else:
                if ((floor(self.mp_loss * self.mp_loss_multiplier) + self.mp_loss_additional) if self.mp_loss != 0 else 0) > self.mp:
                    raise NotEnoughMpToMove
                elif "direction" in list(self.spells[spell_name].__type__) and (
                    not list(
                        set(self.spells[spell_name].__type__) & {"enemy", "ally"}
                    )
                    or len(self.game.players) > 2
                ):
                    if direction is None:
                        raise SpellNeedDirection
                    else:
                        return self.__checker_direction(spell_name, direction)
                else:
                    return None
        else:
            raise NoAbilityToMove

    def __checker_direction(self, spell_name, direction) -> None:
        """Checks the direction of the spell for spells without explicitly specifying it,
        or if there are more than 2 players."""
        another_player: AstralPlayer = self.game.get_player_by_name(direction)
        spell = self.spells[spell_name]

        if list({"enemy", "ally"} & set(spell.__type__)):
            if self.team != another_player.team:
                return None
            else:
                raise WrongDirection
        else:
            if another_player.hp > 0:
                return None
            else:
                raise SpecifiedPlayerIsDead

    def before_move_count(self):
        """Calculates the influence of natural processes and the influence of effects."""
        self.mp = (
            self.mp
            + self.main_mp_regeneration
            + self.additional_mp_regeneration

        )
        if self.mp > self.max_mp:
            self.mp = self.max_mp

        self.hp = self.hp + self.effect_heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def after_move_count(self):
        """Calculates the impact of player actions."""
        self.mp = (
                self.mp
                + self.spell_mp_regeneration
                - (floor(self.mp_loss * self.mp_loss_multiplier) + self.mp_loss_additional) if self.mp_loss != 0 else 0

        )
        if self.mp > self.max_mp:
            self.mp = self.max_mp

        damage = self.main_damage + self.damage_over_time - self.armor
        if damage < 0:
            damage = 0
        self.hp = self.hp - damage + self.spell_heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp
