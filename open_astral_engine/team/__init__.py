class AstralTeam(list):
    """Astral Team class"""

    def __init__(self, color):
        super().__init__()
        self.color = color

    def check_all_dead(self):
        return len(self) == list(filter(lambda player: player.hp <= 0, self))

    def get_players_names(self) -> str:
        return ', '.join(player.name for player in self)


class AstralTeams(dict):
    """An iterable dictionary of teams."""

    def __init__(self):
        super().__init__()
        self.__pos: int = 0

    def __iter__(self):
        return self

    def __next__(self) -> AstralTeam:
        if self.__pos <= len(self.keys())-1:
            team = self[list(self.keys())[self.__pos]]
            self.__pos += 1
            return team
        else:
            self.__pos: int = 0
            raise StopIteration

    def get_alive_teams(self) -> list:
        try:
            return list(filter(lambda team: not team.check_all_dead(), list(self)))
        except IndexError:
            return []