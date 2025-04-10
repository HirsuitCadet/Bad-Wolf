import pygame
import gamelib.animals as animals
from Levels import Level

class Level1(Level):
    def __init__(self,level_width,level_height,):
        background = pygame.image.load("data/fond_etable.png").convert()
        background = pygame.transform.scale(background, (level_width, level_height))
        platforms = [
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
        self.load_animals()
        return background, platforms

    def load_animals():
        animals_list = []
            # 1ère tile (x < 1550) : 4 vaches
        animals_list.append(animals.Cow((300, 700), super().right_images_cow, super().left_images_cow))
        animals_list.append(animals.Cow((800, 700), super().right_images_cow, super().left_images_cow))
        animals_list.append(animals.Cow((700, 200), super().right_images_cow, super()left_images_cow))
        animals_list.append(animals.Cow((1200, 700), super().right_images_cow, super().left_images_cow))
            # 2ème tile (x ≥ 1550) : 1 vache + boss vache
        animals_list.append(animals.Cow((1600, 500), super().right_images_cow, super().left_images_cow))
        animals_list.append(
                animals.Charger((1800, 800), super().right_images_charger_walk, super().left_images_charger_walk,
                                super().right_images_charger_charge, super().left_images_charger_charge)
            )