from .base_exceptions import *


class EffectsDict(dict):
    """Game effect dictionary, contains effect classes."""

    def __init__(self):
        super().__init__()

        self.isPlayer: bool = False
        self.all_effects = None

        # for game and player links
        self.player = None
        self.game = None

    def copy_as_spellclass(self):
        """Create copy of EffectsDict class with object data"""
        obj = EffectsDict()
        obj.update(self.copy())
        return obj

    def effect_to_dict(self, effect) -> None:
        """Class decorator for adding effect"""
        try:
            self[effect.__ename__] = effect
        except AttributeError:
            raise ObjectIsNotEffect

    def effects_names(self) -> list:
        """Returns available effects name"""
        return [self[item].__ename__ for item in self]

    def effects_buff(self) -> list:
        """Returns available buff effects name"""
        return list(filter(lambda key: self[key].__type__ == "buff", self.keys()))

    def effects_debuff(self) -> list:
        """Returns available debuff effects name"""
        return list(filter(lambda key: self[key].__type__ == "debuff", self.keys()))

    def convert_to_player(self) -> None:
        """Convert dict to Player Spells dict"""
        self.all_effects = self.copy_as_spellclass()
        self.isPlayer = True
        self.clear()

    def give_effect(self, effect_name: str, duration: int) -> None:
        """Add effect to user"""
        if not self.isPlayer:
            raise NotPlayerEffectDict
        else:
            if duration < 0:
                raise NegativeNumberOfRounds
            self[effect_name] = self.all_effects[effect_name]()
            self[effect_name].__duration__ = duration

    def act(self) -> None:
        """Show effect effects"""
        for key in self.keys():
            self[key].act(game=self.game, player=self.player)

    def remove_expired(self) -> None:
        """Removes expired effects"""
        for key in self.keys():
            if self[key].__duration__ <= 0:
                self.pop(key)
