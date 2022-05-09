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

    def copy(self):
        """Create copy of EffectsDict class with object data"""
        obj = EffectsDict()
        obj.update(super().copy())
        return obj

    def append(self, effect) -> None:
        """Class decorator for adding effect"""
        try:
            self[effect.__ename__] = effect
        except AttributeError:
            raise ObjectIsNotEffect

    def effects_names(self) -> list:
        """Returns available effects name"""
        return [self[item].__ename__ for item in self]

    def effects_names_sorted_by_fluttering(self) -> str:
        """Returns available effects name sorted by fluttering"""
        fluttering_effects = [self[item] if self[item].__fluttering__ else None for item in self]
        non_fluttering_effects = [self[item] if not self[item].__fluttering__ else None for item in self]

        def remove_none(massive: list):
            """Remove NoneType object from list"""
            while True:
                try:
                    massive.remove(None)
                except ValueError:
                    return massive

        fluttering_effects, non_fluttering_effects = map(remove_none, (fluttering_effects, non_fluttering_effects))

        effects_str = ', '.join(f"{effect.__ename__}{f'✶{effect.__eindex__}' if effect.__eindex__ != -1 else ''}" for effect in fluttering_effects) + ("\nНеразвеиваемые: " if len(non_fluttering_effects) != 0 else '') + ', '.join(effect.__ename__ for effect in non_fluttering_effects)

        return effects_str

    def effects_buff(self) -> list:
        """Returns available buff effects name"""
        return list(filter(lambda key: self[key].__type__ == "buff", self.keys()))

    def effects_debuff(self) -> list:
        """Returns available debuff effects name"""
        return list(filter(lambda key: self[key].__type__ == "debuff", self.keys()))

    def convert_to_player(self) -> None:
        """Convert dict to Player Spells dict"""
        self.all_effects = self.copy()
        self.isPlayer = True
        self.clear()

    def give_effect(self, effect_name: str, duration: int) -> None:
        """Add effect to user"""
        if not self.isPlayer:
            raise NotPlayerEffectDict
        else:
            if duration < 0:
                raise NegativeNumberOfRounds

            effect_list = effect_name.split('✶')
            match effect_list:
                case [effect_name, index]:
                    if not isinstance(effect_name, str) or not isinstance(index, str):
                        raise IncorrectIndexedEffectRequest

                    if self.all_effects[effect_name].__eindex__ == -1:
                        raise IncorrectEffectRequest

                    index = int(index)
                    if index <= 0:
                        raise NegativeEffectIndex

                    self[effect_name] = self.all_effects[effect_name](self.game, self.player)
                    self[effect_name].__duration__ = duration
                    self[effect_name].__eindex__ = index

                case [effect_name]:
                    if not isinstance(effect_name, str):
                        raise IncorrectEffectRequest

                    if self.all_effects[effect_name].__eindex__ != -1:
                        raise IncorrectIndexedEffectRequest

                    self[effect_name] = self.all_effects[effect_name](self.game, self.player)
                    self[effect_name].__duration__ = duration

    def act(self) -> None:
        """Show effect effects"""
        if self.player.hp > 0:
            for key in self.keys():
                self[key].act()

    def remove_expired(self) -> None:
        """Removes expired effects"""
        for key in self.keys():
            if self[key].__duration__ <= 0:
                self.pop(key)
