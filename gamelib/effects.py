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
