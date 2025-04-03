import pygame
import random
from gamelib.sprites import Wolf
from gamelib.animals import *
from gamelib.items import Heal, SpeedBoost
from gamelib.effects import BloodEffect

pygame.init()

# Config 
SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 800
LEVEL_WIDTH = 1900
LEVEL_HEIGHT = 1000
camera_offset = 0
camera_y = LEVEL_HEIGHT - SCREEN_HEIGHT
CAMERA_MARGIN_Y = 200
camera_shake = 0
game_over = False


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bad Wolf – Test Zone")
clock = pygame.time.Clock()

#Background
background_image = pygame.image.load("data/fond_enclos.png").convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Wolf sprites
left_images_wolf = [
    pygame.image.load("data/Loup1.png").convert_alpha(),
    pygame.image.load("data/Loup2.png").convert_alpha(),
    pygame.image.load("data/Loup3.png").convert_alpha(),
    pygame.image.load("data/Loup4.png").convert_alpha(),
    pygame.image.load("data/Loup5.png").convert_alpha(),
    pygame.image.load("data/Loup6.png").convert_alpha(),
    pygame.image.load("data/Loup7.png").convert_alpha(),
    pygame.image.load("data/Loup8.png").convert_alpha(),
]
right_images_wolf = [pygame.transform.flip(img, True, False) for img in left_images_wolf]

Wolf.right_images = right_images_wolf
Wolf.left_images = left_images_wolf

wolf_sit_right = pygame.image.load("data/Loup_sit.png").convert_alpha()
wolf_sit_left = pygame.transform.flip(wolf_sit_right, True, False)

Wolf.sit_image_right = wolf_sit_right
Wolf.sit_image_left = wolf_sit_left


# Chicken sprites
right_images_chicken = [
    pygame.image.load("data/Poule1.png").convert_alpha(),
    pygame.image.load("data/Poule2.png").convert_alpha(),
    pygame.image.load("data/Poule3.png").convert_alpha(),
    pygame.image.load("data/Poule4.png").convert_alpha(),
]
left_images_chicken = [pygame.transform.flip(img, True, False) for img in right_images_chicken]

# Rooster boss
rooster_boss = RoosterBoss((1000, 700), [pygame.Surface((80, 80))], [pygame.Surface((80, 80))])
rooster_boss.right_images[0].fill((255, 255, 255))
rooster_boss.left_images[0].fill((255, 255, 255))

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
    Pig((1500, 700), right_images_pig, left_images_pig),
    Pig((1900, 700), right_images_pig, left_images_pig),
    Charger((1600, 700)),
    Dog((800, 700)),
]
animals.append(rooster_boss)
heals = []
speedboosts = []
speedboost_timer = 0
speedboosts.append(SpeedBoost((600, 700)))
bloods = []
egg_explosions = []
frame_counter = 0

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
# === ÉCRAN DE DÉMARRAGE ===
title_font = pygame.font.Font(None, 80)
info_font = pygame.font.Font(None, 40)

title_text = title_font.render("BAD WOLF", True, (255, 255, 255))
prompt_text = info_font.render("Appuie sur ESPACE pour commencer", True, (200, 200, 200))

