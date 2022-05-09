import open_astral_engine

game = open_astral_engine.AstralGame(id=1)

game.append_player("кек")
game.append_player("лол")

game.start()
game.step()
kek = game.get_player_by_name("кек")
kek.checker('11')
kek.set_move('11')
print(game.game_message)
game.step()
print(game.game_message)
