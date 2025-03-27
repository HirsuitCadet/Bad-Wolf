import pygame

class TestLevel:
    def __init__(self):
        self.platforms = [
            pygame.Rect(100, 500, 300, 30),  # plateforme principale
            pygame.Rect(450, 400, 100, 30),  # petite en hauteur
            pygame.Rect(600, 300, 150, 30),  # encore plus haut
        ]

    def draw(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, (100, 100, 100), platform)

    def get_platforms(self):
        return self.platforms
