import pygame
from players import Player, Computer
from settings import *


class Game:
    def __init__(self, is_smart=True):
        self.is_place = False
        self.is_smart = is_smart
        self.screen = pygame.display.set_mode((1920, 1080))
        self.font = pygame.font.SysFont('notosans',
                                        int(block_size // 1.5))
        self.is_menu = True
        self.is_options = False
        self.is_finished = False
        self.player = Player()
        self.computer = Computer()
        self.ships_amount = 0
        self.rect_to_place = []
        self.rect_taken = None
        self.wrong_ship_placed = False
        self.last_message = None

    def draw_new_game(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_player_statistic(self.font)

    def draw_fast_game(self) -> None:
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_ships()
        self.draw_fleet_statistic()

    def draw_ships(self):
        ships_data = load_file()
        for length in sorted(ships_data.keys(), reverse=True):
            for _ in range(ships_data[length]):
                self.ships_amount += length
                computer_ship_is_created = self.computer.data_ships.create_ship(
                    length)
                while not computer_ship_is_created:
                    computer_ship_is_created = self.computer.data_ships.create_ship(
                        length)
                self.draw_player_ship(length)
        for ship in self.computer.data_ships.ships:
            self.computer.dead_ships_length[len(ship)] = 0
        for ship in self.player.data_ships.ships:
            self.player.dead_ships_length[len(ship)] = 0

    def draw_centre_text(self, text: str, font_size: int,
                         color: (int, int, int), offset_x: int = 0,
                         offset_y: int = 0,
                         ):
        font = pygame.font.SysFont('notosans', int(font_size))
        text = font.render(text, True, color)
        self.screen.blit(text, (
            (self.screen.get_width() - text.get_width()) // 2 + offset_x,
            (self.screen.get_height() - text.get_height()) // 2 + offset_y))
        return (self.screen.get_width() - text.get_width()) // 2 + offset_x, (
                self.screen.get_height() - text.get_height()) // 2 + offset_y, text.get_width(), text.get_height()

    def draw_centre_button(self, text: str, color: tuple, offset_x: int = 0,
                           offset_y: int = 0) -> pygame.Rect:
        font_size = block_size * 3
        font = pygame.font.SysFont('notosans', font_size)
        button_text = font.render(text, True, BLACK)
        button = pygame.Rect(
            (self.screen.get_width() - button_text.get_width()) // 2 +
            offset_x,
            (self.screen.get_height() - button_text.get_height()) // 2 +
            offset_y,
            button_text.get_width(), button_text.get_height())
        pygame.draw.rect(self.screen, color, button)
        self.screen.blit(button_text, (
            (self.screen.get_width() - button_text.get_width()) // 2
            + offset_x,
            (self.screen.get_height() - button_text.get_height()) // 2 +
            offset_y))
        return button

    def draw_menu(self) -> (pygame.Rect, pygame.Rect, pygame.Rect):
        self.screen.fill(WHITE)
        new_game_button = self.draw_centre_button("Новая игра", BLUE,
                                                  offset_y=-250)
        fast_game_button = self.draw_centre_button("Быстрая игра", GREEN,
                                                   offset_y=-80)
        options_button = self.draw_centre_button("Опции", BLUE, offset_y=80)
        exit_button = self.draw_centre_button("Выход из игры", RED,
                                              offset_y=250)
        return new_game_button, fast_game_button, options_button, exit_button

    def draw_options(self) -> (pygame.Rect, pygame.Rect):
        self.screen.fill(WHITE)
        self.draw_centre_text("Опции", block_size * 3, BLACK,
                              offset_y=-250)
        if self.is_smart:
            computer_mode_button = self.draw_centre_button("Умный противник",
                                                           GREEN,
                                                           offset_y=-75)
        else:
            computer_mode_button = self.draw_centre_button("Глупый противник",
                                                           RED,
                                                           offset_y=-75)
        menu_button = self.draw_centre_button("Назад в меню", RED,
                                              offset_y=100)
        return computer_mode_button, menu_button

    def draw_back_to_menu_button(self) -> pygame.Rect:
        font_size = block_size // 2
        font = pygame.font.SysFont('notosans', font_size)
        button = pygame.Rect(1920 - int(block_size * 2.8), 0,
                             int(block_size * 2.8), block_size)
        pygame.draw.rect(self.screen, (255, 0, 0), button)
        back_text = font.render("Назад в меню", True, BLACK)
        self.screen.blit(back_text,
                         (1920 - int(block_size * 2.6),
                          block_size // 3))
        return button

    def draw_winner(self, winner: str) -> None:
        font_size = block_size * 4
        font = pygame.font.SysFont('notosans', font_size)
        text = font.render(f"Победил {winner}!", True, RED)
        self.screen.blit(text, (0, block_size * 13))

    def draw_grid(self) -> None:
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        for i in range(11):
            pygame.draw.line(self.screen, BLACK,
                             (left_margin,
                              top_margin + i * block_size),
                             (left_margin + 10 * block_size,
                              top_margin + i * block_size), 1)
            pygame.draw.line(self.screen, BLACK,
                             (left_margin + i * block_size,
                              top_margin),
                             (left_margin + i * block_size,
                              top_margin + 10 * block_size), 1)
            pygame.draw.line(self.screen, BLACK,
                             (left_margin + 15 * block_size,
                              top_margin +
                              i * block_size),
                             (left_margin + 25 * block_size,
                              top_margin + i * block_size), 1)
            pygame.draw.line(self.screen, BLACK,
                             (left_margin + (i + 15) * block_size,
                              top_margin),
                             (left_margin + (i + 15) * block_size,
                              top_margin + 10 * block_size), 1)
            if i < 10:
                num_ver = self.font.render(str(i + 1), True, BLACK)
                letters_hor = self.font.render(letters[i], True, BLACK)
                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_width = letters_hor.get_width()
                self.screen.blit(num_ver, (
                    left_margin - (
                            block_size // 2 + num_ver_width // 2),
                    top_margin + i * block_size + (
                            block_size // 2 - num_ver_height // 2)))
                self.screen.blit(letters_hor,
                                 (left_margin + i * block_size + (
                                         block_size //
                                         2 - letters_hor_width // 2),
                                  top_margin - block_size // 2))
                self.screen.blit(num_ver, (
                    left_margin - (
                            block_size // 2 + num_ver_width // 2) + 15 *
                    block_size,
                    top_margin + i * block_size + (
                            block_size // 2 - num_ver_height // 2)))
                self.screen.blit(letters_hor,
                                 (left_margin + i * block_size + (
                                         block_size // 2 -
                                         letters_hor_width // 2) +
                                  15 * block_size,
                                  top_margin - block_size // 2))

    def draw_player_ship(self, length: int) -> None:
        if self.player.data_ships.ships_copy is None:
            ship_coordinates = self.player.data_ships.create_ship(length)
            while not ship_coordinates:
                ship_coordinates = self.player.data_ships.create_ship(length)
            for x, y in ship_coordinates:
                pygame.draw.rect(self.screen, BLUE,
                                 pygame.Rect(
                                     left_margin + (
                                             x - 1) * block_size,
                                     top_margin + (
                                             y - 1) * block_size,
                                     block_size, block_size))
        else:
            ship_coordinates = None
            for ship_coordinates in self.player.data_ships.ships_copy:
                if len(ship_coordinates) == length:
                    self.player.data_ships.ships_copy.remove(
                        ship_coordinates)
                    break
            for x, y in ship_coordinates:
                pygame.draw.rect(self.screen, BLUE,
                                 pygame.Rect(
                                     left_margin + (
                                             x - 1) * block_size,
                                     top_margin + (
                                             y - 1) * block_size,
                                     block_size, block_size))

    def draw_hit(self,  x, y, obj, is_hurt, first_ship, last_ship) -> None:
        left_side = left_margin
        if isinstance(obj, Player):
            left_side += block_size * 15
        if is_hurt:
            pygame.draw.line(self.screen, RED, (
                left_side + x * block_size,
                top_margin + y * block_size), (
                                 left_side + (x - 1) * block_size,
                                 top_margin + (y - 1) * block_size), 3)
            pygame.draw.line(self.screen, RED, (
                left_side + (x - 1) * block_size,
                top_margin + y * block_size), (
                                 left_side + x * block_size,
                                 top_margin + (y - 1) * block_size), 3)
            if first_ship is not None:
                self.draw_fleet_statistic()
                if first_ship[1] == last_ship[1]:
                    pygame.draw.line(self.screen, BLACK, (
                        left_side + block_size * (
                                min(first_ship[0], last_ship[0]) - 1),
                        top_margin + block_size * (
                                first_ship[1] - 1) + block_size // 2),
                                     (
                                         left_side + block_size *
                                         max(first_ship[0], last_ship[0]),
                                         top_margin + block_size * (
                                                 last_ship[1] - 1) +
                                         block_size // 2), 5)
                else:
                    pygame.draw.line(self.screen, BLACK,
                                     (left_side + block_size * (
                                             first_ship[0] - 1) +
                                      block_size // 2,
                                      top_margin + block_size * (
                                              min(first_ship[1],
                                                  last_ship[1]) - 1)),
                                     (left_side + block_size * (
                                             last_ship[0] - 1) +
                                      block_size // 2,
                                      top_margin + block_size * max(
                                          first_ship[1],
                                          last_ship[1])), 5)
        else:
            pygame.draw.circle(self.screen, BLACK, (
                left_side + x * block_size - block_size // 2,
                top_margin + y * block_size - block_size // 2), 5)

    def draw_fleet_statistic(self) -> None:
        self.draw_player_statistic(self.font)
        self.computer_statistic(self.font)

    def draw_player_statistic(self, font):
        if self.is_place:
            ships_data = load_file()
            for ship in ships_data:
                self.player.dead_ships_length[ship] = 0
        else:
            ships_data = {}
            for ship in self.player.data_ships.ships:
                if len(ship) in ships_data:
                    ships_data[len(ship)] += 1
                else:
                    ships_data[len(ship)] = 1
        for key in ships_data:
            ships_data[key] -= self.player.dead_ships_length[key]
        i = 0
        j = 0
        for length in ships_data:
            pygame.draw.rect(self.screen, BLUE, pygame.Rect((
                left_margin + j * max(
                    ships_data) * block_size // 2 + j * block_size,
                top_margin + 10.5 * block_size + i * block_size // 1.5),
                (
                    length * block_size // 2,
                    block_size // 2)), 1)
            self.rect_to_place.append(pygame.Rect(pygame.Rect((
                left_margin + j * max(
                    ships_data) * block_size // 2 + j * block_size,
                top_margin + 10.5 * block_size + i * block_size // 1.5),
                (
                    length * block_size // 2,
                    block_size // 2))))
            amount_ship_text = font.render(str(ships_data[length]), True,
                                           BLACK)
            self.screen.fill(WHITE, pygame.Rect(
                (left_margin + j * max(
                    ships_data) * block_size // 2 + length * block_size // 2 + j * block_size + block_size // 4,
                 top_margin + block_size *
                 10.5 + block_size * i // 1.5 + 3),
                (amount_ship_text.get_width() * 2,
                 amount_ship_text.get_height())))
            self.screen.blit(amount_ship_text,
                             (left_margin + j * max(
                                 ships_data) * block_size // 2 + length * block_size // 2 + j * block_size + block_size // 4,
                              top_margin + block_size *
                              10.5 + block_size * i // 1.5 + 3))
            for k in range(length):
                pygame.draw.line(self.screen, BLACK,
                                 (left_margin + j * max(
                                     ships_data) * block_size // 2 + j * block_size + k * block_size // 2,
                                  top_margin + block_size * 10.5 +
                                  block_size * i // 1.5),
                                 (
                                     left_margin + j * max(
                                         ships_data) * block_size // 2 + j * block_size + k * block_size // 2,
                                     top_margin + block_size * 10.5 +
                                     block_size * i // 1.5 +
                                     block_size // 2 - 1))
            i += 1
            if i % 4 == 0:
                i = 0
                j += 1

    def computer_statistic(self, font):
        ships_data = {}
        for ship in self.computer.data_ships.ships:
            if len(ship) in ships_data:
                ships_data[len(ship)] += 1
            else:
                ships_data[len(ship)] = 1
        for key in ships_data:
            ships_data[key] -= self.computer.dead_ships_length[key]
        i = 0
        j = 0
        for length in ships_data:
            pygame.draw.rect(self.screen, BLUE, pygame.Rect((
                left_margin + 15 * block_size + j * max(
                    ships_data) * block_size // 2 + j * block_size,
                top_margin + 10.5 * block_size + i * block_size // 1.5),
                (
                    length * block_size // 2,
                    block_size // 2)), 1)
            amount_ship_text = font.render(str(ships_data[length]), True,
                                           BLACK)

            self.screen.fill(WHITE, pygame.Rect(
                (left_margin + 15 * block_size + j * max(
                    ships_data) * block_size // 2 + length * block_size // 2 + j * block_size + block_size // 4,
                 top_margin + block_size *
                 10.5 + block_size * i // 1.5 + 3),
                (amount_ship_text.get_width() * 2,
                 amount_ship_text.get_height())))
            self.screen.blit(amount_ship_text,
                             (left_margin + 15 * block_size + j * max(
                                 ships_data) * block_size // 2 + length * block_size // 2 + j * block_size + block_size // 4,
                              top_margin + block_size *
                              10.5 + block_size * i // 1.5 + 3))
            for k in range(length):
                pygame.draw.line(self.screen, BLACK,
                                 (left_margin + 15 * block_size + j * max(
                                     ships_data) * block_size // 2 + j * block_size + k * block_size // 2,
                                  top_margin + block_size * 10.5 +
                                  block_size * i // 1.5),
                                 (
                                     left_margin + 15 * block_size + j * max(
                                         ships_data) * block_size // 2 + j * block_size + k * block_size // 2,
                                     top_margin + block_size * 10.5 +
                                     block_size * i // 1.5 +
                                     block_size // 2 - 1))
            i += 1
            if i % 4 == 0:
                i = 0
                j += 1

    def place_ship_manually(self, cell, rect, is_horizontal):
        if self.wrong_ship_placed:
            self.delete_message()
        ships_data = load_file()
        if not self.player.data_ships.ships_placed:
            for ship in ships_data:
                self.player.data_ships.ships_placed[ship] = 0
        if self.player.data_ships.ships_placed[
            rect.w // (block_size // 2)] < ships_data[
            rect.w // (block_size // 2)]:
            result = self.player.data_ships.create_ship(
                rect.width // (block_size // 2),
                True, cell, not is_horizontal)
            if result:
                if is_horizontal:
                    pygame.draw.rect(self.screen, BLUE,
                                     pygame.Rect(left_margin + (
                                             cell[0] - 1) * block_size,
                                                 top_margin + (
                                                         cell[1] - 1)
                                                 * block_size,
                                                 rect.width * 2,
                                                 rect.height * 2))
                else:
                    pygame.draw.rect(self.screen, BLUE,
                                     pygame.Rect(left_margin + (
                                             cell[0] - 1) * block_size,
                                                 top_margin + (
                                                         cell[1] - 1)
                                                 * block_size,
                                                 rect.height * 2,
                                                 rect.width * 2))
                i = 0
                j = 0
                for length in ships_data:
                    amount_ship_text = self.font.render(
                        str(ships_data[length] -
                            self.player.data_ships.ships_placed[length]),
                        True,
                        BLACK)
                    self.screen.fill(WHITE, pygame.Rect(
                        (left_margin + j * max(
                            ships_data) * block_size // 2 + length * block_size // 2 + j * block_size + block_size // 4,
                         top_margin + block_size *
                         10.5 + block_size * i // 1.5 + 3),
                        (amount_ship_text.get_width(),
                         amount_ship_text.get_height())))
                    self.screen.blit(amount_ship_text,
                                     (left_margin + j * max(
                                         ships_data) * block_size // 2 + length * block_size // 2 + j * block_size + block_size // 4,
                                      top_margin + block_size *
                                      10.5 + block_size * i // 1.5 + 3))
                    i += 1
                    if i % 4 == 0:
                        i = 0
                        j += 1
            else:
                self.last_message = "Невозможно установить корабль"
                self.draw_centre_text(
                    self.last_message,
                    round(block_size * 1.5), RED,
                    offset_y=400, offset_x=200)
                self.wrong_ship_placed = True

        else:
            self.last_message = "Больше нет таких кораблей"
            self.draw_centre_text(
                self.last_message,
                round(block_size * 1.5), RED,
                offset_y=400, offset_x=200)
            self.wrong_ship_placed = True

    def delete_message(self):
        text_data = self.draw_centre_text(
            self.last_message,
            block_size * 2, RED,
            offset_y=400, offset_x=200)
        self.screen.fill(WHITE, pygame.Rect(*text_data))
        self.wrong_ship_placed = False


def load_file():
    data = {}
    with open('ships.txt', 'r', encoding="UTF-8") as file_obj:
        is_title = True
        for line in file_obj.readlines():
            if is_title:
                is_title = False
            else:
                temp = line.strip()
                if temp.find(" - ") == -1:
                    raise ValueError
                data[int(temp.split(' - ')[0])] = \
                    int(temp.split(' - ')[1])
    space = 0
    for k, v in data.items():
        space += k*v
        if k > 10 or k < 1 or v < 1 or space>20:
            raise ValueError
    return data
