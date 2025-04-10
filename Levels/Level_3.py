import pygame
import gamelib.animals as animals
from Levels.Levels import Levels

class Level3(Levels):
    def __init__(self, level_width, level_height):
        super().__init__()

        self.background = pygame.image.load("data/fond_jardin.png").convert()
        self.background = pygame.transform.scale(self.background, (level_width, level_height))

        self.platforms = [
            pygame.Rect(0, 900, 3100, 50),
            pygame.Rect(0, 900, 3000, 50),
            pygame.Rect(250, 800, 180, 20),        
            pygame.Rect(200, 650, 180, 20),       
            pygame.Rect(450, 550, 120, 20),       
            pygame.Rect(750, 450, 150, 20),       
            pygame.Rect(1100, 600, 100, 20),      
            pygame.Rect(1400, 500, 200, 20),      
            pygame.Rect(300, 400, 150, 20),       
            pygame.Rect(1600, 350, 120, 20),      
            pygame.Rect(600, 300, 180, 20),       
            pygame.Rect(1700, 250, 150, 20),
            pygame.Rect(1650, 770, 180, 20),
            pygame.Rect(1850, 720, 150, 20),
            pygame.Rect(2100, 670, 180, 20),
            pygame.Rect(2350, 720, 160, 20),
            pygame.Rect(2600, 770, 200, 20),
        ]

        self.animals = self.load_animals(0, level_width)

    def load_animals(self, start_level, end_level,):
        animals_list = []
        # 1ère tile : poulets, cochons, vaches
        animals_list.append(animals.Chicken((400, 300), start_level, end_level, self.right_images_chicken, self.left_images_chicken))
        animals_list.append(animals.Pig((700, 200), start_level, end_level, self.right_images_pig, self.left_images_pig))
        animals_list.append(animals.Cow((1000, 700), start_level, end_level, self.right_images_cow, self.left_images_cow))

        # 2ème tile : Boss poulet + 1 de chaque
        rooster_boss = animals.RoosterBoss((1600, 700), start_level, end_level, self.rooster_walk_right, self.rooster_walk_left,
                                           self.rooster_charge_right, self.rooster_charge_left, self.rooster_shoot_right, self.rooster_shoot_left)
        animals_list.append(rooster_boss)
        animals_list.append(animals.Cow((1800, 700), start_level, end_level, self.right_images_cow, self.left_images_cow))
        animals_list.append(animals.Pig((1900, 700), start_level, end_level, self.right_images_pig, self.left_images_pig))
        animals_list.append(animals.Chicken((1700, 700), start_level, end_level, self.right_images_chicken, self.left_images_chicken))
        return animals_list