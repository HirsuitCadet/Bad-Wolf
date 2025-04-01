
import pygame

class Animal:
    def __init__(self, pos, right_images, left_images, speed=2, health=1):
        self.right_images = right_images
        self.left_images = left_images
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.direction = 1
        self.health = health
        self.alive = True
        self.frame = 0
        self.frame_timer = 0
        self.flash_timer = 0

    def update(self):
        if not self.alive:
            return

        self.rect.x += self.speed * self.direction

        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1

        self.images = self.right_images if self.direction > 0 else self.left_images

        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
            self.frame_timer = 0

        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1

    def draw(self, screen, offset_x=0, offset_y=0):
        if self.alive:
            screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

    def take_damage(self, amount):
        self.health -= amount
        self.flash_timer = 6
        if self.health <= 0:
            self.alive = False
            self.rect.width = 0
            self.rect.height = 0
            return True
        return False

class Chicken(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=3, health=1)

class Cow(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=1, health=3)

class Pig(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=1, health=2)

class Charger(Animal):
    def __init__(self, pos):
        surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        surface.fill((200, 0, 200))
        super().__init__(pos, [surface], [surface], speed=6, health=3)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, wolf=None):
        if not self.alive:
            return

        # Distance entre le loup et le Charger
        dx = wolf.rect.centerx - self.rect.centerx

        # Si le loup est devant lui et à portée → charge
        if abs(dx) < 500 and ((dx > 0 and self.direction > 0) or (dx < 0 and self.direction < 0)):
            self.speed = 7
        else:
            self.speed = 3

        self.rect.x += self.speed * self.direction

        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1

        self.images = self.right_images if self.direction > 0 else self.left_images
        self.image = self.images[0]

        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1
