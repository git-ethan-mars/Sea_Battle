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
    def draw_player_ship(length):
        ship_coordinates = player.ships.create_ship(length)
        while not ship_coordinates:
            ship_coordinates = computer.ships.create_ship(length)
        for x, y in ship_coordinates:
            pygame.draw.rect(screen, BLUE,
                             pygame.Rect(
                                 left_margin + (x - 1) * block_size,
                                 top_margin + (y - 1) * block_size,
                                 block_size, block_size))

    @staticmethod
    def draw_hit(x, y, ships_set, enemy_left, enemy_top):
        if (x, y) in [j for i in ships_set for j in i]:
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
        else:
            pygame.draw.circle(screen, BLACK, (
                enemy_left + x * block_size - block_size // 2,
                enemy_top + y * block_size - block_size // 2), 5)


def main():
    game = Game()
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game_over = False
    screen.fill(WHITE)
    game.draw_grid()
    button = game.draw_quit_button()
    for length in range(4, 0, -1):
        for _ in range(5 - length):
            computer.ships.create_ship(length)
            Game.draw_player_ship(length)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                temp = player.shoot(event.pos)
                if temp is not None:
                    Game.draw_hit(*temp)
                    Game.draw_hit(*computer.shoot())
        pygame.display.update()


main()
pygame.quit()
