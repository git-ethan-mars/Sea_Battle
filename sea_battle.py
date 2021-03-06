import pygame
from game import Game, load_file
from shipsSet import is_on_field
from players import Player, Computer
from settings import *


def main():
    pygame.init()
    pygame.display.set_caption("Морской бой")
    game = Game()
    new_game_button, fast_game_button, \
    options_button, exit_button = game.draw_menu()
    working = True
    menu_button = None
    computer_mode_button = None
    start_game_button = None
    while working:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif game.is_place and game.player.is_ships_placed(load_file()):
                start_game_button = game.draw_centre_button("Начать игру",
                                                            GREEN,
                                                            offset_y=-500,
                                                            font_size=block_size)
            if event.type == pygame.MOUSEBUTTONDOWN and (
                    event.button == 1 or event.button == 3):
                if game.ship_to_replace is not None and game.is_place:
                    game.change_ship_position(Player.get_cell(event.pos),
                                              len(game.ship_to_replace),
                                              event.button == 1)
                    game.ship_to_replace = None
                    continue
                for ship in game.player.data_ships.ships:
                    for cell in ship:
                        if Player.get_cell(
                                event.pos) == cell and game.is_place:
                            game.ship_to_replace = ship
                            game.color_ship(ship, GREEN)
                            break
                if start_game_button is not None and start_game_button.collidepoint(
                        event.pos):
                    game.player.data_ships.ships_copy = game.player.data_ships.ships[
                                                        :]
                    start_game_button = None
                    game.draw_fast_game()
                    menu_button = game.draw_back_to_menu_button()
                if (not game.is_menu or game.is_options) \
                        and menu_button.collidepoint(event.pos):
                    game = Game(game.is_smart)
                    start_game_button = None
                    new_game_button, fast_game_button, \
                    options_button, exit_button = game.draw_menu()
                elif game.is_menu and not game.is_options and new_game_button.collidepoint(
                        event.pos):
                    menu_button = game.draw_new_game()
                elif game.is_place and start_game_button is None and any(
                        [rect.collidepoint(event.pos) for rect in
                         game.rect_to_place]):
                    for rect in game.rect_to_place:
                        if rect.collidepoint(event.pos):
                            game.mark_current_ship(rect)
                            game.rect_taken = rect
                elif game.is_place and start_game_button is None and game.rect_taken is not None and game.ship_to_replace is None:
                    cell = Player.get_cell(event.pos)
                    if is_on_field(cell):
                        game.place_ship_manually(cell, game.rect_taken.w,
                                                 game.rect_taken.h,
                                                 event.button == 1)
                elif game.is_menu and not game.is_options and \
                        (fast_game_button.collidepoint(
                            event.pos) or new_game_button.collidepoint(
                            event.pos)):
                    menu_button = game.draw_fast_game()
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
                    player_shoot_status = game.player.shoot(game.computer,
                                                            Computer.get_cell(
                                                                event.pos))
                    if player_shoot_status is not None:
                        game.draw_hit(*player_shoot_status)
                        if not player_shoot_status[3]:
                            computer_shoot_status = game.computer.shoot(
                                game.player, game.computer, game.is_smart)
                            game.draw_hit(*computer_shoot_status)
                            while computer_shoot_status[3]:
                                game.player.dead_ships += 1
                                computer_shoot_status = game.computer.shoot(
                                    game.player, game.computer,
                                    game.is_smart)
                                game.draw_hit(*computer_shoot_status)
                        else:
                            game.computer.dead_ships += 1
        if not game.is_menu and game.player.dead_ships == game.ships_amount != 0:
            game.draw_centre_text("Победил компьютер!", block_size * 2.5,
                                  RED)
            game.is_finished = True
        elif not game.is_menu and \
                game.computer.dead_ships == game.ships_amount != 0:
            game.draw_centre_text("Победил игрок!", block_size * 3.5, RED)
            game.is_finished = True


if __name__ == '__main__':
    main()
