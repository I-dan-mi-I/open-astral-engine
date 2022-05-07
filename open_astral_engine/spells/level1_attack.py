from .base_classes import SpellsDict

spells = SpellsDict()


@spells.spell_to_dict
class Level1Attack11:

    __sname__ = "Огненная стрела"
    __description__ = """Наносит врагу прямой урон в размере - 6 хп, на следующий ход накладывается эффект 'Горение' (периодический урон -2хп)."""
    __number__ = "11"
    __level__ = 1
    __priority__ = 28
    __distribution_type__ = "a"
    __type__ = ("directed", "enemy")
    __mp__ = 3
    __synergy__ = """Эффект Ядовитый плевок
    
1. В сочетании с эффектом "Теневой клинок" (Эффект на кастере)  - усиливает клинки ядом (накладывает на цель 1 тик "Ядовитый плевок" -3хп на след раунд)                                                             
2. В сочитании с заклинанием "Ярость дракона" усиливает пламя Ядом                                                  
3. В сочитании с заклинанием "Форма Дракона", меняет цвет дракона на "Зеленый"
4. В сочетании с эффектом "Бег" наносит -2хп периодический урон в текущем раунде  
5. В сочетании с заклинанием "Огненная стрела"  усиливает урон стрелы до -7хп и вместо "Горения" накладывает "Трупный яд" на след раунд;
6. При наличии эффекта "Радиация" (Эффект на кастере) плевок накладывает развеиваемый эффект "Токсин" на 3 раунда с текущего  (-4хп, -2 макс хп)
7. В сочетании с эффектом "Астральная мина" (Эффект на цели) меняет тип мины на "Токсичная мина" 
8. При наличии эффекта "Влага" или "Капля" (Эффект на кастере) меняет атаку на водный удар - наносит в текущем раунде -8хп периодическим уроном, накладывает "Влага3" на следующий раунд"""