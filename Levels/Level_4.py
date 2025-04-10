import pygame
import gamelib.animals as animals
from Levels.Levels import Levels

class Level4(Levels):
    def __init__(self, level_width, level_height):
        super().__init__()

        self.background = pygame.image.load("data/fond_salon.png").convert()
        self.background = pygame.transform.scale(self.background, (level_width, level_height))

        self.platforms = [
            pygame.Rect(0, 900, 3100, 50),
            pygame.Rect(50, 800, 180, 20),
            pygame.Rect(500, 700, 300, 20),       
            pygame.Rect(200, 700, 180, 20),       
            pygame.Rect(450, 600, 120, 20),       
            pygame.Rect(750, 500, 150, 20),       
            pygame.Rect(1100, 650, 100, 20),      
            pygame.Rect(1400, 550, 200, 20),      
            pygame.Rect(300, 450, 150, 20),       
            pygame.Rect(1600, 400, 120, 20),      
            pygame.Rect(600, 350, 180, 20),       
            pygame.Rect(1700, 300, 150, 20),
            pygame.Rect(1650, 630, 300, 25),
            pygame.Rect(2050, 670, 250, 25),
            pygame.Rect(2400, 730, 300, 25),
            pygame.Rect(2200, 830, 300, 25), 
        ]

        self.animals = self.load_animals(0, level_width)

    def load_animals(self, start_level, end_level,):
        animals_list = []
        animals_list.append(animals.Dog((300, 350), start_level, end_level, self.right_walk_dog, self.left_walk_dog,
                                            self.dog_jump_prep, self.dog_jump_prep_left,
                                            self.dog_jump_air, self.dog_jump_air_left))
        animals_list.append(animals.Dog((500, 250), start_level, end_level, self.right_walk_dog, self.left_walk_dog,
                                            self.dog_jump_prep, self.dog_jump_prep_left,
                                            self.dog_jump_air, self.dog_jump_air_left))
        animals_list.append(animals.Dog((1700, 700), start_level, end_level, self.right_walk_dog, self.left_walk_dog,
                                            self.dog_jump_prep, self.dog_jump_prep_left,
                                            self.dog_jump_air, self.dog_jump_air_left))
        animals_list.append(animals.Dog((100, 700), start_level, end_level, self.right_walk_dog, self.left_walk_dog,
                                            self.dog_jump_prep, self.dog_jump_prep_left,
                                            self.dog_jump_air, self.dog_jump_air_left))
        return animals_list