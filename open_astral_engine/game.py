from .player import AstralPlayer
from .bot import AstralBot
from .base_exceptions import OddNumberOfPlayers, DefunctPlayer, ExistingPlayer
from copy import copy
from .spells import Level0Skip
from .team import *

team_colors = ["Красная", "Оранжевая", "Желтая", "Зеленая", "Синяя", "Фиолетовая"]

distribute_rules = [
    "",
    "",
    "1Aх1D",
    "1Dх1A",
    "1Aх1D",
    "1Dх1A",
    "1Dх2A",
    "1Aх1D",
    "1Aх2D",
    "1Dх1A",
    "1Dх2A",
    "1Aх3",
    "1Aх2D",
    "1Dх2A",
    "1Aх2D",
    "2Dх2A",
    "1Dх3",
    "1Aх2D",
    "2Dх2A",
    "1Dх2D",
    "2Dх2A",
    "2Aх3",
    "2Aх2D",
    "1Aх2A",
    "2Aх2D",
    "2Dх2A",
    "2Dх3",
    "2Aх2D",
    "2Dх3",
    "2Dх2A",
    "3х3",
]


class AstralGame:
    """Astral Game class"""

    def __init__(self, id: int = 0):
        self.id = id
        self.players: list = []
        self.teams: AstralTeams[AstralTeam] = AstralTeams()
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
        for player in self.players:
            if player.name == player_name:
                return player
        raise DefunctPlayer

    def check_all_moved(self):
        return len(self.players) == len(
            list(filter(lambda player: player.moved, self.players))
        )

    def distribute_spells(self) -> None:
        for player in self.players:
            player.spells.distribute_spells(distribute_rules[self.round])

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
                self.teams[team] = AstralTeam(team)
                count = 0
                for player in self.players:
                    if count == half:
                        team = next(teams_iterator)
                        self.teams[team] = AstralTeam(team)

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
        if self.stop:
            raise StopIteration
        elif self.round == 0:
            self.game_message = f"""Начинается игра Астрал
В смертельной битве магов сразятся: {' // VS // '.join(team.get_players_names() for team in self.teams)}"""

            self.game_message += (
                "\n\nВеликая Белка жаждет кровавую жертву! Начинаем Раунд №1"
            )

            for player in self.players:
                player.new_round()
                player.effects.act()
                player.before_move_count()

            self.round += 1
            self.rounds[self.round] = copy(self)

            return self
        else:
            self.game_message = f"И-так, в {self.round}-ом раунде\n\n"

            for player in self.players:
                if player.hp > 0:
                    if player.move is None:
                        player.move = Level0Skip(self, player)

            self.players.sort(key=lambda player: player.move.__priority__)

            for player in self.players:
                if player.hp > 0:
                    if not player.move_cancelation:
                        self.game_message += player.move.move() + "\n"
                    else:
                        self.game_message += f"Попытка применения кастером {player.name} заклинания {player.move.__sname__} сорвана\n"

            self.game_message += "\n"

            alive_teams = self.teams.get_alive_teams()

            match len(alive_teams):
                case 1:
                    team: AstralTeam = alive_teams[0]
                    self.stop = True
                    self.game_message += f"Победа достаётся {team.color} команде\n{'Участники: ' if len(team) > 1 else 'Участник:'}{', '.join(player.name for player in team)}\n"
                case 0:
                    self.stop = True
                    self.game_message += "Ничья\n"
                case _:
                    for team in alive_teams:
                        for player in team:
                            if player.hp > 0:
                                player.after_move_count()

            if not self.stop:
                teams_to_message = alive_teams
            else:
                teams_to_message = self.teams

            for team in teams_to_message:
                self.game_message += f"{team.color} команда:\n"
                for player in team:
                    self.game_message += f"{player.name} HP: {player.hp} MP: {player.mp}. {player.effects.effects_names_sorted_by_fluttering()}\n"
                self.game_message += "\n"

            self.round += 1
            self.rounds[self.round] = copy(self)

            if not self.stop and self.round < 30:
                self.game_message += f"Начало раунда №{self.round}"
            else:
                self.game_message += f"Ничья.\nКонец игры."
                self.stop = True

            for player in self.players:
                if player.hp > 0:
                    player.effects.remove_expired()
                    player.new_round()
                    player.effects.act()
                    player.before_move_count()

            # Uncomment when spell dictionaries are ready
            # self.distribute_spells()

            return self
