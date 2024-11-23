import string

from Support import Chain


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.money: int = 6_000
        self.stocks: dict[str, int] = {}
        self.tiles: list[tuple[int, int]] = []

    def place_tile(self) -> tuple[int, int]:
        players_tiles = ''
        for tile in self.tiles:
            players_tiles += ', '
            players_tiles += string.ascii_uppercase[tile[0]]
            players_tiles += str(tile[1] + 1)
        print(f"You, {self.name} have the following tiles: ", players_tiles[2:])
        tile_str = input("What tile do you want to place? ")
        if (string.ascii_uppercase.index(tile_str[0]), int(tile_str[1:]) - 1) not in self.tiles:
            print("Not valid input: ", tile_str)
            exit(-1)

        self.tiles.remove((string.ascii_uppercase.index(tile_str[0]), int(tile_str[1:]) - 1))
        return string.ascii_uppercase.index(tile_str[0]), int(tile_str[1:]) - 1

    def choose_merge_order(self, merged_chains: list[Chain]):
        # TODO
        return None

    def dispose_stocks(self, defunct_chain: Chain, acquirer: Chain):
        # TODO
        return None
