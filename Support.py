class Chain:
    # The Acquire Chain Object
    def __init__(self, name: str, quality: int):
        self.name: str = name
        self.stock_amt: int = 25
        self.hotels: list[tuple[int, int]] = []
        self.size: int = len(self.hotels)
        self.quality: int = quality
        self.is_safe: bool = False

    def expand_chain(self, hotel: tuple[int, int]):
        self.hotels.append(hotel)
        self.size = len(self.hotels)
        if len(self.hotels) == 11:
            self.is_safe = True

    def purchase_stock(self, amt: int = 1):
        self.stock_amt -= amt

    def reset_chain(self):
        self.hotels = []
        self.stock_amt = 25
        self.size = len(self.hotels)


class Board:
    # The Acquire Board Class

    def __init__(self):
        self.board: list[list[bool]] = [[True] * 12] * 9
        self.chains: list[Chain] = []

    def place_tile(self, tile: tuple[int, int]) -> list[Chain] | None:
        # Assumes that the tile is a legal move. ie doesn't cause mergers between sufficiently sized chains.
        # Returns true if the tile causes a merger.
        assert not self.board[tile[0]][tile[1]]
        self.board[tile[0]][tile[1]] = True

        if self.does_initiate_merger(tile):
            chains: list[Chain] = self.chains_adjacent_to(tile)
            return chains
        return None

    def does_initiate_merger(self, tile) -> bool:
        chains: list[Chain] = self.chains_adjacent_to(tile)
        return False if chains is None else True

    def chains_adjacent_to(self, tile: tuple[int, int]) -> list[Chain] | None:
        chains = []
        if tile[0] - 1 > 0 and self.board[tile[0] - 1][tile[1]]:
            chains.append(self.chain_from_tile((tile[0] - 1, tile[1])))
        if tile[0] + 1 < len(self.board) and self.board[tile[0] + 1][tile[1]]:
            chains.append(self.chain_from_tile((tile[0] + 1, tile[1])))
        if tile[1] - 1 > 0 and self.board[tile[0]][tile[1] - 1]:
            chains.append(self.chain_from_tile((tile[0], tile[1] - 1)))
        if tile[1] + 1 < len(self.board[0]) and self.board[tile[0]][tile[1] + 1]:
            chains.append(self.chain_from_tile((tile[0], tile[1] + 1)))

        return chains if chains != [] else None

    def chain_from_tile(self, tile) -> Chain | None:
        for chain in self.chains:
            if tile in chain.hotels:
                return tile
        return None
