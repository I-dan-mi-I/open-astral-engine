from .base_classes import SpellsDict

spells = SpellsDict()


@spells.append
class Level1Attack11:

    __sname__ = "Огненная стрела"
    __description__ = """Наносит врагу прямой урон в размере - 6 хп, на следующий ход накладывается эффект 'Горение' (периодический урон -2хп)."""
    __number__ = "11"
    __level__ = 1
    __priority__ = 28
    __distribution_type__ = "a"
    __type__ = ("directed", "enemy")
    __mp__ = 3
    __mp_loss__ = __mp__
    __synergy__ = """Эффект Ядовитый плевок
    
1. В сочетании с эффектом "Теневой клинок" (Эффект на кастере)  - усиливает клинки ядом (накладывает на цель 1 тик "Ядовитый плевок" -3хп на след раунд)                                                             
2. В сочитании с заклинанием "Ярость дракона" усиливает пламя Ядом                                                  
3. В сочитании с заклинанием "Форма Дракона", меняет цвет дракона на "Зеленый"
4. В сочетании с эффектом "Бег" наносит -2хп периодический урон в текущем раунде  
5. В сочетании с заклинанием "Огненная стрела"  усиливает урон стрелы до -7хп и вместо "Горения" накладывает "Трупный яд" на след раунд;
6. При наличии эффекта "Радиация" (Эффект на кастере) плевок накладывает развеиваемый эффект "Токсин" на 3 раунда с текущего  (-4хп, -2 макс хп)
7. В сочетании с эффектом "Астральная мина" (Эффект на цели) меняет тип мины на "Токсичная мина" 
8. При наличии эффекта "Влага" или "Капля" (Эффект на кастере) меняет атаку на водный удар - наносит в текущем раунде -8хп периодическим уроном, накладывает "Влага3" на следующий раунд"""

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def move(self, target=None):
        caster_effects = self.player.effects.effects_names()
        if target is None:
            target = self.player.move_direction
        target_effects = target.effects.effects_names()

        arrow_name = "Огненную"
        arrow_damage = 6

        if self == target:
            target_name = "себе"
        else:
            target_name = target.name

        if list(set(caster_effects) & {"Злобный разум", "Астральный паразит"}):
            arrow_name = "Ментальную"
            # target.effects.give_effect("Сжигание энергии", 1)
        elif list(set(caster_effects) & {"Кровосток", "Кровотечение"}):
            arrow_name = "Зазубренную"
            arrow_damage = 7
            # target.effects.give_effect("Кровотечеие", 99)
        elif list(set(caster_effects) & {"Ядовитый плевок", "Трупный яд"}):
            arrow_name = "Отравленную"
            arrow_damage = 7
            # target.effects.give_effect("Трупный яд", 99)
        elif list(set(caster_effects) & {"Ледяной укус", "Обморожение"}):
            arrow_name = "Ледяную"
            arrow_damage = 0
            # target.effects.give_effect("Обморожение", 99)
        else:
            target.effects.give_effect("Горение✶2", 1)

        target.main_damage = arrow_damage
        self.player.mp_loss = self.__mp_loss__

        if list(set(target_effects) & {"Каменный еж", "Огонек", "Висп"}) and arrow_damage != 0:
            counter_move = target.spells.all_spells['11'](self.game, target)
            counter_move(self.player)

        self.player.spells.remove(self)

        return f"{self.player.name} выпускает {arrow_name} стрелу по {target_name} (№11)"
