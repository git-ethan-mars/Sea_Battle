import random

from shipsSet import ShipsSet


class Player:

    def __init__(self, game):
        self.data_ships = ShipsSet()
        self.dead_ships = 0
        self.free_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.enemy_left = game.left_margin + game.block_size * 15
        self.enemy_top = game.top_margin
        self.last_hurt_ship = []
        self.dead_ships_length = {}

    def is_destroyed(self, computer) -> bool:
        for ship in computer.data_ships.ships:
            if set(ship) <= set(self.last_hurt_ship):
                return True
        return False

    def shoot(self, game, position) -> (
            int, int, int, int, bool, tuple or None, tuple or None):
        first_ship = None
        last_ship = None
        x, y = ((position[0] - self.enemy_left) // game.block_size + 1,
                (position[1] - self.enemy_top) // game.block_size + 1)
        is_hurt = (x, y) in [j for i in game.computer.data_ships.ships for j in
                             i]
        if ShipsSet.is_on_field((x, y)) and (x, y) in self.free_cells:
            self.free_cells.remove((x, y))
            if is_hurt:
                self.last_hurt_ship.append((x, y))
            if self.is_destroyed(game.computer):
                ship_candidate = []
                for ship in game.computer.data_ships.ships:
                    if set(ship) <= set(self.last_hurt_ship):
                        ship_candidate = ship
                        break
                temp = []
                for cell in ship_candidate:
                    if cell in self.last_hurt_ship:
                        temp.append(cell)
                        self.last_hurt_ship.remove(cell)
                temp.sort()
                first_ship = temp[0]
                last_ship = temp[-1]
                game.computer.dead_ships_length[len(ship)] += 1
            if is_hurt:
                return x, y, self.enemy_left, \
                       self.enemy_top, True, first_ship, last_ship
            else:
                return x, y, self.enemy_left, \
                       self.enemy_top, False, first_ship, last_ship


class Computer:

    def __init__(self, game):
        self.data_ships = ShipsSet()
        self.dead_ships = 0
        self.free_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.enemy_left = game.left_margin
        self.enemy_top = game.top_margin
        self.possible_targets = []
        self.last_hurt_ship = []
        self.dead_ships_length = {}

    def is_destroyed(self, player: Player) -> bool:
        for ship in player.data_ships.ships:
            if set(ship) <= set(self.last_hurt_ship):
                return True
        return False

    def shoot(self, game) -> (
            int, int, int, int, bool, tuple or None, tuple or None):
        is_horizontal = True
        is_vertical = True
        first_ship = None
        last_ship = None
        if not game.is_smart:
            x, y = random.choice(self.free_cells)
            self.free_cells.remove((x, y))
            if (x, y) in [j for i in game.player.data_ships.ships for j in i]:
                self.last_hurt_ship.append((x, y))
            if self.is_destroyed(game.computer):
                ship_candidate = []
                for ship in game.computer.data_ships.ships:
                    if set(ship) <= set(self.last_hurt_ship):
                        ship_candidate = ship
                        break
                temp = []
                for cell in ship_candidate:
                    if cell in self.last_hurt_ship:
                        temp.append(cell)
                        self.last_hurt_ship.remove(cell)
                temp.sort()
                first_ship = temp[0]
                last_ship = temp[-1]
                game.player.dead_ships_length[len(ship)] += 1
        else:
            if self.possible_targets:
                x, y = random.choice(self.possible_targets)
                self.possible_targets.remove((x, y))
            else:
                x, y = random.choice(self.free_cells)
            self.free_cells.remove((x, y))
            if (x, y) in [j for i in game.player.data_ships.ships for j in i]:
                self.last_hurt_ship.append((x, y))
                if len(self.last_hurt_ship) >= 2:
                    if self.last_hurt_ship[0][0] == self.last_hurt_ship[1][0]:
                        is_horizontal = False
                        for i in range(len(self.possible_targets) - 1, -1, -1):
                            if self.possible_targets[i][0] != \
                                    self.last_hurt_ship[0][
                                        0]:
                                self.free_cells.remove(
                                    self.possible_targets[i])
                                del self.possible_targets[i]
                    if self.last_hurt_ship[0][1] == self.last_hurt_ship[1][1]:
                        is_vertical = False
                        for i in range(len(self.possible_targets) - 1, -1, -1):
                            if self.possible_targets[i][1] != \
                                    self.last_hurt_ship[0][1]:
                                self.free_cells.remove(
                                    self.possible_targets[i])
                                del self.possible_targets[i]
                if ShipsSet.is_on_field((x - 1, y)) and (
                        x - 1, y) in self.free_cells and is_horizontal:
                    self.possible_targets.append((x - 1, y))
                if ShipsSet.is_on_field((x + 1, y)) and (
                        x + 1, y) in self.free_cells and is_horizontal:
                    self.possible_targets.append((x + 1, y))
                if ShipsSet.is_on_field((x, y - 1)) and (
                        x, y - 1) in self.free_cells and is_vertical:
                    self.possible_targets.append((x, y - 1))
                if ShipsSet.is_on_field((x, y + 1)) and (
                        x, y + 1) in self.free_cells and is_vertical:
                    self.possible_targets.append((x, y + 1))
            if self.is_destroyed(game.player):
                self.last_hurt_ship.sort()
                first_ship = self.last_hurt_ship[0]
                last_ship = self.last_hurt_ship[-1]
                for ship in self.possible_targets:
                    self.free_cells.remove(ship)
                self.last_hurt_ship = []
                self.possible_targets = []
        return x, y, self.enemy_left, self.enemy_top, (x, y) in \
            [j for i in game.player.data_ships.ships for j in i], \
            first_ship, last_ship
