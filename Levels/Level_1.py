import pygame
import gamelib.animals as animals
from Levels.Levels import Levels

class Level1(Levels):
    def __init__(self, level_width, level_height):
        super().__init__()

        self.background = pygame.image.load("data/fond_etable.png").convert()
        self.background = pygame.transform.scale(self.background, (level_width, level_height))

        self.platforms = [
            pygame.Rect(0, 900, 3100, 50),
            pygame.Rect(350, 800, 380, 20),     
            pygame.Rect(250, 700, 180, 20),       
            pygame.Rect(500, 600, 120, 20),       
            pygame.Rect(800, 500, 150, 20),       
            pygame.Rect(1100, 650, 100, 20),      
            pygame.Rect(1400, 550, 200, 20),      
            pygame.Rect(300, 450, 150, 20),       
            pygame.Rect(1600, 400, 120, 20),      
            pygame.Rect(600, 350, 180, 20),       
            pygame.Rect(1700, 300, 150, 20),
            pygame.Rect(1700, 760, 160, 20),
            pygame.Rect(1800, 850, 120, 20),
            pygame.Rect(2000, 740, 180, 20),
            pygame.Rect(2150, 700, 140, 20),
            pygame.Rect(2350, 760, 100, 20),
        ]

        self.animals = self.load_animals(0, level_width)

    def load_animals(self, start_level, end_level):
        animals_list = []
        animals_list.append(animals.Cow((300, 700), start_level, end_level, self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Cow((800, 700), start_level, end_level, self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Cow((700, 200), start_level, end_level,self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Cow((1200, 700), start_level, end_level,self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Cow((1600, 500), start_level, end_level,self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Charger(
            (1800, 785), start_level, end_level,
            self.right_images_charger_walk, self.left_images_charger_walk,
            self.right_images_charger_charge, self.left_images_charger_charge
        ))
        return animals_list