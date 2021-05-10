import pygame
import ships
import player

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
block_size = 45
left_margin = 90
top_margin = 72
screen = pygame.display.set_mode((1280, 720))


class Game:
    @staticmethod
    def draw_quit_button():
        font_size = block_size // 2
        font = pygame.font.SysFont('notosans', font_size)
        button = pygame.Rect(1280 - int(block_size * 1.5), 0, int(block_size * 1.5), block_size)
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
            pygame.draw.line(screen, BLACK, (left_margin, top_margin + i * block_size),
                             (left_margin + 10 * block_size, top_margin + i * block_size), 1)
            # Vert grid1
            pygame.draw.line(screen, BLACK, (left_margin + i * block_size, top_margin),
                             (left_margin + i * block_size, top_margin + 10 * block_size), 1)
            # Hor grid2
            pygame.draw.line(screen, BLACK, (left_margin + 15 * block_size, top_margin +
                                             i * block_size),
                             (left_margin + 25 * block_size, top_margin + i * block_size), 1)
            # Vert grid2
            pygame.draw.line(screen, BLACK, (left_margin + (i + 15) * block_size, top_margin),
                             (left_margin + (i + 15) * block_size, top_margin + 10 * block_size), 1)

            if i < 10:
                num_ver = font.render(str(i + 1), True, BLACK)
                letters_hor = font.render(letters[i], True, BLACK)

                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                letters_hor_width = letters_hor.get_width()

                # Ver num grid1
                screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_width // 2),
                                      top_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
                # Hor letters grid1
                screen.blit(letters_hor, (left_margin + i * block_size + (block_size //
                                                                          2 - letters_hor_width // 2),
                                          top_margin - block_size // 2))
                # Ver num grid2
                screen.blit(num_ver, (left_margin - (block_size // 2 + num_ver_width // 2) + 15 *
                                      block_size,
                                      top_margin + i * block_size + (block_size // 2 - num_ver_height // 2)))
                # Hor letters grid2
                screen.blit(letters_hor, (left_margin + i * block_size + (block_size // 2 -
                                                                          letters_hor_width // 2) + 15 * block_size,
                                          top_margin - block_size // 2))


def main():
    game = Game()
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game_over = False
    screen.fill(WHITE)
    game.draw_grid()
    button = game.draw_quit_button()
    p = player.Player()
    computer = ships.Ships()
    for length in range(4, 0, -1):
        for _ in range(5 - length):
            p.ships.draw_ship(length, screen)
            temp = computer.create_ship(length)[0]
            while not temp:
                temp = computer.create_ship(length)[0]

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                p.shoot(event.pos,computer.ships_set)

        pygame.display.update()


main()
pygame.quit()
