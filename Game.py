from Support import Board, Chain
from Player import Player
import random


class Game:
    def __init__(self, *players):
        self.board = Board()
        self.players: list[Player] = list(players)
        self.tiles: list[tuple[int, int]] = []
        for i in range(9):
            for j in range(12):
                self.tiles.append((i, j))

        for player in players:
            for _ in range(6):
                self.draw(player)

        self.chains: list[Chain] = [Chain("Tower", 1), Chain("Luxor", 1),
                                    Chain("American", 2), Chain("Worldwide", 2),
                                    Chain("Festival", 2), Chain("Imperial", 3),
                                    Chain("Continental", 3)]

    def start(self):
        while True:
            for player in self.players:
                self.turn(player)
                if not self.any_valid_moves():
                    results = self.end_game()
                    return results

    def any_valid_moves(self) -> bool:
        amt = 0
        for player in self.players:
            amt += len(player.tiles)

    def draw(self, player: Player):
        # Assumes only valid moves in game pile
        tile = self.tiles[random.randint(0, len(self.tiles))]
        player.tiles.append(tile)
        self.tiles.remove(tile)

    def turn(self, player):
        tile = player.place_tile()
        chains = self.board.place_tile(tile)
        if chains is not None:
            #Merger
            self.merge(chains, player)

    def merge(self, chains: list[Chain], merger_maker: Player):
        #TODO
        sorted_chains = reversed(sorted(chains, key=lambda x: x.size)) # large to small chain size
        for i, chain in enumerate(sorted_chains):
            if i == 0:
                continue
            if chain.size == sorted_chains[i-1].size:
                result = merger_maker.choose_defunct_chain(sorted_chains[i-1], chain)


    def end_game(self):
        #TODO
        return None
