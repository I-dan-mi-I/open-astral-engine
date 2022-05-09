from .base_classes import EffectsDict


effects = EffectsDict()


@effects.append
class DebuffExample:

    __ename__ = "Название Дебафф"
    __description__ = """Описание"""
    __fluttering__ = False
    __event__ = False
    __duration__ = 0
    __eindex__ = -1
    __type__ = "debuff"
    __synergy__ = """Синергии"""

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def act(self):
        pass


@effects.append
class DebuffCombustion:

    __ename__ = "Горение"
    __description__ = """Кастер получает периодический урон, равный индексу"""
    __fluttering__ = True
    __event__ = False
    __duration__ = 0
    __eindex__ = 0
    __type__ = "debuff"
    __synergy__ = """1. В сочетании с заклинанием "Порыв ветра" дает эффект "Горение" на следущий раунд (-2хп)                                 
2. В сочетании с заклинанием "Ярость дракона" усиливает пламя "Пеклом 3х"                                                  
3. В сочетании с заклинанием "Форма Дракона", меняет цвет дракона на "Красный"
4. В сочетании с заклинанием "Торнадо" - меняет действие заклинания - наносит -8хп периодическим уроном в текущем раунде, накладывает на следующий раунд эффекты:  "Левитация, Страх, Пекло5, Горение4".
5. В сочетании с заклинанием "Огненный шар" усиливает прямой урон на -1хп и усиливает "Пекло" на -1хп   
6. В сочетании с одним из эффектов "Ливень, Коррозия, Капля" эффект исчезает """

    def __init__(self, game, player):
        self.game = game
        self.player = player

    def act(self):
        pass
