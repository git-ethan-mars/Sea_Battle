import random

from shipsSet import ShipsSet, is_on_field
from settings import left_margin, top_margin, block_size


class Player:

    def __init__(self):
        self.data_ships = ShipsSet()
        self.dead_ships = 0
        self.free_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.last_hurt_ship = []
        self.dead_ships_length = {}

    def is_ship_destroyed(self, computer) -> bool:
        for ship in computer.data_ships.ships:
            if set(ship) <= set(self.last_hurt_ship):
                return True
        return False

    def is_ships_placed(self, file_data):
        return file_data == self.data_ships.ships_placed

    def shoot(self, computer, position):
        first_ship = None
        last_ship = None
        ship = None
        x, y = position
        is_hurt = (x, y) in [j for i in computer.data_ships.ships for j in
                             i]
        if is_on_field((x, y)) and (x, y) in self.free_cells:
            self.free_cells.remove((x, y))
            if is_hurt:
                self.last_hurt_ship.append((x, y))
            if self.is_ship_destroyed(computer):
                ship_candidate = []
                for ship in computer.data_ships.ships:
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
                computer.dead_ships_length[len(ship)] += 1
            if is_hurt:
                return x, y, self, True, first_ship, last_ship
            else:
                return x, y, self, False, first_ship, last_ship

    @staticmethod
    def get_cell(position):
        return (position[0] - left_margin) // block_size + 1, (
                position[1] - top_margin) // block_size + 1


class Computer:

    def __init__(self):
        self.data_ships = ShipsSet()
        self.dead_ships = 0
        self.free_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.possible_targets = []
        self.last_hurt_ship = []
        self.dead_ships_length = {}

    def is_destroyed(self, player: Player) -> bool:
        for ship in player.data_ships.ships:
            if set(ship) <= set(self.last_hurt_ship):
                return True
        return False

    def shoot(self, player, computer, is_smart):
        is_horizontal = True
        is_vertical = True
        first_ship = None
        last_ship = None
        ship = None
        if not is_smart:
            x, y = random.choice(self.free_cells)
            self.free_cells.remove((x, y))
            if (x, y) in [j for i in player.data_ships.ships for j in i]:
                self.last_hurt_ship.append((x, y))
            if self.is_destroyed(computer):
                ship_candidate = []
                for ship in player.data_ships.ships:
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
                player.dead_ships_length[len(ship)] += 1
        else:
            if self.possible_targets:
                x, y = random.choice(self.possible_targets)
                self.possible_targets.remove((x, y))
            else:
                x, y = random.choice(self.free_cells)
            self.free_cells.remove((x, y))
            if (x, y) in [j for i in player.data_ships.ships for j in i]:
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
                if is_on_field((x - 1, y)) and (
                        x - 1, y) in self.free_cells and is_horizontal:
                    self.possible_targets.append((x - 1, y))
                if is_on_field((x + 1, y)) and (
                        x + 1, y) in self.free_cells and is_horizontal:
                    self.possible_targets.append((x + 1, y))
                if is_on_field((x, y - 1)) and (
                        x, y - 1) in self.free_cells and is_vertical:
                    self.possible_targets.append((x, y - 1))
                if is_on_field((x, y + 1)) and (
                        x, y + 1) in self.free_cells and is_vertical:
                    self.possible_targets.append((x, y + 1))
            if self.is_destroyed(player):
                self.last_hurt_ship.sort()
                first_ship = self.last_hurt_ship[0]
                last_ship = self.last_hurt_ship[-1]
                player.dead_ships_length[len(self.last_hurt_ship)] += 1
                for ship in self.possible_targets:
                    self.free_cells.remove(ship)
                self.last_hurt_ship = []
                self.possible_targets = []
        return x, y, self, (x, y) in \
            [j for i in player.data_ships.ships for j in i], \
            first_ship, last_ship

    @staticmethod
    def get_cell(position):
        return (position[0] - (
                left_margin + block_size * 15)) // block_size + 1, (
                       position[1] - top_margin) // block_size + 1
