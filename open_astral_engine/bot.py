from .spells import get_player_spells_dict
from .effects import get_player_effects_dict


class AstralBot:
    def __init__(
        self,
        game,
        name: str = "AstralBot",
        hp: int = 30,
        mp: int = 30,
        max_hp: int = 30,
        max_mp: int = 40,
    ):
        # идентификационные данные
        self.name: str = name
        self.team: str = ""

        self.bot: bool = True
        self.moved: bool = True
        self.move_ability: bool = True

        # ограничение хп, мп
        self.max_hp: int = max_hp
        self.max_mp: int = max_mp

        # текущие параметры
        self.hp: int = hp
        self.mp: int = mp

        # спеллы и эффекты
        self.spells = get_player_spells_dict(game, self)
        self.effects = get_player_effects_dict(game, self)

        # параметры игры
        self.game = game

        # параметры хода
        self.move = None

        # параметры раунда:
        self.main_mp_regeneration: int = 0
        self.additional_mp_regeneration: int = 0
        self.mp_loss: int = 0
        self.main_damage: int = 0
        self.damage_over_time: int = 0
        self.heal: int = 0
        self.armor: int = 0

    def new_round(self):
        self.moved = True
        if self.hp > 0:
            self.move_ability: bool = True
        else:
            self.move_ability: bool = False

        # параметры хода
        self.move = None
        self.move_direction = None

        # параметры раунда:
        if self.hp > 0:
            if 1 < self.game.round <= 5:
                self.main_mp_regeneration += 1
            elif 6 <= self.game.round <= 15:
                self.main_mp_regeneration += 2
            elif self.game.round >= 16:
                self.main_mp_regeneration += 3

        self.additional_mp_regeneration: int = 0
        self.mp_loss: int = 0
        self.main_damage: int = 0
        self.damage_over_time: int = 0
        self.heal: int = 0
        self.armor: int = 0

    def premove(self):
        self.mp = (
            self.mp
            + self.main_mp_regeneration
            + self.additional_mp_regeneration
            - self.mp_loss
            - self.mp_spend
        )
        if self.mp > self.max_mp:
            self.mp = self.max_mp

        damage = self.main_damage + self.damage_over_time - self.armor
        if damage < 0:
            damage = 0
        self.hp = self.hp - damage + self.heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        # логика бота по выбору спелла
