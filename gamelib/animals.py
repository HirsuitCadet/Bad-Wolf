
import pygame
import random
import time

LEVEL_WIDTH = 1900

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
        self.gravity = 1
        self.fall_speed = 0
        self.on_ground = False


    def update(self,platforms):
        if not self.alive:
            return

        self.rect.x += self.speed * self.direction

        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.fall_speed >= 0 and self.rect.bottom <= plat.bottom:
                    self.rect.bottom = plat.top
                    self.fall_speed = 0
                    self.on_ground = True

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


class EggProjectile:
    def __init__(self, pos, direction):
        self.image = pygame.image.load("data/oeuf.webp").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = 6 * direction[0]
        self.speed_y = 5 * direction[1]
        self.gravity = 0.3 if direction[1] != 0 else 0
        self.alive = True

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_y += self.gravity

        if self.rect.right < 0 or self.rect.left > 2000 or self.rect.top > 1200:
            self.alive = False

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

class RoosterBoss(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images)
        self.health = 3
        self.speed = 2.5
        self.normal_speed = 2.5
        self.flee_speed = 10  # Vitesse pendant la fuite
        self.flee_timer = 0
        self.projectiles = []
        self.shooting = False
        self.shoot_timer = 0
        self.pre_attack_duration = 15
        self.shoot_direction = (0, 0)
        self.charge_image = pygame.Surface((80, 80))
        self.charge_image.fill((255, 200, 200))

        self.shoot_interval = random.randint(60, 120)
        self.flash_timer = 0
        self.invincibility_timer = 0
        self.last_damage_frame = -1000

        self.explosion_frames = [
            pygame.image.load("data/oeuf1.png").convert_alpha(),
            pygame.image.load("data/oeuf2.png").convert_alpha(),
            pygame.image.load("data/oeuf3.png").convert_alpha(),
            pygame.image.load("data/oeuf4.png").convert_alpha()
        ]

    def update(self, wolf_rect=None, wolf=None, effects=None):
        if not self.alive:
            for egg in self.projectiles:
                egg.update()
            self.projectiles = [e for e in self.projectiles if e.alive]
            return

        self.speed = self.flee_speed if self.flee_timer > 0 else self.normal_speed
        self.rect.x += self.speed * self.direction

        if self.flee_timer > 0:
            self.flee_timer -= 1
        elif random.random() < 0.01:
            self.direction *= -1

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH
            self.direction = -1

        self.images = self.right_images if self.direction > 0 else self.left_images

        if not self.shooting:
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

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        if self.shooting:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                self.projectiles.append(EggProjectile(self.rect.center, self.shoot_direction))
                self.shooting = False
        else:
            self.shoot_interval -= 1
            if self.shoot_interval <= 0:
                prob_map = {3: 30, 2: 60, 1: 90}
                shoot_chance = prob_map.get(self.health, 90)
                alea = random.randint(1, 100)
                if alea <= shoot_chance:
                    if wolf_rect and abs(self.rect.centerx - wolf_rect.centerx) < 400:
                        dir_x = 1 if wolf_rect.centerx > self.rect.centerx else -1
                        dir_y = random.choice([0, -1])
                        self.shoot_direction = (dir_x, dir_y)
                        self.shooting = True
                        self.shoot_timer = self.pre_attack_duration
                cooldown_map = {3: 90, 2: 60, 1: 30}
                base_cd = cooldown_map.get(self.health, 30)
                self.shoot_interval = base_cd + random.randint(0, 20)

        for egg in self.projectiles[:]:
            egg.update()
            if wolf and egg.rect.colliderect(wolf.rect):
                egg.alive = False
                if wolf.hit_timer <= 0:
                    wolf.hp -= 1
                    wolf.hit_timer = 60
                    if effects is not None:
                        for i, frame in enumerate(self.explosion_frames):
                            effects.append((frame, egg.rect.center, 15))
        self.projectiles = [e for e in self.projectiles if e.alive]

    def take_damage(self, amount, wolf_rect=None, current_frame=None):
        if self.invincibility_timer > 0:
            return False

        if current_frame is not None and current_frame - self.last_damage_frame < 20:
            return False

        self.last_damage_frame = current_frame if current_frame is not None else 0

        self.health -= amount
        self.flash_timer = 6
        self.invincibility_timer = 30
        self.flee_timer = 20

        if self.health <= 0:
            self.alive = False
            return True

        if wolf_rect:
            if wolf_rect.centerx < self.rect.centerx:
                self.direction = 1
            else:
                self.direction = -1

        return False

    def draw(self, screen, offset_x, offset_y):
        if self.alive:
            image = self.charge_image if self.shooting else self.image
            screen.blit(image, self.rect.move(-offset_x, -offset_y))
        for egg in self.projectiles:
            egg.draw(screen, offset_x, offset_y)