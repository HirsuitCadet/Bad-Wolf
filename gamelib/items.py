
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

class SpeedBoost:
    def __init__(self, pos):
        self.image = pygame.image.load("data/power_up_cri.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.timer = 600  # 10 secondes d'apparition

    def update(self):
        self.timer -= 1

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

class MovingPlatform:
    def __init__(self, x, y, width, height, dx=2, range_x=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.start_x = x
        self.dx = dx
        self.range_x = range_x

    def update(self):
        self.rect.x += self.dx
        if abs(self.rect.x - self.start_x) >= self.range_x:
            self.dx *= -1

    def draw(self, screen, offset_x, offset_y):
        pygame.draw.rect(screen, (150, 100, 100), self.rect.move(-offset_x, -offset_y))  # couleur différente
