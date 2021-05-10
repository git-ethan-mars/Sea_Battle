import ships

block_size = 45
left_margin = 90
top_margin = 72


class Player:
    def __init__(self):
        self.ships = ships.Ships()
        self.enemy_left = left_margin + block_size * 15
        self.enemy_top = top_margin

    def shoot(self, position, ships_set):
        x, y = ((position[0] - self.enemy_left) // block_size + 1, (position[1] - self.enemy_top) // block_size + 1)
        if ships.Ships.is_on_field((x, y)):
            if (x, y) in [j for i in ships_set for j in i]:
                print("Попал")
            else:
                print("Мимо")
