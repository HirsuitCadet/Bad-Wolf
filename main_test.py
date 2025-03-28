import pygame
from gamelib.sprites import Wolf
from gamelib.animals import *

pygame.init()

# Config 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LEVEL_WIDTH = 1900
LEVEL_HEIGHT = 1000
camera_offset = 0
camera_y = LEVEL_HEIGHT - SCREEN_HEIGHT
CAMERA_MARGIN_Y = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bad Wolf – Test Zone")
clock = pygame.time.Clock()

#Background
background_image = pygame.image.load("data/fond_enclos.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Wolf sprites
Wolf.right_images = [pygame.Surface((50, 50)) for _ in range(6)]
for surf in Wolf.right_images:
    surf.fill((120, 120, 120))

# Chicken sprites
right_images_chicken = [
    pygame.image.load("data/Poule1.png").convert_alpha(),
    pygame.image.load("data/Poule2.png").convert_alpha(),
    pygame.image.load("data/Poule3.png").convert_alpha(),
    pygame.image.load("data/Poule4.png").convert_alpha(),
]
left_images_chicken = [pygame.transform.flip(img, True, False) for img in right_images_chicken]

#Cow sprites
right_images_cow = [
    pygame.image.load("data/Vache1.png").convert_alpha(),
    pygame.image.load("data/Vache2.png").convert_alpha(),
    pygame.image.load("data/Vache3.png").convert_alpha(),
]
left_images_cow = [pygame.transform.flip(img, True, False) for img in right_images_cow]

#Pig sprites
right_images_pig = [
    pygame.image.load("data/Cochon1.png").convert_alpha(),
    pygame.image.load("data/Cochon2.png").convert_alpha(),
    pygame.image.load("data/Cochon3.png").convert_alpha(),
    pygame.image.load("data/Cochon4.png").convert_alpha(),
]
left_images_pig = [pygame.transform.flip(img, True, False) for img in right_images_pig]

# Entities
wolf = Wolf((150, 700))
animals = [
    Chicken((1000, 700), right_images_chicken, left_images_chicken),
    Chicken((1500, 700), right_images_chicken, left_images_chicken),
    Cow((1200, 700), right_images_cow, left_images_cow),
    Cow((1700, 700), right_images_cow, left_images_cow),
    Pig((1300, 700), right_images_pig, left_images_pig),
    Pig((1900, 700), right_images_pig, left_images_pig),
]

# Plateformes
platforms = [
    pygame.Rect(0, 800, 1900, 50),
    pygame.Rect(200, 700, 120, 20),
    pygame.Rect(400, 600, 100, 20),
    pygame.Rect(600, 500, 100, 20),
    pygame.Rect(850, 700, 150, 20),
    pygame.Rect(1050, 600, 100, 20),
    pygame.Rect(1250, 500, 120, 20),
    pygame.Rect(1450, 400, 120, 20),
    pygame.Rect(1650, 650, 100, 20),
    pygame.Rect(1750, 550, 100, 20),
    pygame.Rect(1800, 450, 80, 20)
]

# HUD
heart_image = pygame.Surface((30, 30))
heart_image.fill((255, 0, 0))

running = True
while running:
    screen.fill((135, 206, 235))
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        dx = -wolf.move_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = wolf.move_speed
    if (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_w] or keys[pygame.K_UP]) and not wolf.jumping:
        wolf.jump()

    wolf.move(dx, 0)
    wolf.jump_speed += wolf.jump_accel
    if wolf.jump_speed > wolf.max_fall_speed:
        wolf.jump_speed = wolf.max_fall_speed
    wolf.move(0, wolf.jump_speed)



    # Collisions plateformes
    wolf.jumping = True
    for platform in platforms:
        if wolf.rect.colliderect(platform) and wolf.jump_speed >= 0:
            wolf.rect.bottom = platform.top
            wolf.jump_speed = 0
            wolf.jumping = False
            break

    # Interactions avec animaux
    for animal in animals:
        animal.update()
        if animal.alive and wolf.rect.colliderect(animal.rect):
            if wolf.rect.bottom <= animal.rect.top + 10 and wolf.jump_speed > 0:
                animal.take_damage(1)
                wolf.jump_speed = -8
            else:
                if wolf.hit_timer <= 0:
                    wolf.hp -= 1
                    wolf.hit_timer = 60
                    if wolf.hp <= 0:
                        running = False
        else:
            wolf.hit_timer = max(wolf.hit_timer - 1, 0)

    # Scroll horizontal
    if wolf.rect.right > camera_offset + SCREEN_WIDTH:
        if camera_offset + SCREEN_WIDTH < LEVEL_WIDTH:
            camera_offset += SCREEN_WIDTH
            wolf.rect.left = camera_offset
    if wolf.rect.left < camera_offset:
        if camera_offset > 0:
            camera_offset -= SCREEN_WIDTH
            wolf.rect.right = camera_offset + SCREEN_WIDTH

    # Scroll vertical
    if wolf.rect.top < camera_y + CAMERA_MARGIN_Y:
        camera_y = max(0, wolf.rect.top - CAMERA_MARGIN_Y)
    elif wolf.rect.bottom > camera_y + SCREEN_HEIGHT - CAMERA_MARGIN_Y:
        camera_y = min(LEVEL_HEIGHT - SCREEN_HEIGHT, wolf.rect.bottom - SCREEN_HEIGHT + CAMERA_MARGIN_Y)

    # DESSIN
    for plat in platforms:
        pygame.draw.rect(screen, (100, 100, 100), plat.move(-camera_offset, -camera_y))

    for animal in animals:
        animal.draw(screen, camera_offset, camera_y)

    wolf.update()
    screen.blit(wolf.image, wolf.rect.move(-camera_offset, -camera_y))

    for i in range(wolf.hp):
        screen.blit(heart_image, (10 + i * 35, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()