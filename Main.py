from Game import Game
from Player import Player

names = ["Nathan", "Alex"]
players: list[Player] = []
for name in names:
    players.append(Player(name))

g1 = Game(*players)
g1.start()