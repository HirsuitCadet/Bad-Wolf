import pygame

def create_jardin():
    background = pygame.image.load("data/fond_jardin.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    platforms = [
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
    return background, platforms