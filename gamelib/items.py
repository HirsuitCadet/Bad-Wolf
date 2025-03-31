import pygame

class Heal:
    def __init__(self, pos):
        self.image = pygame.image.load("data/heal.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.timer = 300

    def update(self):
        self.timer -= 1

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))
