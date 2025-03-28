import pygame

class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.image = self.right_images[0] if hasattr(self, 'right_images') else pygame.Surface((50, 50))
        self.image.fill((120, 120, 120))
        self.rect = self.image.get_rect(topleft=pos)

        self.jump_speed = 0
        self.jump_accel = 0.6
        self.max_fall_speed = 14
        self.move_speed = 6
        self.jumping = False

        self.max_health = 3
        self.health = 3
        self.hp = self.health
        self.hit_timer = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        self.jump_speed = -13
        self.jumping = True

    def update(self):
        pass