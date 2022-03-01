mxp = 30 # макс хп
mmp = 40 # макс мп
mag = -1 # макс агр

class Game(object):
    """Astral Game object"""

    def __init__(self, uid):
        self.uuid: str = uid

        # ограничение хп, мп и агра
        self.max_xp: int = mxp
        self.max_mp: int = mmp
        self.max_ag: int = mag

        # игровые параметры
        self.arena: int = 0
        self.deathmatch: bool = False

        # игроки
        self.playerslist: list = []
        self.teams: list = []

        # ход
        self.game_message: str = ''

    def newRound(self):
        for player in self.playerslist:
            player.newRound()