import pygame
from players import Player, Computer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self, is_smart=True):
        self.is_fast = False
        self.is_smart = is_smart
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.block_size = 70
        self.left_margin = 90
        self.top_margin = 130
        self.is_menu = True
        self.is_options = False
        self.is_finished = False
        self.player = Player(self)
        self.computer = Computer(self)
        self.ships_amount = 0

    def draw_new_game(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        for length in range(4, 0, -1):
            for _ in range(5 - length):
                self.ships_amount += length
                computer_ship_is_created = self.computer.ships.create_ship(length)
                while not computer_ship_is_created:
                    computer_ship_is_created = self.computer.ships.create_ship(
                        length)
                self.draw_player_ship(length)

    def draw_centre_text(self, text, offset_x=0, offset_y=0):
        font_size = self.block_size * 3
        font = pygame.font.SysFont('notosans', font_size)
        text = font.render(text, True, BLACK)
        self.screen.blit(text, (
            (self.screen.get_width() - text.get_width()) // 2 + offset_x,
            (self.screen.get_height() - text.get_height()) // 2 + offset_y))

    def draw_centre_button(self, text: str, color: tuple, offset_x: int = 0,
                           offset_y: int = 0):
        font_size = self.block_size * 3
        font = pygame.font.SysFont('notosans', font_size)
        button_text = font.render(text, True, BLACK)
        button = pygame.Rect(
            (self.screen.get_width() - button_text.get_width()) // 2 + offset_x,
            (self.screen.get_height() - button_text.get_height()) // 2 + offset_y,
            button_text.get_width(), button_text.get_height())
        pygame.draw.rect(self.screen, color, button)
        self.screen.blit(button_text, (
            (self.screen.get_width() - button_text.get_width()) // 2 + offset_x,
            (self.screen.get_height() - button_text.get_height()) // 2 + offset_y))
        return button

    def draw_menu(self):
        self.screen.fill(WHITE)
        new_game_button = self.draw_centre_button("Новая игра", BLUE,
                                                  offset_y=-250)
        fast_game_button = self.draw_centre_button("Быстрая игра", GREEN,
                                                   offset_y=-80)
        options_button = self.draw_centre_button("Опции", BLUE, offset_y=80)
        exit_button = self.draw_centre_button("Выход из игры", RED, offset_y=250)
        return new_game_button, fast_game_button, options_button, exit_button

    def draw_options(self):
        self.screen.fill(WHITE)
        self.draw_centre_text("Опции", offset_y=-250)
        if self.is_smart:
            computer_mode_button = self.draw_centre_button("Умный противник", GREEN,offset_y=-75)
        else:
            computer_mode_button = self.draw_centre_button("Глупый противник", RED,
                                                           offset_y=-75)
        menu_button = self.draw_centre_button("Назад в меню", RED,offset_y=100)
        return computer_mode_button, menu_button

    def draw_back_to_menu_button(self):
        font_size = self.block_size // 2
        font = pygame.font.SysFont('notosans', font_size)
        button = pygame.Rect(1920 - int(self.block_size * 2.8), 0,
                             int(self.block_size * 2.8), self.block_size)
        pygame.draw.rect(self.screen, (255, 0, 0), button)
        back_text = font.render("Назад в меню", True, BLACK)
        self.screen.blit(back_text,
                         (1920 - int(self.block_size * 2.6), self.block_size // 3))
        return button

    def draw_winner(self, winner):
        font_size = self.block_size * 4
        font = pygame.font.SysFont('notosans', font_size)
        text = font.render(f"Победил {winner}!", True, RED)
        self.screen.blit(text, (0, self.block_size * 13))

    def draw_grid(self):
        font_size = int(self.block_size // 1.5)
        font = pygame.font.SysFont('notosans', font_size)
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        for i in range(11):
            pygame.draw.line(self.screen, BLACK,
                             (self.left_margin,
                              self.top_margin + i * self.block_size),
                             (self.left_margin + 10 * self.block_size,
                              self.top_margin + i * self.block_size), 1)
            pygame.draw.line(self.screen, BLACK,
                             (self.left_margin + i * self.block_size,
                              self.top_margin),
                             (self.left_margin + i * self.block_size,
                              self.top_margin + 10 * self.block_size), 1)
            pygame.draw.line(self.screen, BLACK,
                             (self.left_margin + 15 * self.block_size,
                              self.top_margin +
                              i * self.block_size),
                             (self.left_margin + 25 * self.block_size,
                              self.top_margin + i * self.block_size), 1)
            pygame.draw.line(self.screen, BLACK,
                             (self.left_margin + (i + 15) * self.block_size,
                              self.top_margin),
                             (self.left_margin + (i + 15) * self.block_size,
                              self.top_margin + 10 * self.block_size), 1)

            if i < 10:
                num_ver = font.render(str(i + 1), True, BLACK)
                letters_hor = font.render(letters[i], True, BLACK)
                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_width = letters_hor.get_width()
                self.screen.blit(num_ver, (
                    self.left_margin - (self.block_size // 2 + num_ver_width // 2),
                    self.top_margin + i * self.block_size + (
                            self.block_size // 2 - num_ver_height // 2)))
                self.screen.blit(letters_hor,
                                 (self.left_margin + i * self.block_size + (
                                         self.block_size //
                                         2 - letters_hor_width // 2),
                                  self.top_margin - self.block_size // 2))
                self.screen.blit(num_ver, (
                    self.left_margin - (
                            self.block_size // 2 + num_ver_width // 2) + 15 *
                    self.block_size,
                    self.top_margin + i * self.block_size + (
                            self.block_size // 2 - num_ver_height // 2)))
                # Hor letters grid2
                self.screen.blit(letters_hor,
                                 (self.left_margin + i * self.block_size + (
                                         self.block_size // 2 -
                                         letters_hor_width // 2) + 15 * self.block_size,
                                  self.top_margin - self.block_size // 2))

    def draw_player_ship(self, length: int) -> None:
        ship_coordinates = self.player.ships.create_ship(length)
        while not ship_coordinates:
            ship_coordinates = self.player.ships.create_ship(length)
        for x, y in ship_coordinates:
            pygame.draw.rect(self.screen, BLUE,
                             pygame.Rect(
                                 self.left_margin + (x - 1) * self.block_size,
                                 self.top_margin + (y - 1) * self.block_size,
                                 self.block_size, self.block_size))

    def draw_hit(self, x: float, y: float, enemy_left: int, enemy_top: int,
                 is_hurt: bool, first_ship: tuple or None,
                 last_ship: tuple or None) -> None:
        if is_hurt:
            pygame.draw.line(self.screen, RED, (
                enemy_left + x * self.block_size,
                enemy_top + y * self.block_size), (
                                 enemy_left + (x - 1) * self.block_size,
                                 enemy_top + (y - 1) * self.block_size), 3)
            pygame.draw.line(self.screen, RED, (
                enemy_left + (x - 1) * self.block_size,
                enemy_top + y * self.block_size), (
                                 enemy_left + x * self.block_size,
                                 enemy_top + (y - 1) * self.block_size), 3)
            if first_ship is not None:
                if first_ship[1] == last_ship[1]:
                    pygame.draw.line(self.screen, BLACK, (
                        enemy_left + self.block_size * (
                                min(first_ship[0], last_ship[0]) - 1),
                        enemy_top + self.block_size * (
                                first_ship[1] - 1) + self.block_size // 2),
                                     (
                                         enemy_left + self.block_size *
                                         max(first_ship[0], last_ship[0]),
                                         enemy_top + self.block_size * (
                                                 last_ship[
                                                     1] - 1) + self.block_size // 2),
                                     5)
                else:
                    pygame.draw.line(self.screen, BLACK,
                                     (enemy_left + self.block_size * (first_ship[
                                                                          0] - 1) + self.block_size // 2,
                                      enemy_top + self.block_size * (
                                              min(first_ship[1],
                                                  last_ship[1]) - 1)),
                                     (enemy_left + self.block_size * (last_ship[
                                                                          0] - 1) + self.block_size // 2,
                                      enemy_top + self.block_size * max(
                                          first_ship[1],
                                          last_ship[
                                              1])), 5)
        else:
            pygame.draw.circle(self.screen, BLACK, (
                enemy_left + x * self.block_size - self.block_size // 2,
                enemy_top + y * self.block_size - self.block_size // 2), 5)


def main():
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game = Game()
    new_game_button, fast_game_button, options_button, exit_button = game.draw_menu()
    working = True
    while working:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if (not game.is_menu or game.is_options) \
                        and menu_button.collidepoint(event.pos):
                    game.__init__(game.is_smart)
                    new_game_button, fast_game_button, options_button, exit_button = game.draw_menu()
                elif game.is_menu and not game.is_options and (
                        new_game_button.collidepoint(
                            event.pos) or fast_game_button.collidepoint(event.pos)):
                    game.draw_new_game()
                    menu_button = game.draw_back_to_menu_button()
                    game.is_menu = False
                elif game.is_menu and not game.is_options and exit_button.collidepoint(
                        event.pos):
                    pygame.quit()
                    working = False
                    break
                elif game.is_menu and options_button.collidepoint(event.pos):
                    game.is_options = True
                    computer_mode_button, menu_button = game.draw_options()
                elif game.is_options and computer_mode_button.collidepoint(
                        event.pos):
                    game.is_smart = not game.is_smart
                    computer_mode_button, menu_button = game.draw_options()
                elif not (game.is_finished or game.is_menu):
                    player_shoot_status = game.player.shoot(game,
                                                            event.pos)
                    if player_shoot_status is not None:
                        game.draw_hit(*player_shoot_status)
                        if not player_shoot_status[4]:
                            computer_shoot_status = game.computer.shoot(game)
                            game.draw_hit(*computer_shoot_status)
                            while computer_shoot_status[4]:
                                game.player.dead_ships += 1
                                computer_shoot_status = game.computer.shoot(game)
                                game.draw_hit(*computer_shoot_status)
                        else:
                            game.computer.dead_ships += 1
        if not game.is_menu and game.player.dead_ships == game.ships_amount:
            game.draw_winner("Копьютер")
            game.is_finished = True
        elif not game.is_menu and game.computer.dead_ships == game.ships_amount:
            game.draw_winner("Игрок")
            game.is_finished = True


if __name__ == '__main__':
    main()
