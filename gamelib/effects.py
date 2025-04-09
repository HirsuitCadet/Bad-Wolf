import pygame
import math

class BloodEffect:
    def __init__(self, pos):
        self.images = [
            pygame.image.load(f"data/blood{i}.png").convert_alpha()
            for i in range(1, 5) 
        ]
        self.frame = 0
        self.frame_timer = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=pos)
        self.finished = False

    def update(self):
        self.frame_timer += 1
        if self.frame_timer >= 5:  # vitesse animation
            self.frame += 1
            if self.frame >= len(self.images):
                self.finished = True
            else:
                self.image = self.images[self.frame]
            self.frame_timer = 0

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

# Code fait avec ChatGPT
#################################################
class EggProjectile:
    def __init__(self, pos, direction, explosion_frames, frame_duration=6):
        self.image = pygame.image.load("data/oeuf.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = 6 * direction[0]
        self.speed_y = 5 * direction[1]
        self.gravity = 0.3
        self.exploding = False
        self.finished = False

        # Explosion
        self.explosion_frames = explosion_frames
        self.frame_duration = frame_duration
        self.frame_index = 0
        self.timer = 0

    def update(self):
        if not self.exploding:
            self.rect.x += self.speed_x
            self.speed_y += self.gravity
            self.rect.y += int(self.speed_y)
        else:
            self.timer += 1
            if self.timer >= self.frame_duration:
                self.timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.explosion_frames):
                    self.finished = True

    def explode(self):
        self.exploding = True
        self.frame_index = 0
        self.timer = 0
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0

    def draw(self, screen, offset_x, offset_y):
        if self.exploding and not self.finished:
            frame = self.explosion_frames[self.frame_index]
            screen.blit(frame, self.rect.move(-offset_x, -offset_y))
        elif not self.exploding:
            screen.blit(self.image, self.rect.move(-offset_x, -offset_y))
#################################################

#CODE FAIT AVEC CHATGPT######################################
class HomingProjectile:
    def __init__(self, start_pos, target_pos):
        self.original_image = pygame.image.load("data/claquette.png").convert_alpha()
        self.image = self.original_image.copy()
        self.angle = 0

        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 8
        self.target = target_pos
        self.lifetime = 600
        self.dir_x = 0
        self.dir_y = 0

    def update(self, target_rect):
        # Réoriente légèrement vers la cible
        dx = target_rect.centerx - self.rect.centerx
        dy = target_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        dx /= dist
        dy /= dist

        smooth_factor = 0.05
        self.dir_x += (dx - self.dir_x) * smooth_factor
        self.dir_y += (dy - self.dir_y) * smooth_factor

        self.rect.x += int(self.dir_x * self.speed)
        self.rect.y += int(self.dir_y * self.speed)

        self.angle = (self.angle + 15) % 360  # vitesse de rotation
        self.lifetime -= 1

    def draw(self, screen, offset_x, offset_y):
        # Clignote dans les 3 dernières secondes (180 frames)
        if self.lifetime > 180 or (self.lifetime // 10) % 2 == 0:
            rotated = pygame.transform.rotate(self.original_image, self.angle)
            new_rect = rotated.get_rect(center=self.rect.center)
            screen.blit(rotated, new_rect.move(-offset_x, -offset_y))

#############################################################