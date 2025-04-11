
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
        self.gravity = 1
        self.fall_speed = 0
        self.on_ground = False


    def update(self, platforms=[]):
        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        # Collision avec le sol
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.fall_speed >= 0 and self.rect.bottom <= plat.bottom:
                    self.rect.bottom = plat.top
                    self.fall_speed = 0
                    self.on_ground = True
                    break
        else:
            self.on_ground = False

        self.timer -= 1


    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

#CODE FAIT AVEC CHATGPT############
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

#########################################

class Shield:
    def __init__(self, pos):
        self.image = pygame.image.load("data/moon.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.timer = 600  # reste visible 10 secondes
        self.gravity = 0.01
        self.fall_speed = 0
        self.on_ground = False

    def update(self, platforms=[]):
        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.fall_speed >= 0 and self.rect.bottom <= plat.bottom:
                    self.rect.bottom = plat.top
                    self.fall_speed = 0
                    self.on_ground = True
                    break
        else:
            self.on_ground = False

        self.timer -= 1

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))
