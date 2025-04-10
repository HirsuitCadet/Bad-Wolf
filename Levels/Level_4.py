import pygame

def create_salon():
    background = pygame.image.load("data/fond_salon.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    platforms = [
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
    return background, platforms