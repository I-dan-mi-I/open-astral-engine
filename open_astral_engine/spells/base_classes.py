from random import choice
from .base_exceptions import *


class SpellsDict(dict):
    """Game spell dictionary, contains spell classes."""

    def __init__(self):
        super().__init__()

        self.player: bool = False
        self.all_spells = None

    def copy_as_spellclass(self):
        """Create copy of SpellsDict class with object data"""
        obj = SpellsDict()
        obj.update(self.copy())
        return obj

    def spell_to_dict(self, spell) -> None:
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
        return list(filter(lambda key: self[key].__distribution_type__ == 'a', self.keys()))

    def spells_def(self) -> list:
        """Returns available def spells numbers"""
        return list(filter(lambda key: self[key].__distribution_type__ == 'd', self.keys()))

    def convert_to_player(self):
        """Convert dict to Player Spells dict"""
        if not list(set(['11', '112', '119', '124']) & set(self.keys())):
            raise AnUnfinishedDictionary
        self.all_spells = self.copy_as_spellclass()
        self.player = True
        self.clear()
        for spell in ['11', '112', '119', '124']:
            self[spell] = self.all_spells[spell]

    def distribute_spells(self, rule: str):
        if not self.player:
            raise NotPlayerSpellsDict
        else:
            rules = rule.strip().split("x")
            for rule in rules:
                rule_lower = rule.lower()
                if len(rule_lower) == 2:
                    spell = choice(list(filter(
                                lambda key: self.all_spells[key].__level__
                                == int(rule_lower[0])
                                and self.all_spells[key].__distribution_type__
                                == rule_lower[1]
                                and key not in list(self.keys()),
                                self.all_spells.keys(),
                            )))
                    self[spell] = self.all_spells[spell]
                else:
                    spell = choice(list(filter(
                                lambda key: self.all_spells[key].__level__
                                == int(rule_lower)
                                and key not in list(self.keys()),
                                self.all_spells.keys(),
                            )))
                    self[spell] = self.all_spells[spell]
