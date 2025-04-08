import pygame

class BloodEffect:
    def __init__(self, pos):
        self.images = [
            pygame.image.load(f"data/blood{i}.png").convert_alpha()
            for i in range(1, 5)  # sang1.png à sang4.png
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