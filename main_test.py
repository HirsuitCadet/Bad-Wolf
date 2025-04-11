import pygame
import random
import math
import gamelib.animals as animals
from Levels.Levels import Levels
from Levels.Level_1 import Level1
from Levels.Level_2 import Level2
from Levels.Level_3 import Level3
from Levels.Level_4 import Level4
from Levels.Level_5 import Level5
from Levels.Level_6 import Level6
from gamelib.sprites import Wolf
from gamelib.items import Heal, SpeedBoost, MovingPlatform
from gamelib.effects import BloodEffect

pygame.init()

# Config 
SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 800
LEVEL_WIDTH = 3100
LEVEL_HEIGHT = 1000
camera_offset = 0
camera_y = LEVEL_HEIGHT - SCREEN_HEIGHT
CAMERA_MARGIN_Y = 200
camera_shake = 0
game_over = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bad Wolf – Test Zone")
clock = pygame.time.Clock()

level = Level1(LEVEL_WIDTH, LEVEL_HEIGHT)
platforms = level.platforms
liste_animals = level.animals
background_image = pygame.transform.scale(level.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
level_number = 1

# Entities
wolf = Wolf((150, 700))

heals = []
speedboosts = []
speedboost_timer = 0
bloods = []
egg_explosions = []
frame_counter = 0

#moving_platforms = [
 #   MovingPlatform(400, 600, 120, 20, dx=2, range_x=200) 
#]
# HUD

heart_image = pygame.image.load("data/heal.png").convert_alpha()
heart_empty = pygame.image.load("data/health_vide.png").convert_alpha()

running = True

# === ÉCRAN DE DÉMARRAGE ===
waiting = True
while waiting:
    start_img = pygame.image.load("data/start_screen.png").convert()
    start_img = pygame.transform.scale(start_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(start_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
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

    #for plat in moving_platforms:
    #    plat.update()


    # Collisions plateformes
    wolf.jumping = True
    for platform in platforms :#+ [p.rect for p in moving_platforms]:
        if wolf.rect.colliderect(platform):
            if wolf.jump_speed > 0 and previous_bottom <= platform.top:
                wolf.rect.bottom = platform.top
                wolf.jump_speed = 0
                wolf.jumping = False
                break

    # Interactions avec animaux
    
    for animal in liste_animals:
        # Initialisation du flag de suivi de vie
        if not hasattr(animal, "was_alive"):
            animal.was_alive = True

        # === Update selon le type ===
        if isinstance(animal, animals.RoosterBoss):
            animal.update(wolf.rect, wolf, platforms)
        elif isinstance(animal, animals.Charger):
            animal.update(wolf)
        elif isinstance(animal, animals.BossFemme):
            animal.update(wolf, platforms)

            to_remove = []
            for proj in animal.projectiles:
                if wolf.rect.colliderect(proj.rect) and wolf.hit_timer <= 0:
                    wolf.take_damage(animal)
                    to_remove.append(proj)

            for proj in to_remove:
                animal.projectiles.remove(proj)
        elif isinstance(animal, animals.FinalBoss):
            animal.update(wolf, platforms)
            # Si le boss vient d’atterrir pour son attaque de zone (phase 1), on déclenche le tremblement
            if animal.shake_on_impact:
                camera_shake =40 # nombre de frames de secousse
                animal.shake_on_impact = False

            if animal.charging and wolf.rect.colliderect(animal.rect) and wolf.hit_timer <= 0:
                wolf.take_damage(animal)
                camera_shake = 30
            for proj in animal.projectiles:
                rect, vx, vy = proj
                angle = math.degrees(math.atan2(-vy, vx))
                rotated_fork = pygame.transform.rotate(level.fork_image, angle)
                rotated_rect = rotated_fork.get_rect(center=rect.center)
                screen.blit(rotated_fork, rotated_rect.move(-camera_offset, -camera_y))

                if rect.colliderect(wolf.rect) and wolf.hit_timer <= 0:
                    wolf.take_damage(animal)
            loup_above = (
                    previous_bottom <= animal.rect.top and
                    wolf.jump_speed > 0 and
                    wolf.rect.bottom <= animal.rect.top + 10
                )
            if wolf.rect.colliderect(animal.rect):

                if loup_above:
                    if animal.take_damage(1):
                        bloods.append(BloodEffect(animal.rect.center))
                    wolf.jump_speed = -8  # rebond

                elif wolf.hit_timer <= 0 and not animal.attack_zone_active:
                        wolf.take_damage(animal)
            # Zone d’impact (attaque au sol)
            if animal.attack_zone_active:
                # Position de la zone au sol
                zone_x = animal.rect.centerx - 300
                zone_y = animal.rect.bottom - 20
                zone_rect = pygame.Rect(zone_x, zone_y, 600, 20)

                # Affichage de l'image
                screen.blit(level.zone_attack_img, (zone_x - camera_offset, zone_y - camera_y))

                # Collision avec le loup
                if (
                    zone_rect.colliderect(wolf.rect)
                    and not loup_above
                    and wolf.hit_timer <= 0
                ):
                    wolf.take_damage(animal)
        elif isinstance(animal, animals.Dog):
            animal.update(wolf, platforms)
        elif isinstance(animal, animals.PigBoss):
            animal.update(wolf=wolf, platforms=platforms)
            if wolf.rect.colliderect(animal.rect):
                loup_above_boss = (
                    previous_bottom <= animal.rect.top + 5 and
                    wolf.jump_speed > 0 and
                    wolf.rect.centery < animal.rect.top
                )
                if loup_above_boss:
                    if animal.take_damage(1):
                        animal.knockback()
                        bloods.append(BloodEffect(animal.rect.center))
                        wolf.jump_speed = -8
                elif wolf.hit_timer <= 0:
                    animal.crush_effect(wolf)
        else:
            animal.update(platforms)

        # === Collisions génériques avec loup ===
        if not animal.alive:
            continue

        if wolf.rect.colliderect(animal.rect) and not isinstance(animal, (animals.PigBoss, animals.FinalBoss)):
            loup_above = (
                previous_bottom <= animal.rect.top + 5 and
                wolf.jump_speed > 0 and
                wolf.rect.centery < animal.rect.centery
            )
            if loup_above:
                if animal.take_damage(1):
                    bloods.append(BloodEffect(animal.get_blood_position()))
                    wolf.jump_speed = -8
            elif wolf.hit_timer <= 0:
                wolf.take_damage(animal)
                if isinstance(animal, animals.Charger):
                    camera_shake = 50
                    wolf.jump_speed = -20
                    wolf.jumping = True

        # === DROP UNIQUE À LA MORT ===
        if not animal.alive and animal.was_alive:
            animal.was_alive = False  # on évite les répétitions

            if isinstance(animal, (animals.Charger, animals.RoosterBoss, animals.PigBoss, animals.BossFemme)):
                speedboosts.append(SpeedBoost(animal.rect.center))
            else:
                if random.randint(1, 100) <= 20:
                    heals.append(Heal(animal.rect.center))

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
    explosion_frame_duration = 25  # plus la valeur est grande, plus l'explosion est lente

    for blood in bloods[:]:
        if isinstance(blood, tuple):  # Animation d'explosion d'œuf
            img, pos, delay = blood
            if frame_counter >= delay * explosion_frame_duration:
                screen.blit(img, (pos[0] - camera_offset, pos[1] - camera_y))
                bloods.remove(blood)
        else:  # BloodEffect classique
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

    #for plat in moving_platforms:
    #    plat.draw(screen, camera_offset, camera_y)


    for animal in liste_animals:
        animal.draw(screen, camera_offset, camera_y)

    wolf.update()

    # Gestion du ralentissement temporaire par le boss cochon
    if hasattr(wolf, 'slowed_timer') and wolf.slowed_timer > 0:
        wolf.slowed_timer -= 1
        if wolf.slowed_timer == 0:
            wolf.move_speed = 6
            wolf.jump = lambda: setattr(wolf, 'jump_speed', -13) or setattr(wolf, 'jumping', True)
            wolf.right_images = wolf.default_right_images
            wolf.left_images = wolf.default_left_images

    # Appliquer la secousse de caméra si active
    shake_x = random.randint(-5, 5) if camera_shake > 0 else 0
    shake_y = random.randint(-5, 5) if camera_shake > 0 else 0

    camera_offset += shake_x
    camera_y += shake_y

    if camera_shake > 0:
        camera_shake -= 1

    screen.blit(wolf.image, wolf.rect.move(-camera_offset, -camera_y))

    for i in range(wolf.max_health):
        image = heart_image if i < wolf.hp else heart_empty
        screen.blit(image, (10 + i * 45, 10))

    frame_counter += 1

    # Affichage des effets d'explosion d'œufs
    for explosion in egg_explosions[:]:
        explosion.update()
        explosion.draw(screen, camera_offset, camera_y)
        if explosion.finished:
            egg_explosions.remove(explosion)

    # === Passage au niveau suivant ===
    if all(not animal.alive for animal in liste_animals):
        level_number += 1

        if level_number == 2:
            level = Level2(LEVEL_WIDTH, LEVEL_HEIGHT)
        elif level_number == 3:
            level = Level3(LEVEL_WIDTH, LEVEL_HEIGHT)
        elif level_number == 4:
            level = Level4(LEVEL_WIDTH, LEVEL_HEIGHT)
        elif level_number == 5:
            level = Level5(LEVEL_WIDTH, LEVEL_HEIGHT)
        elif level_number == 6:
            level = Level6(LEVEL_WIDTH, LEVEL_HEIGHT)
        elif level_number > 6:
            # === FIN DU JEU ===
            victory_img = pygame.image.load("data/fond_win.png").convert()
            victory_img = pygame.transform.scale(victory_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(victory_img, (0, 0))
            pygame.display.flip()
            pygame.time.wait(5000)
            running = False
            break

        # Reset du niveau
        platforms = level.platforms
        liste_animals = level.animals
        background_image = pygame.transform.scale(level.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        wolf.rect.topleft = (150, 700)
        camera_offset = 0
        camera_y = LEVEL_HEIGHT - SCREEN_HEIGHT


    #if wolf.hp <= 0:
    #    game_over = True
    #    running = False

    pygame.display.flip()
    clock.tick(60)
# === ÉCRAN DE GAME OVER ===
if game_over:
    title_font = pygame.font.Font(None, 80)
    info_font = pygame.font.Font(None, 40)

    waiting = True
    while waiting:
        gameover_img = pygame.image.load("data/gameover_screen.png").convert()
        gameover_img = pygame.transform.scale(gameover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(gameover_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

        pygame.display.flip()
        clock.tick(60)

pygame.quit()