waiting = True
while waiting:
    screen.fill((0, 0, 0))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting = False

    pygame.display.flip()
    clock.tick(60)

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
        wolf.direction = -1
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = wolf.move_speed
        wolf.direction = 1
    if (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_w] or keys[pygame.K_UP]) and not wolf.jumping:
        wolf.jump()

    wolf.move(dx, 0)
    wolf.jump_speed += wolf.jump_accel
    if wolf.jump_speed > wolf.max_fall_speed:
        wolf.jump_speed = wolf.max_fall_speed
    previous_bottom = wolf.rect.bottom
    wolf.move(0, wolf.jump_speed)

    # Collisions plateformes
    wolf.jumping = True
    for platform in platforms:
        if wolf.rect.colliderect(platform):
            if wolf.jump_speed > 0 and previous_bottom <= platform.top:
                wolf.rect.bottom = platform.top
                wolf.jump_speed = 0
                wolf.jumping = False
                break

    # Interactions avec animaux
    
    for animal in animals:
        if isinstance(animal, Charger):
            animal.update(wolf)
        elif isinstance(animal, Dog):
            animal.update(wolf, platforms)
        else:
            animal.update(platforms)

        if not animal.alive:
            continue

        if wolf.rect.colliderect(animal.rect):
            # Attaque par le haut (toujours possible)
            if wolf.rect.bottom <= animal.rect.top + 10 and wolf.jump_speed > 0:
                # Si l'animal meurt
                if animal.take_damage(1):
                    # Si on est dans les 20% de chance
                    if random.randint(1,100) <= 20:
                        # Drop un os avec de la viande au bout 
                        heals.append(Heal(animal.rect.center))
                    bloods.append(BloodEffect(animal.rect.center))
                wolf.jump_speed = -8
            
            elif wolf.hit_timer <= 0:
                # Collision dangereuse seulement si pas invincible
                wolf.take_damage(animal)

                # Knockback si c'est un Charger
                if isinstance(animal, Charger):
                    camera_shake = 50  # durée de la secousse en frames

                    wolf.jump_speed = -20
                    wolf.jumping = True

                if wolf.hp <= 0:
                    game_over = True
                    running = False


    # Affichage des power-ups

    # Affichage des heals
    for heal in heals[:]:
        heal.update()
        heal.draw(screen, camera_offset, camera_y)

        # Ramassage
        if wolf.rect.colliderect(heal.rect):
            wolf.hp = min(wolf.hp + 1, wolf.max_health)
            heals.remove(heal)

        # Disparition naturelle
        elif heal.timer <= 0:
            heals.remove(heal)

    
    # Affichage et ramassage des SpeedBoosts
    for boost in speedboosts[:]:
        boost.update()
        boost.draw(screen, camera_offset, camera_y)

        # Ramassage
        if wolf.rect.colliderect(boost.rect):
            speedboosts.remove(boost)
            speedboost_timer = 600  # 10 secondes
            wolf.move_speed = 10
            wolf.jump = lambda: setattr(wolf, 'jump_speed', -20) or setattr(wolf, 'jumping', True)

        elif boost.timer <= 0:
            speedboosts.remove(boost)

    # Fin du boost après 10 secondes
    if speedboost_timer > 0:
        speedboost_timer -= 1
        if speedboost_timer == 0:
            wolf.move_speed = 6
            wolf.jump = lambda: setattr(wolf, 'jump_speed', -13) or setattr(wolf, 'jumping', True)

# Affichage des effets
    for blood in bloods[:]:
        blood.update()
        blood.draw(screen, camera_offset, camera_y)
        if blood.finished:
            bloods.remove(blood)


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

    # Appliquer la secousse de caméra si active
    shake_x = random.randint(-5, 5) if camera_shake > 0 else 0
    shake_y = random.randint(-5, 5) if camera_shake > 0 else 0

    camera_offset += shake_x
    camera_y += shake_y

    if camera_shake > 0:
        camera_shake -= 1

    screen.blit(wolf.image, wolf.rect.move(-camera_offset, -camera_y))
    
    rooster_boss.update(wolf.rect, wolf, egg_explosions)
    rooster_boss.draw(screen, camera_offset, camera_y)

    for i in range(wolf.hp):
        screen.blit(heart_image, (10 + i * 35, 10))

    frame_counter += 1
    if wolf.hp <= 0:
        running = False

    # Affichage des effets d'explosion d'œufs
    for img, pos, delay in egg_explosions[:]:
        if frame_counter >= delay:
            screen.blit(img, (pos[0] - img.get_width() // 2 - camera_offset,
                            pos[1] - img.get_height() // 2 - camera_y))
            egg_explosions.remove((img, pos, delay))

    pygame.display.flip()
    clock.tick(60)
# === ÉCRAN DE GAME OVER ===
if game_over:
    title_font = pygame.font.Font(None, 80)
    info_font = pygame.font.Font(None, 40)

    over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    retry_text = info_font.render("Appuie sur ÉCHAP pour quitter", True, (255, 255, 255))

    waiting = True
    while waiting:
        screen.fill((0, 0, 0))
        screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

        pygame.display.flip()
        clock.tick(60)

pygame.quit()

