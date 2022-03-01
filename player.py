from spells_sorted import spells_distribution

mxp = 30 # макс хп
mmp = 40 # макс мп
mag = -1 # макс агр

skills = [ # умения
    'м',
    'б',
    'д',
    'л',
    'гг',
    'о',
    'ж',
    'ф',
    'п',
    'с'
]

direction2 = ['119', '140', '168', '242', '245'] # спеллы, требующие направление при игре на 2

# спеллы кранятся в массиве player.spells в формате string

# эффекты хранятся в словаре player.effects в формате
# {
# 'эффект' : {кол-во раундов}
# }

class player(object):
    """Astral player class"""

    def __init__(self, name, team):
        # идентификационные данные
        self.name: string = name
        self.team: string = team

        # ограничение хп, мп и агра
        self.max_xp: int = mxp
        self.max_mp: int = mmp
        self.max_ag: int = mag

        # текущие параметры
        self.hp: int = 30
        self.mp: int = 30

        # параметры предыдущего рануда
        self.old_hp: int = 30
        self.old_mp: int = 30

        # спеллы и эффекты
        self.spells: list = []
        self.avaliable_spells: list = self.spells
        self.effects: dict = {}

        # параметры игры
        self.players: list = []
        self.players_name: list = []
        self.crew: list = []
        self.enemy: list = []

        # параметры хода
        self.move: str = ''
        self.move_direction: str = ''
        self.ability: bool = True
        self.move_message: str = ''
        self.round = 0

        # параметры раунда:
        self.main_mp_regeneration: int = 0
        self.additional_mp_regeneration: int = 0
        self.mp_loss: int = 0
        self.main_damage: int = 0
        self.mp_spend: int = 0
        self.round: int = 0
        self.damage_over_time: int = 0
        self.heal: int = 0
        self.armor: int = 0

        self.move_answer = {}
        # структура
        # '{PlayerName}': {
        # 'main_mp_regeneration': {int},
        # 'additional_mp_regeneration': {int},
        # 'mp_loss': {int},
        # 'main_damage': {int},
        # 'mp_spend': {int},
        # 'damage_over_time': {int},
        # 'heal': {int},
        # 'armor': {int},
        # 'additional_effects': {
        # '{effect}: {int}
        # }
        # }

        # получаемые из игры данные
        self.game_message: str = ''

    # проверка корректности хода
    def check(self, move):
        if move['spell'] in self.avaliable_spells:
            if move['spell'] in direction2:
                try:
                    direction = move['direction']
                except:
                    direction = ''
                    pass
                
                if direction not in self.players_name:
                    return 'check direction'
                else:
                    return 'ok'
            else:
                return 'ok'
        else:
            return 'spell is not avaliable'

    # предварительный расчёт
    def pre_move_count(self, move_answer):
        try:
            self.main_mp_regeneration += move_answer['main_mp_regeneration']
        except:
            pass

        try:
            self.additional_mp_regeneration += move_answer['additional_mp_regeneration']
        except:
            pass

        try:
            self.mp_loss += move_answer['mp_loss']
        except:
            pass

        try:
            self.main_damage += move_answer['main_damage']
        except:
            pass

        try:
            self.mp_spend += move_answer['mp_spend']
        except:
            pass

        try:
            self.damage_over_time += move_answer['damage_over_time']
        except:
            pass

        try:
            self.heal += move_answer['heal']
        except:
            pass

        try:
            self.armor += move_answer['armor']
        except:
            pass

        try:
            self.effects = self.effects | move_answer['additional_effects']
        except:
            pass

    # расчёт хода
    def move_count(self):
        # save old param
        self.old_hp = self.hp
        self.old_mp = self.mp
        self.round += 1

        self.round_param_count()

        self.move_answer = {}
        
        if self.hp > 0:

            # move
            if self.move == '':
                #exec(f'spell_{self.move}(self)')
                pass
            else:
                self.move_message = f'{self.name} бездействует, пропуская ход'
    
            # effects
            for eff in self.effects:
                #exec(f'eff_{eff}(self)')
                if self.effects[eff] > 0:
                    self.effects[eff] = self.effects[eff] - 1
                elif self.effects[eff] < 0:
                    del self.effects[eff]

            return self.move_answer

    # расчёт нового раунда
    def newRound(self):
        if self.hp > 0:
            if 1 < self.round <= 5:
                self.main_mp_regeneration += 1
            elif 6 <= self.round <= 15:
                self.main_mp_regeneration += 2
            elif self.round >= 16:
                self.main_mp_regeneration += 3

            self.round_param_count()
            self.spells_dist()

            # формирование доступных ходов
            self.avaliable_spells = []

            for spell in self.spells:
                if spell.startswith('1') and self.mp >= 3:
                    self.avaliable_spells.append(spell)
                elif spell.startswith('2') and self.mp >= 8:
                    self.avaliable_spells.append(spell)
                elif spell.startswith('3') and self.mp >= 15:
                    self.avaliable_spells.append(spell)
                else:
                    self.avaliable_spells.append(spell)

            try:
                checkStan = self.effects['Стан']
                checkStan = True
            except:
                checkStan = False
                pass

            try:
                checkSleep = self.effects['Кошмарный сон']
                checkSleep = True
            except:
                checkSleep = False
                pass

            check233 = '233' in self.avaliable_spells
            check258 = '258' in self.avaliable_spells

            if not checkStan and not checkSleep:
                self.ability = True
            else:
                self.ability = False
                self.avaliable_spells = []
                if check233:
                    self.avaliable_spells.append('233')
                    self.ability = True
                if check258:
                    self.avaliable_spells.append('258')
                    self.ability = True

            self.move = ''
            self.move_direction = ''

        else:
            self.ability = False

    # распределение спеллов
    def spells_dist(self):
        self.spells = spells_distribution(self.round, self.spells)

    # сброс параметров раунда
    def round_param_reset(self):
        # параметры раунда:
        self.main_mp_regeneration: int = 0
        self.additional_mp_regeneration: int = 0
        self.mp_loss: int = 0
        self.main_damage: int = 0
        self.mp_spend: int = 0
        self.round: int = 0
        self.damage_over_time: int = 0
        self.heal: int = 0
        self.armor: int = 0

    # просчёт параметров раунда
    def round_param_count(self):
        self.mp = self.mp + self.main_mp_regeneration + self.additional_mp_regeneration - self.mp_loss - self.mp_spend
        if self.mp > self.max_mp:
            self.mp = self.max_mp

        damage = self.main_damage + self.damage_over_time - self.armor
        if damage < 0:
            damage = 0
        self.hp = self.hp - damage + self.heal
        if self.hp > self.max_hp:
            self.hp = self.max_hp

        self.round_param_reset()




