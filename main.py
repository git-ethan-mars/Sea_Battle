import pygame
from game import Game, RED, Player, Computer


def main():
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game = Game()
    new_game_button, fast_game_button, \
    options_button, exit_button = game.draw_menu()
    working = True
    while working:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
                if (not game.is_menu or game.is_options) \
                        and menu_button.collidepoint(event.pos):
                    game = Game(game.is_smart)
                    new_game_button, fast_game_button, \
                    options_button, exit_button = game.draw_menu()
                elif game.is_menu and not game.is_options and new_game_button.collidepoint(
                        event.pos):
                    game.is_place = True
                    game.draw_new_game()
                    game.draw_fleet_statistic()
                    menu_button = game.draw_back_to_menu_button()
                    game.is_menu = False
                elif any([rect.collidepoint(event.pos) for rect in
                          game.rect_to_place]):
                    for rect in game.rect_to_place:
                        if rect.collidepoint(event.pos):
                            game.rect_taken = rect
                elif game.rect_taken is not None:
                    cell = Player.get_cell(game, event.pos)
                    if game.player.data_ships.is_on_field(cell):
                        game.draw_ship_manually(cell, game.rect_taken,event.button == 1)

                elif game.is_menu and not game.is_options and \
                        fast_game_button.collidepoint(event.pos):
                    try:
                        game.draw_fast_game()
                        menu_button = game.draw_back_to_menu_button()
                        game.is_menu = False
                    except ValueError:
                        game.draw_menu()
                        game.draw_centre_text(
                            "В файле ships.txt введены некоректные данные!",
                            40,
                            RED, offset_y=470)
                        game.draw_centre_text(
                            "Измените и сохраните его",
                            40,
                            RED, offset_y=500)
                    except IndexError:
                        game.draw_menu()
                        game.draw_centre_text(
                            "Уменьшите количество кораблей",
                            40,
                            RED, offset_y=470)
                        game.draw_centre_text(
                            "Невозможна генерация поля",
                            40,
                            RED, offset_y=500)
                        game.player = Player(game)
                        game.computer = Computer(game)
                elif game.is_menu and not game.is_options and \
                        exit_button.collidepoint(event.pos):
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
                elif not (game.is_finished or game.is_menu or game.is_place):
                    player_shoot_status = game.player.shoot(game,
                                                            event.pos)
                    if player_shoot_status is not None:
                        game.draw_hit(*player_shoot_status)
                        if not player_shoot_status[4]:
                            computer_shoot_status = game.computer.shoot(game)
                            game.draw_hit(*computer_shoot_status)
                            while computer_shoot_status[4]:
                                game.player.dead_ships += 1
                                computer_shoot_status = game.computer.shoot(
                                    game)
                                game.draw_hit(*computer_shoot_status)
                        else:
                            game.computer.dead_ships += 1
        if not game.is_menu and game.player.dead_ships == game.ships_amount != 0:
            game.draw_centre_text("Победил компьютер!", game.block_size * 3.5,
                                  RED)
            game.is_finished = True
        elif not game.is_menu and \
                game.computer.dead_ships == game.ships_amount != 0:
            game.draw_centre_text("Победил игрок!", game.block_size * 3.5, RED)
            game.is_finished = True


if __name__ == '__main__':
    main()
