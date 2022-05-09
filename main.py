import open_astral_engine

game = open_astral_engine.AstralGame()

game.append_player("кек")
game.append_player("лол")

for game_round in game:
    print(game_round.game_message)
