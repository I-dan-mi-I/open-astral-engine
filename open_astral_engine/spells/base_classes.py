from random import choice
from .base_exceptions import *


class SpellsDict(dict):
    """Game spells dictionary, contains spell classes."""

    def __init__(self):
        super().__init__()

        self.isPlayer: bool = False
        self.all_spells = None

        # for game and player links
        self.player = None
        self.game = None

    def copy(self):
        """Create copy of SpellsDict class with object data"""
        obj = SpellsDict()
        obj.update(super().copy())
        return obj

    def append(self, spell) -> None:
        """Class decorator for adding spells"""
        try:
            self[spell.__number__] = spell
        except AttributeError:
            raise ObjectIsNotSpell

    def spells_numbers(self) -> list:
        """Returns available spells number"""
        return list(self.keys())

    def spells_names(self) -> list:
        """Returns available spells name"""
        return [self[item].__sname__ for item in self]

    def spells_attack(self) -> list:
        """Returns available attack spells numbers"""
        return list(
            filter(lambda key: self[key].__distribution_type__ == "a", self.keys())
        )

    def spells_def(self) -> list:
        """Returns available def spells numbers"""
        return list(
            filter(lambda key: self[key].__distribution_type__ == "d", self.keys())
        )

    def convert_to_player(self) -> None:
        """Convert dict to Player Spells dict"""
        if not list({"11", "112", "119", "124"} & set(self.keys())):
            raise AnUnfinishedDictionary
        self.all_spells = self.copy()
        self.isPlayer = True
        self.clear()
        for spell in ["11", "112", "119", "124"]:
            self[spell] = self.all_spells[spell](self.game, self.player)

    def give_spell(self, spell_name) -> None:
        """Add spell to user"""
        if not self.isPlayer:
            raise NotPlayerSpellsDict
        else:
            self[spell_name] = self.all_spells[spell_name]()

    def distribute_spells(self, rule: str) -> None:
        """Add spell according to given rule"""
        if not self.isPlayer:
            raise NotPlayerSpellsDict
        else:
            rules = rule.strip().split("х")
            for rule in rules:
                rule_lower = rule.lower()
                if len(rule_lower) == 2:
                    spell = choice(
                        list(
                            filter(
                                lambda key: self.all_spells[key].__level__
                                == int(rule_lower[0])
                                and self.all_spells[key].__distribution_type__
                                == rule_lower[1]
                                and key not in list(self.keys()),
                                self.all_spells.keys(),
                            )
                        )
                    )
                    self[spell] = self.all_spells[spell](self.game, self.player)
                else:
                    spell = choice(
                        list(
                            filter(
                                lambda key: self.all_spells[key].__level__
                                == int(rule_lower)
                                and key not in list(self.keys()),
                                self.all_spells.keys(),
                            )
                        )
                    )
                    self[spell] = self.all_spells[spell](self.game, self.player)
