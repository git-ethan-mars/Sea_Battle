import ships
import random

block_size = 45
left_margin = 90
top_margin = 72


class Player:
    ships = ships.Ships()
    dead_ships = 0

    def __init__(self):
        self.empty_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.enemy_left = left_margin + block_size * 15
        self.enemy_top = top_margin

    def shoot(self, position):
        x, y = ((position[0] - self.enemy_left) // block_size + 1,
                (position[1] - self.enemy_top) // block_size + 1)
        if ships.Ships.is_on_field((x, y)) and (x, y) in self.empty_cells:
            self.empty_cells.remove((x, y))
            if (x, y) in [j for i in Computer.ships.ships_set for j in i]:
                Computer.dead_ships += 1
                return x, y, self.enemy_left, self.enemy_top, True
            else:
                return x, y, self.enemy_left, self.enemy_top, False


class Computer:
    ships = ships.Ships()
    dead_ships = 0

    def __init__(self):
        self.empty_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.enemy_left = left_margin
        self.enemy_top = top_margin

    def shoot(self):
        x, y = random.choice(self.empty_cells)
        self.empty_cells.remove((x, y))
        if (x, y) in [j for i in Player.ships.ships_set for j in i]:
            Player.dead_ships += 1
            return x, y, self.enemy_left, self.enemy_top, True
        else:
            return x, y, self.enemy_left, self.enemy_top, False
