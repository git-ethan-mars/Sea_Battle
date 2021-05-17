import random


class ShipsSet:

    @staticmethod
    def is_on_field(cell: tuple) -> bool:
        return 1 <= cell[0] <= 10 and 1 <= cell[1] <= 10

    def __init__(self):
        self.available_cells = [(x, y) for x in range(1, 11) for y in
                                range(1, 11)]
        self.ships = []

    def choose_started_cell(self) -> ([int, int], bool, int):
        started_cell = random.choice(self.available_cells)
        is_vertical = bool(random.getrandbits(1))
        direction = random.choice([-1, 1])
        return started_cell, is_vertical, direction

    def create_ship(self, length):
        ship_coordinates = []
        started_cell, is_vertical, direction = self.choose_started_cell()
        x, y = started_cell
        for i in range(length):
            if not is_vertical:
                if ShipsSet.is_on_field((x + i * direction, y)) and (
                        x + i * direction, y) in self.available_cells:
                    ship_coordinates.append((x + i * direction, y))
                else:
                    return False
            else:
                if ShipsSet.is_on_field((x, y + i * direction)) and (
                        x, y + i * direction) in self.available_cells:
                    ship_coordinates.append((x, y + i * direction))
                else:
                    return False
        self.ships.append(ship_coordinates)
        self.refresh_available_cells(ship_coordinates)
        return ship_coordinates

    def refresh_available_cells(self, ship_coordinates: (int, int)) -> None:
        for x, y in ship_coordinates:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if ShipsSet.is_on_field((x + i, y + j)) and (
                            x + i, y + j) in self.available_cells:
                        self.available_cells.remove((x + i, y + j))
