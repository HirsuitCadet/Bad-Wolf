import pygame

def create_jardin_boss():
    background = pygame.image.load("data/fond_jardin_boss.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    platforms = [
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
    return background, platforms

