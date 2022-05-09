from .player import AstralPlayer
from .bot import AstralBot
from .base_exceptions import OddNumberOfPlayers, DefunctPlayer, ExistingPlayer
from copy import copy
from .spells import Level0Skip

team_colors = ["red", "orange", "yellow", "green", "blue", "violet"]


class AstralGame:
    """Astral Game class"""

    def __init__(self, id: int = 0):
        self.id = id
        self.players: list = []
        self.teams: dict = {}
        self.stop = False

        self.arena: str = ""
        self.deathmatch: bool = False

        self.round: int = 0
        self.rounds: dict = {}

        self.game_message: str = ""

    def append_player(self, name: str):
        player = list(filter(lambda p: p.name == name, self.players))
        if not player:
            self.players.append(AstralPlayer(self, name))
        else:
            raise ExistingPlayer

    def append_bot(self, name: str = "AstralBot"):
        player = list(filter(lambda p: p.name == name, self.players))
        if not player:
            self.players.append(AstralBot(self, name))
        else:
            raise ExistingPlayer

    def kick(self, player_name: str):
        player = list(filter(lambda p: p.name == player_name, self.players))
        if not player:
            raise DefunctPlayer
        else:
            self.players.remove(player)

    def get_player_by_name(self, player_name: str):
        player = list(filter(lambda p: p.name == player_name, self.players))
        if not player:
            raise DefunctPlayer
        else:
            return player

    def check_all_moved(self):
        return len(self.players) == len(
            list(filter(lambda player: player.moved, self.players))
        )

    def start(self):
        self.__iter__()

    def step(self):
        self.__next__()

    def __iter__(self):
        if len(self.players) % 2 != 0:
            raise OddNumberOfPlayers
        else:
            if not self.deathmatch:
                half = len(self.players) // 2
                teams_iterator = iter(team_colors)
                team = next(teams_iterator)
                self.teams[team] = []
                count = 0
                for player in self.players:
                    if count == half:
                        team = next(teams_iterator)
                        self.teams[team] = []

                    self.teams[team].append(player)
                    player.team = team
                    count += 1
            else:
                teams_iterator = iter(team_colors)
                team = next(teams_iterator)
                for player in self.players:
                    player.team = team
                    team = next(teams_iterator)
            return self

    def __next__(self):
        if self.round >= 30 or self.stop:
            self.stop = True
            raise StopIteration
        elif self.round == 0:
            self.game_message = f"""Начинается игра Астрал
В смертельной битве магов сразятся: {' // VS // '.join(player.name for player in self.players)}"""

            self.game_message += (
                "\n\nВеликая Белка жаждет кровавую жертву! Начинаем Раунд №1"
            )

            for player in self.players:
                player.new_round()
                player.effects.act()
                player.premove()

            self.round += 1
            self.rounds[self.round] = copy(self)

            return self
        else:
            self.game_message = f"И-так, в {self.round}-ом раунде\n\n"

            for player in self.players:
                if player.move is None:
                    player.move = Level0Skip(self, player)

            self.players.sort(key=lambda player: player.move.__priority__)

            for player in self.players:
                self.game_message += player.move.move() + "\n"

            self.game_message += "\n"

            for player in self.players:
                self.game_message += f"{player.name} HP: {player.hp} MP: {player.mp}\n"

            self.game_message += "\n"

            self.round += 1
            self.rounds[self.round] = copy(self)

            self.game_message += f"Начало раунда №{self.round}"

            for player in self.players:
                player.new_round()
                player.effects.act()
                player.premove()

            return self
