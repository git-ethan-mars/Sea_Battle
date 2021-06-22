import pygame
from players import Player, Computer
from settings import *
from shipsSet import is_on_field


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
                    raise IndexError
                data[int(temp.split(' - ')[0])] = \
                    int(temp.split(' - ')[1])
    space = 0
    for k, v in data.items():
        space += k * v
        if k > 10 or k < 1 or v < 1 or space > 20:
            raise ValueError
    return data


class Game:
    def __init__(self, is_smart=True):
        self.is_place = False
        self.is_smart = is_smart
        self.screen = pygame.display.set_mode((1920, 1080))
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
        self.file_font = 'noto-sans.ttf'
        self.font = pygame.font.Font(self.file_font,
                                     int(block_size // 3))
        self.message_rect = None
        self.ship_to_replace = None

    def draw_new_game(self):
        try:
            self.is_place = True
            self.screen.fill(WHITE)
            self.draw_player_statistic(self.font)
            self.draw_grid()
            self.is_menu = False
            return self.draw_back_to_menu_button()
        except IndexError:
            self.is_place = False
            self.draw_menu()
            self.draw_centre_text(
                "В файле ships.txt введены некоректные данные!",
                40,
                RED, offset_y=470)
            self.draw_centre_text(
                "Измените и сохраните его",
                40,
                RED, offset_y=500)
        except ValueError:
            self.is_place = False
            self.draw_menu()
            self.draw_centre_text(
                "Уменьшите количество кораблей",
                40,
                RED, offset_y=470)
            self.draw_centre_text(
                "Невозможна генерация поля",
                40,
                RED, offset_y=500)
            self.player = Player()
            self.computer = Computer()

    def draw_fast_game(self):
        try:
            self.is_place = False
            self.screen.fill(WHITE)
            self.draw_grid()
            self.draw_ships()
            self.draw_fleet_statistic()
            self.is_menu = False
            return self.draw_back_to_menu_button()
        except IndexError:
            self.draw_menu()
            self.draw_centre_text(
                "В файле ships.txt введены некоректные данные!",
                40,
                RED, offset_y=470)
            self.draw_centre_text(
                "Измените и сохраните его",
                40,
                RED, offset_y=500)
        except ValueError:
            self.draw_menu()
            self.draw_centre_text(
                "Уменьшите количество кораблей",
                40,
                RED, offset_y=470)
            self.draw_centre_text(
                "Невозможна генерация поля",
                40,
                RED, offset_y=500)
            self.player = Player()
            self.computer = Computer()

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
        font = pygame.font.Font(self.file_font, int(font_size))
        text = font.render(text, True, color)
        self.message_rect = self.screen.blit(text, (
            (self.screen.get_width() - text.get_width()) // 2 + offset_x,
            (self.screen.get_height() - text.get_height()) // 2 + offset_y))

    def draw_centre_button(self, text: str, color: tuple, offset_x: int = 0,
                           offset_y: int = 0) -> pygame.Rect:
        font_size = int(block_size * 1.5)
        font = pygame.font.Font(self.file_font, font_size)
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
        self.draw_centre_text("Опции", block_size * 2, BLACK,
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
        font = pygame.font.Font(self.file_font, font_size)
        back_text = font.render("Назад в меню", True, BLACK)
        button = pygame.Rect(1920 - back_text.get_width() - block_size // 3, 0,
                             back_text.get_width() + block_size // 3,
                             block_size)
        pygame.draw.rect(self.screen, RED, button)
        self.screen.blit(back_text,
                         (1920 - int(block_size * 3.5),
                          block_size // 7))
        return button

    def draw_winner(self, winner: str) -> None:
        font_size = block_size * 4
        font = pygame.font.Font(self.file_font, font_size)
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

    def draw_hit(self, x, y, obj, is_hurt, first_ship, last_ship) -> None:
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
            if ships_data is None:
                return
            for ship in ships_data:
                self.player.dead_ships_length[ship] = 0
        else:
            ships_data = {}
            for ship in self.player.data_ships.ships:
                if len(ship) in ships_data:
                    ships_data[len(ship)] += 1
                else:
                    ships_data[len(ship)] = 1
        ships_data = dict(
            sorted(ships_data.items(), key=lambda x: x[0], reverse=True))
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

    def place_ship_manually(self, cell, rect_width, rect_height,
                            is_horizontal, replace=False):
        if self.wrong_ship_placed:
            self.delete_message()
        ships_data = load_file()
        if not self.player.data_ships.ships_placed:
            for ship in ships_data:
                self.player.data_ships.ships_placed[ship] = 0
        if self.player.data_ships.ships_placed[
            rect_width // (block_size // 2)] < ships_data[
            rect_width // (block_size // 2)] or replace:
            result = self.player.data_ships.create_ship(
                max(rect_width, rect_height) // (block_size // 2),
                True, cell, not is_horizontal, replace)
            if result:
                if replace:
                    self.color_ship(self.ship_to_replace, WHITE)
                    self.refresh_cells(self.ship_to_replace)
                self.color_ship(result, BLUE)
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
                    block_size, RED,
                    offset_y=400, offset_x=200)
                self.wrong_ship_placed = True
                if replace:
                    self.player.data_ships.create_ship(
                        max(rect_width, rect_height) // (block_size // 2),
                        True, self.ship_to_replace[0], not is_horizontal,replace)
                    self.color_ship(self.ship_to_replace, BLUE)
        else:
            self.last_message = "Больше нет таких кораблей"
            self.draw_centre_text(
                self.last_message,
                block_size, RED,
                offset_y=400, offset_x=200)
            self.wrong_ship_placed = True

    def delete_message(self):
        self.screen.fill(WHITE, self.message_rect)
        self.wrong_ship_placed = False

    def mark_current_ship(self, current_rect):
        if self.rect_taken is not None:
            pygame.draw.circle(self.screen, WHITE, (
                self.rect_taken.left - 15, self.rect_taken.centery), 5)
        pygame.draw.circle(self.screen, RED, (
            current_rect.left - 15, current_rect.centery), 5)

    def change_ship_position(self, cell, length, is_horizontal):
        if not is_on_field(cell):
            self.color_ship(self.ship_to_replace, BLUE)
        else:
            temp = cell
            self.player.data_ships.ships.remove(self.ship_to_replace)
            for cell in self.ship_to_replace:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if is_on_field(
                                (cell[0] + i, cell[1] + j)) and (
                                cell[0] + i, cell[
                                                 1] + j) not in self.player.data_ships.available_cells:
                            self.player.data_ships.available_cells.append(
                                (cell[0] + i, cell[1] + j))
            cell = temp
            if is_horizontal:
                self.place_ship_manually(cell, length * (block_size // 2),
                                         block_size // 2, is_horizontal, True)
            else:
                self.place_ship_manually(cell, block_size // 2,
                                         length * (block_size // 2),
                                         is_horizontal,
                                         True)

    def color_ship(self, ship, color):
        for cell in ship:
            pygame.draw.rect(self.screen, color,
                             pygame.Rect(left_margin + (
                                     cell[0] - 1) * block_size,
                                         top_margin + (
                                                 cell[1] - 1)
                                         * block_size,
                                         block_size,
                                         block_size))

    def refresh_cells(self, ship):
        for cell in ship:
            pygame.draw.line(self.screen, BLACK, (
                left_margin + (cell[0] - 1) * block_size,
                top_margin + (cell[1] - 1) * block_size), (
                                 left_margin + (cell[0] - 1) * block_size,
                                 top_margin + cell[1] * block_size))
            pygame.draw.line(self.screen, BLACK, (
                left_margin + (cell[0] - 1) * block_size,
                top_margin + (cell[1] - 1) * block_size), (
                                 left_margin + cell[0] * block_size,
                                 top_margin + (cell[1] - 1) * block_size))
            pygame.draw.line(self.screen, BLACK, (
                left_margin + cell[0] * block_size,
                top_margin + (cell[1] - 1) * block_size), (
                                 left_margin + cell[0] * block_size,
                                 top_margin + cell[1] * block_size))
            pygame.draw.line(self.screen, BLACK, (
                left_margin + (cell[0] - 1) * block_size,
                top_margin + cell[1] * block_size), (
                                 left_margin + cell[0] * block_size,
                                 top_margin + cell[1] * block_size))
