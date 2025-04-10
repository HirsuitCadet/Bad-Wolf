import pygame
import gamelib.animals as animals
from Levels.Levels import Levels

class Level5(Levels):
    def __init__(self, level_width, level_height):
        super().__init__()

        self.background = pygame.image.load("data/fond_chambre.png").convert()
        self.background = pygame.transform.scale(self.background, (level_width, level_height))

        self.platforms = [
            pygame.Rect(0, 900, 3100, 50),
            pygame.Rect(250, 800, 180, 20),
            pygame.Rect(500, 700, 300, 20),      
            pygame.Rect(200, 650, 150, 20),       
            pygame.Rect(450, 550, 120, 20),       
            pygame.Rect(750, 450, 180, 20),       
            pygame.Rect(1100, 600, 100, 20),      
            pygame.Rect(1400, 500, 200, 20),      
            pygame.Rect(300, 400, 150, 20),       
            pygame.Rect(1600, 350, 120, 20),      
            pygame.Rect(600, 300, 180, 20),       
            pygame.Rect(1700, 250, 150, 20),
            pygame.Rect(1700, 740, 220, 25),
            pygame.Rect(2150, 690, 220, 25),
            pygame.Rect(2550, 740, 220, 25),
            pygame.Rect(2850, 790, 200, 25), 
        ]

        self.animals = self.load_animals(0, level_width)

    def load_animals(self, start_level, end_level,):
        animals_list = []
        animals_list.append(animals.BossFemme(
            (1200, 700), start_level, end_level,
            self.femme_walk_images, self.femme_walk_images_left,
            self.femme_throw_images, self.femme_throw_images_left
        ))
        return animals_list