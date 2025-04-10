import pygame
import gamelib.animals as animals
from Levels.Levels import Levels

class Level2(Levels):
    def __init__(self, level_width, level_height):
        super().__init__()

        self.background = pygame.image.load("data/fond_enclos.png").convert()
        self.background = pygame.transform.scale(self.background, (level_width, level_height))

        self.platforms = [
            pygame.Rect(0, 900, 3100, 50), 
            pygame.Rect(250, 800, 180, 20),       
            pygame.Rect(200, 650, 150, 20),       
            pygame.Rect(450, 550, 120, 20),       
            pygame.Rect(700, 700, 100, 20),       
            pygame.Rect(900, 500, 180, 20),       
            pygame.Rect(1200, 600, 120, 20),      
            pygame.Rect(1500, 450, 150, 20),      
            pygame.Rect(1700, 550, 100, 20),      
            pygame.Rect(350, 400, 200, 20),       
            pygame.Rect(1600, 350, 150, 20),
            pygame.Rect(1700, 780, 180, 20),
            pygame.Rect(1950, 740, 150, 20),
            pygame.Rect(2200, 690, 200, 20),
            pygame.Rect(2500, 740, 130, 20),
            pygame.Rect(2800, 780, 160, 20),  
        ]

        self.animals = self.load_animals(0, level_width)

    def load_animals(self, start_level, end_level,):
        animals_list = []
        # 1ère tile : quelques vaches et cochons
        animals_list.append(animals.Pig((400, 300), start_level, end_level, self.right_images_pig, self.left_images_pig))
        animals_list.append(animals.Pig((800, 700), start_level, end_level, self.right_images_pig, self.left_images_pig))
        animals_list.append(animals.Cow((900, 400), start_level, end_level, self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Cow((1100, 700), start_level, end_level, self.right_images_cow, self.left_images_cow))

        # 2ème tile : boss cochon + cochon
        animals_list.append(
            animals.PigBoss((1600, 700), start_level, end_level, self.right_walk_pigboss, self.left_walk_pigboss,
                            self.right_charge_pigboss, self.left_charge_pigboss)
        )
        animals_list.append(animals.Pig((1750, 700), start_level, end_level, self.right_images_cow, self.left_images_cow))
        return animals_list