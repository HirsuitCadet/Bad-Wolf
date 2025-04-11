import pygame
import random
import gamelib.animals as animals
import gamelib.effects as effects
from Levels.Levels import Levels

class Level6(Levels):
    def __init__(self, level_width, level_height):
        super().__init__()
        self.son_boss.play()
        self.son_spawn_fermier.play()
        self.background = pygame.image.load("data/fond_jardin_boss.png").convert()
        self.background = pygame.transform.scale(self.background, (level_width, level_height))

        self.platforms = [
            pygame.Rect(0, 900, 3150, 50),
            pygame.Rect(350, 700, 120, 20),
            pygame.Rect(550, 800, 180, 20),       
            pygame.Rect(250, 600, 120, 20),       
            pygame.Rect(500, 500, 250, 20),       
            pygame.Rect(800, 400, 100, 20),       
            pygame.Rect(1100, 550, 180, 20),      
            pygame.Rect(1400, 450, 520, 20),      
            pygame.Rect(300, 350, 200, 20),       
            pygame.Rect(1600, 300, 150, 20),      
            pygame.Rect(600, 250, 180, 20),       
            pygame.Rect(1700, 200, 150, 20),
            pygame.Rect(1750, 770, 280, 20),
            pygame.Rect(2250, 670, 180, 20),
            pygame.Rect(2550, 770, 200, 20),   
        ]
        self.shield_powerups = []
        self.animals = self.load_animals(0, level_width)

    def load_animals(self, start_level, end_level,):
        animals_list = []
        animals_list.append(animals.FinalBoss(
            (1200, 700), start_level, end_level,
            self.boss_walk_images, self.boss_walk_images_left, self.boss_charge_images, self.boss_charge_images_left, self.boss_jump_start, self.boss_jump_start_left,
            self.boss_jump_air, self.boss_jump_air_left, self.boss_attack_ground, self.boss_attack_ground_left
        ))
        return animals_list