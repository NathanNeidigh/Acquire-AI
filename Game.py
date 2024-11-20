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
        self.board.display_board()
        tile = player.place_tile()
        chains = self.board.place_tile(tile)
        if None not in chains:
            #Merger
            print(chains)
            self.merge(chains, player)
        self.board.display_board()

    def merge(self, chains: list[Chain], merger_maker: Player):
        sorted_chains = reversed(sorted(chains, key=lambda x: x.size)) # large to small chain size
        merge_order: list[Chain] = []
        groups = []
        for chain in sorted_chains:
            if not groups or groups[-1][0].size != chain.size:
                groups.append([chain])
            else:
                groups[-1].append(chain)

        for chain_group in groups:
            merge_order.append(merger_maker.choose_merge_order(chain_group))

        acquirer = merge_order[0]
        for defunct_chain in merge_order[1:]:
            self.award_bonuses(defunct_chain)

            index = self.players.index(merger_maker)
            for player in self.players[index:] + self.players[:index]:
                player.dispose_stocks(defunct_chain, acquirer)

            acquirer.expand_chain(*defunct_chain.hotels)
            defunct_chain.reset_chain()

    def award_bonuses(self, defunct_chain: Chain):
        #TODO
        return None

    def end_game(self):
        #TODO
        return None
