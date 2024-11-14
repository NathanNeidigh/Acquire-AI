class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.money: int = 6_000
        self.stocks: dict[str, int] = {}
        self.tiles: list[tuple[int, int]] = []

    def place_tile(self) -> tuple[int, int]:
        #TODO
        return None
