import random
import os
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
block_size = 45
left_margin = 90
top_margin = 72


class Ships:
    head_ship_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'images\\triangle.png'))
    head_ship_image.set_colorkey(WHITE)

    @staticmethod
    def get_angle(is_vertical, direction):
        angle = 0
        if is_vertical and direction == -1:
            angle = 90
        elif not is_vertical and direction == -1:
            angle = 180
        elif is_vertical and direction == 1:
            angle = 270
        return angle

    @staticmethod
    def is_on_field(cell):
        return 1 <= cell[0] <= 10 and 1 <= cell[1] <= 10

    def __init__(self):
        self.available_cells = [(x, y) for x in range(1, 11) for y in range(1, 11)]
        self.ships_set = []

    def choose_started_cell(self):
        started_cell = random.choice(self.available_cells)
        is_vertical = bool(random.getrandbits(1))
        direction = random.choice([-1, 1])
        return started_cell, is_vertical, direction

    def create_ship(self, length):
        ship_coordinates = []
        started_cell, is_vertical, direction = self.choose_started_cell()
        x, y = started_cell
        angle = Ships.get_angle(is_vertical, direction)
        rotated_image = pygame.transform.rotate(Ships.head_ship_image, angle)
        for i in range(length):
            if not is_vertical:
                if Ships.is_on_field((x + i * direction, y)) and (x + i * direction, y) in self.available_cells:
                    ship_coordinates.append((x + i * direction, y))
                else:
                    return [False, None]
            else:
                if Ships.is_on_field((x, y + i * direction)) and (x, y + i * direction) in self.available_cells:
                    ship_coordinates.append((x, y + i * direction))
                else:
                    return [False, None]
        self.ships_set.append(ship_coordinates)
        self.refresh_available_cells(ship_coordinates)
        return [ship_coordinates, rotated_image]

    def draw_ship(self, length, screen):
        ship_coordinates, rotated_image = self.create_ship(length)
        while not ship_coordinates:
            ship_coordinates, rotated_image = self.create_ship(length)
        screen.blit(rotated_image, (left_margin + (ship_coordinates[0][0] - 1) * block_size,
                                    top_margin + (ship_coordinates[0][1] - 1) * block_size))
        for x, y in ship_coordinates[1::]:
            pygame.draw.rect(screen, RED, pygame.Rect(left_margin + (x - 1) * block_size,
                                                      top_margin + (y - 1) * block_size,
                                                      block_size, block_size))

    def refresh_available_cells(self, ship_coordinates):
        for x, y in ship_coordinates:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if Ships.is_on_field((x + i, y + j)) and (x + i, y + j) in self.available_cells:
                        self.available_cells.remove((x + i, y + j))
