import pygame
from players import Player, Computer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.block_size = 70
        self.left_margin = 90
        self.top_margin = 130
        self.player = Player(self)
        self.computer = Computer(self)

    def draw_menu(self):
        self.screen.fill(WHITE)

    def draw_quit_button(self):
        font_size = self.block_size // 2
        font = pygame.font.SysFont('notosans', font_size)
        button = pygame.Rect(1920 - int(self.block_size * 1.5), 0,
                             int(self.block_size * 1.5), self.block_size)
        pygame.draw.rect(self.screen, (255, 0, 0), button)
        quit_text = font.render("Выход", True, BLACK)
        self.screen.blit(quit_text,
                         (1920 - int(self.block_size * 1.3), self.block_size // 3))
        return button

    def draw_restart_button(self):
        font_size = self.block_size // 2
        font = pygame.font.SysFont('notosans', font_size)
        button = pygame.Rect(1920 - int(self.block_size * 5), 0,
                             int(self.block_size * 2), self.block_size)
        pygame.draw.rect(self.screen, (255, 0, 0), button)
        quit_text = font.render("Перезапуск", True, BLACK)
        self.screen.blit(quit_text,
                         (1920 - int(self.block_size * 4.95), self.block_size // 3))
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
    game = Game()
    game_finished = False
    restart = False
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game.screen.fill(WHITE)
    game.draw_grid()
    quit_button = game.draw_quit_button()
    restart_button = game.draw_restart_button()
    amount_of_ships = 0
    for length in range(4, 0, -1):
        for _ in range(5 - length):
            amount_of_ships += length
            computer_ship_is_created = game.computer.ships.create_ship(length)
            while not computer_ship_is_created:
                computer_ship_is_created = game.computer.ships.create_ship(length)
            game.draw_player_ship(length)
    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    flag = True
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    pygame.quit()
                    flag = True
                    restart = True
                    break
            if event.type == pygame.MOUSEBUTTONDOWN and not game_finished:
                player_shoot_status = game.player.shoot(game,
                                                        event.pos)
                if player_shoot_status is not None:
                    game.draw_hit(*player_shoot_status)
                    if not player_shoot_status[4]:
                        computer_shoot_status = game.computer.shoot(game.player)
                        game.draw_hit(*computer_shoot_status)
                        while computer_shoot_status[4]:
                            game.player.dead_ships += 1
                            computer_shoot_status = game.computer.shoot(game.player)
                            game.draw_hit(*computer_shoot_status)
                    else:
                        game.computer.dead_ships += 1
        if flag:
            break
        pygame.display.update()
        if game.player.dead_ships == amount_of_ships:
            game.draw_winner("Копьютер")
            game_finished = True
        elif game.computer.dead_ships == amount_of_ships:
            game.draw_winner("Игрок")
            game_finished = True

    if restart:
        main()


if __name__ == '__main__':
    main()
