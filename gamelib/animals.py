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

    def update(self):
        if not self.alive:
            return

        # Mouvement
        self.rect.x += self.speed * self.direction

        # Collision avec les bords de la map
        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1

        # Choisir images selon la direction
        self.images = self.right_images if self.direction > 0 else self.left_images

        # Animation
        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
            self.frame_timer = 0

    def draw(self, screen, offset_x=0, offset_y=0):
        if self.alive:
            screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False


class Chicken(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=2, health=1)