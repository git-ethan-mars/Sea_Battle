import pygame
from players import Player, Computer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
block_size = 45
left_margin = 90
top_margin = 72
screen = pygame.display.set_mode((1280, 720))
player = Player()
computer = Computer()


class Game:
    @staticmethod
    def draw_quit_button():
        font_size = block_size // 2
        font = pygame.font.SysFont('notosans', font_size)
        button = pygame.Rect(1280 - int(block_size * 1.5), 0,
                             int(block_size * 1.5), block_size)
        pygame.draw.rect(screen, (255, 0, 0), button)
        quit_text = font.render("Выход", True, BLACK)
        screen.blit(quit_text, (1280 - int(block_size * 1.3), block_size // 3))
        return button

    @staticmethod
    def draw_winner(winner):
        font_size = block_size * 4
        font = pygame.font.SysFont('notosans', font_size)
        text = font.render(f"Победил {winner}!", True, RED)
        screen.blit(text, (0, block_size * 13))

    @staticmethod
    def draw_grid():
        font_size = int(block_size // 1.5)
        font = pygame.font.SysFont('notosans', font_size)
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']
        for i in range(11):
            # Hor grid1
            pygame.draw.line(screen, BLACK,
                             (left_margin, top_margin + i * block_size),
                             (left_margin + 10 * block_size,
                              top_margin + i * block_size), 1)
            # Vert grid1
            pygame.draw.line(screen, BLACK,
                             (left_margin + i * block_size, top_margin),
                             (left_margin + i * block_size,
                              top_margin + 10 * block_size), 1)
            # Hor grid2
            pygame.draw.line(screen, BLACK,
                             (left_margin + 15 * block_size, top_margin +
                              i * block_size),
                             (left_margin + 25 * block_size,
                              top_margin + i * block_size), 1)
            # Vert grid2
            pygame.draw.line(screen, BLACK,
                             (left_margin + (i + 15) * block_size, top_margin),
                             (left_margin + (i + 15) * block_size,
                              top_margin + 10 * block_size), 1)

            if i < 10:
                num_ver = font.render(str(i + 1), True, BLACK)
                letters_hor = font.render(letters[i], True, BLACK)
                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_width = letters_hor.get_width()
                # Ver num grid1
                screen.blit(num_ver, (
                    left_margin - (block_size // 2 + num_ver_width // 2),
                    top_margin + i * block_size + (
                            block_size // 2 - num_ver_height // 2)))
                # Hor letters grid1
                screen.blit(letters_hor,
                            (left_margin + i * block_size + (block_size //
                                                             2 - letters_hor_width // 2),
                             top_margin - block_size // 2))
                # Ver num grid2
                screen.blit(num_ver, (
                    left_margin - (block_size // 2 + num_ver_width // 2) + 15 *
                    block_size,
                    top_margin + i * block_size + (
                            block_size // 2 - num_ver_height // 2)))
                # Hor letters grid2
                screen.blit(letters_hor,
                            (left_margin + i * block_size + (block_size // 2 -
                                                             letters_hor_width // 2) + 15 * block_size,
                             top_margin - block_size // 2))

    @staticmethod
    def draw_player_ship(length: int) -> None:
        ship_coordinates = player.ships.create_ship(length)
        while not ship_coordinates:
            ship_coordinates = player.ships.create_ship(length)
        for x, y in ship_coordinates:
            pygame.draw.rect(screen, BLUE,
                             pygame.Rect(
                                 left_margin + (x - 1) * block_size,
                                 top_margin + (y - 1) * block_size,
                                 block_size, block_size))

    @staticmethod
    def draw_hit(x: float, y: float, enemy_left: int, enemy_top: int,
                 is_hurt: bool, first_ship: tuple or None,
                 last_ship: tuple or None) -> None:
        if is_hurt:
            pygame.draw.line(screen, RED, (
                enemy_left + x * block_size,
                enemy_top + y * block_size), (
                                 enemy_left + (x - 1) * block_size,
                                 enemy_top + (y - 1) * block_size), 3)
            pygame.draw.line(screen, RED, (
                enemy_left + (x - 1) * block_size,
                enemy_top + y * block_size), (
                                 enemy_left + x * block_size,
                                 enemy_top + (y - 1) * block_size), 3)
            if first_ship is not None:
                if first_ship[1] == last_ship[1]:
                    pygame.draw.line(screen, BLACK, (
                        enemy_left + block_size * (
                                min(first_ship[0], last_ship[0]) - 1),
                        enemy_top + block_size * (
                                first_ship[1] - 1) + block_size // 2),
                                     (
                                         enemy_left + block_size *
                                         max(first_ship[0], last_ship[0]),
                                         enemy_top + block_size * (
                                                 last_ship[
                                                     1] - 1) + block_size // 2),
                                     5)
                else:
                    pygame.draw.line(screen, BLACK,
                                     (enemy_left + block_size * (first_ship[
                                                                     0] - 1) + block_size // 2,
                                      enemy_top + block_size * (
                                              min(first_ship[1],
                                                  last_ship[1]) - 1)),
                                     (enemy_left + block_size * (last_ship[
                                                                     0] - 1) + block_size // 2,
                                      enemy_top + block_size * max(first_ship[1],
                                                                   last_ship[
                                                                       1])), 5)
        else:
            pygame.draw.circle(screen, BLACK, (
                enemy_left + x * block_size - block_size // 2,
                enemy_top + y * block_size - block_size // 2), 5)


def main():
    game = Game()
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game_over = False
    finished = False
    screen.fill(WHITE)
    game.draw_grid()
    button = game.draw_quit_button()
    amount_of_ships = 0
    for length in range(4, 0, -1):
        for _ in range(5 - length):
            amount_of_ships += length
            computer_ship_is_created = computer.ships.create_ship(length)
            while not computer_ship_is_created:
                computer_ship_is_created = computer.ships.create_ship(length)
            Game.draw_player_ship(length)
    print(Computer.ships.ships_set)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                player_shoot_status = player.shoot(event.pos)
                if player_shoot_status is not None:
                    Game.draw_hit(*player_shoot_status)
                    if not player_shoot_status[4]:
                        computer_shoot_status = computer.shoot()
                        Game.draw_hit(*computer_shoot_status)
                        while computer_shoot_status[4]:
                            computer_shoot_status = computer.shoot()
                            Game.draw_hit(*computer_shoot_status)

        pygame.display.update()
        if player.dead_ships == amount_of_ships:
            Game.draw_winner("Копьютер")
            finished = True
        elif computer.dead_ships == amount_of_ships:
            Game.draw_winner("Игрок")
            finished = True


if __name__ == '__main__':
    main()
    pygame.quit()
