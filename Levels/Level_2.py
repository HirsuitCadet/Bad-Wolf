import pygame

def create_enclos():
    background = pygame.image.load("data/fond_enclos.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    platforms = [
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
    return background, platforms