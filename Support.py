class Chain:
    # The Acquire Chain Object
    def __init__(self, name: str, quality: int):
        self.name: str = name
        self.stock_amt: int = 25
        self.hotels: list[tuple[int, int]] = []
        self.size: int = len(self.hotels)
        self.quality: int = quality
        self.is_safe: bool = False

    def expand_chain(self, *hotels: tuple[int, int]):
        for hotel in hotels:
            self.hotels.append(hotel)
            self.size = len(self.hotels)
            if len(self.hotels) == 11:
                self.is_safe = True

    def purchase_stock(self, amt: int = 1):
        self.stock_amt -= amt

    def sell_stock(self, amt: int = 1):
        self.stock_amt += amt

    def reset_chain(self):
        self.hotels = []
        self.size = len(self.hotels)

    def merge_chain(self, defunct_chain: 'Chain'):
        self.hotels.extend(defunct_chain.hotels)
        self.size = len(self.hotels)
        if self.size >= 11:
            self.is_safe = True
        
        defunct_chain.reset_chain()

    def is_tile_in_chain(self, tile: tuple[int, int]) -> bool:
        return tile in self.hotels
    
    def calculate_value(self) -> int:
        cost = 200
        if self.size > 41:
            cost = 1_000
        elif self.size > 31:
            cost = 900
        elif self.size > 21:
            cost = 800
        elif self.size > 11:
            cost = 700
        elif self.size > 6:
            cost = 600
        elif self.size > 3:
            cost = 500
        elif self.size > 2:
            cost = 300
        return cost + 100 * self.quality

    def __str__(self):
        return f"Chain(name={self.name}, size={self.size}, quality={self.quality}, is_safe={self.is_safe})"


class Board:
    # The Acquire Board Class

    def __init__(self):
        self.board: list[list[bool]] = [[], [], [], [], [], [], [], [], [], [], [], []]
        for i in range(12):
            for j in range(9):
                self.board[i].append(False)
        self.chains: list[Chain] = []

    def place_tile(self, tile: tuple[int, int]) -> list[Chain] | bool:
        # Assumes that the tile is a legal move. ie doesn't cause mergers between sufficiently sized chains.
        # Returns true if the tile creates a chain .
        assert not self.board[tile[0]][tile[1]], f"Tile attempted to be placed was {tile}"
        self.board[tile[1]][tile[0]] = True

        chains: list[Chain] = self.chains_adjacent_to(tile)
        if chains is not None:
            return chains
        return False

    def tiles_adjacent_to(self, tile: tuple[int, int]):
        adjacent_tiles = []
        if tile[0] - 1 >= 0:
            adjacent_tiles.append((tile[0] - 1, tile[1]))
        if tile[0] + 1 < len(self.board):
            adjacent_tiles.append((tile[0] + 1, tile[1]))
        if tile[1] - 1 >= 0:
            adjacent_tiles.append((tile[0], tile[1] - 1))
        if tile[1] + 1 < len(self.board[0]):
            adjacent_tiles.append((tile[0], tile[1] + 1))
        return adjacent_tiles

    def chains_adjacent_to(self, tile: tuple[int, int]) -> list[Chain] | None:
        chains = []
        for adj_tile in self.tiles_adjacent_to(tile):
            chain = self.chain_from_tile(adj_tile)
            chains.append(chain)
        return chains if chains else None

    def chain_from_tile(self, tile) -> Chain | None:
        for chain in self.chains:
            if tile in chain.hotels:
                return chain
        return None
    
    def create_chain(self, name: str, quality: int, initial_tile: tuple[int, int]):
        new_chain = Chain(name, quality)
        new_chain.expand_chain(initial_tile)
        self.chains.append(new_chain)

    def merge_chains(self, main_chain: Chain, defunct_chain: Chain):
        main_chain.merge_chain(defunct_chain)
        self.chains.remove(defunct_chain)

    def is_tile_in_any_chain(self, tile: tuple[int, int]) -> bool:
        return any(chain.is_tile_in_chain(tile) for chain in self.chains)

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += '\n'
            for tile in row:
                board_str += '* ' if tile else '_ '
        return board_str[1:-1]
