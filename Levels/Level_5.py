import pygame

def create_chambre():
    background = pygame.image.load("data/fond_chambre.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    platforms = [
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
    return background, platforms