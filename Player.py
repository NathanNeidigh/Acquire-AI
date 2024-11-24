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

    def choose_merge_order(self, merged_chains: list[Chain]) -> list[Chain]:
        print(f"{self.name}, choose the order of merging the chains:")
        for i, chain in enumerate(merged_chains):
            print(f"{i + 1}: {chain.name}")
        order = input("Enter the order of merging (e.g., 1,2,3): ")
        order_indices = [int(x) - 1 for x in order.split(',')]
        return [merged_chains[i] for i in order_indices]

    def dispose_stocks(self, defunct_chain: Chain, acquirer: Chain):
        print(f"{self.name}, you need to dispose of stocks from the defunct chain {defunct_chain.name}.")
        while self.stocks[defunct_chain.name] > 0:
            print(f"You have {self.stocks[defunct_chain.name]} stocks in {defunct_chain.name}.")
            action = input("Do you want to (s)ell, (t)rade, or (k)eep? ")
            if action == 's':
                self.sell_stock(defunct_chain.name, 1)
                self.money += defunct_chain.calculate_value()
            elif action == 't':
                self.trade_stock(defunct_chain.name, acquirer.name, 2)
            elif action == 'k':
                break

    def buy_stock(self, chain: Chain, amount: int):
        cost = chain.calculate_value() * amount
        if self.money >= cost and chain.stock_amt >= amount:
            self.money -= cost
            chain.purchase_stock(amount)
            if chain.name in self.stocks:
                self.stocks[chain.name] += amount
            else:
                self.stocks[chain.name] = amount
        else:
            print(f"Cannot buy {amount} stocks of {chain.name}.")

    def sell_stock(self, chain_name: str, amount: int):
        if self.stocks.get(chain_name, 0) >= amount:
            self.stocks[chain_name] -= amount
            if self.stocks[chain_name] == 0:
                del self.stocks[chain_name]
        else:
            print(f"Cannot sell {amount} stocks of {chain_name}.")

    def trade_stock(self, defunct_chain_name: str, acquirer_chain_name: str, amount: int):
        if self.stocks.get(defunct_chain_name, 0) >= amount:
            self.stocks[defunct_chain_name] -= amount
            if self.stocks[defunct_chain_name] == 0:
                del self.stocks[defunct_chain_name]
            if acquirer_chain_name in self.stocks:
                self.stocks[acquirer_chain_name] += amount // 2
            else:
                self.stocks[acquirer_chain_name] = amount // 2
        else:
            print(f"Cannot trade {amount} stocks of {defunct_chain_name}.")

    def __str__(self):
        return f"Player(name={self.name}, money={self.money}, stocks={self.stocks}, tiles={self.tiles})"
