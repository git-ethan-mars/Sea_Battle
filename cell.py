import pygame


class Cell(pygame.sprite.Sprite):
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'C:/Users/1290723/PycharmProjects/pythonProject/images/cell.jpg')
        # self.image.set_colorkey((0, 0, 0))
        # self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (Cell.WIDTH / 2, Cell.HEIGHT / 2)

    def update(self):
        pass
        # self.rect.x += 5

        # if self.rect.left > Cell.WIDTH:
        #     self.rect.right = 0
