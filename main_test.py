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
from gamelib.items import Heal, SpeedBoost, Shield
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
shield_timer = 0
shield_spawn_timer = random.randint(180, 600)

#moving_platforms = [
 #   MovingPlatform(400, 600, 120, 20, dx=2, range_x=200) 
#]
# HUD

heart_image = pygame.image.load("data/heal.png").convert_alpha()
heart_empty = pygame.image.load("data/health_vide.png").convert_alpha()

running = True
level.debut_jeu.play(-1)
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
                level.debut_jeu.stop()
                level.fond_jeu.play(-1)

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
    for platform in platforms:
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
        if isinstance(animal, animals.RoosterBoss):
            animal.update(wolf.rect, wolf, platforms, level)
        elif isinstance(animal, animals.Charger):
            animal.update(wolf)
        elif isinstance(animal, animals.BossFemme):
            animal.update(wolf, platforms)
            
            to_remove = []
            for proj in animal.projectiles:
                if wolf.rect.colliderect(proj.rect) and wolf.hit_timer <= 0 and shield_timer <= 0:
                    wolf.take_damage(animal, level)
                    to_remove.append(proj)
            # Supprime les projectiles qui ont touché le loup
            for proj in to_remove:
                animal.projectiles.remove(proj)

        elif isinstance(animal, animals.FinalBoss):
            animal.update(wolf, platforms)
            # Si le boss vient d’atterrir pour son attaque de zone (phase 1), on déclenche le tremblement
            if animal.shake_on_impact:
                camera_shake =40 # nombre de frames de secousse
                animal.shake_on_impact = False

            if animal.charging and wolf.rect.colliderect(animal.rect) and wolf.hit_timer <= 0 and shield_timer <= 0:
                wolf.take_damage(animal,level)
                camera_shake = 30
            for proj in animal.projectiles:
                rect, vx, vy = proj
                angle = math.degrees(math.atan2(-vy, vx))
                rotated_fork = pygame.transform.rotate(level.fork_image, angle)
                rotated_rect = rotated_fork.get_rect(center=rect.center)
                screen.blit(rotated_fork, rotated_rect.move(-camera_offset, -camera_y))
                if rect.colliderect(wolf.rect) and wolf.hit_timer <= 0 and shield_timer <= 0:
                    wolf.take_damage(animal,level)
            loup_above = (
                    previous_bottom <= animal.rect.top and
                    wolf.jump_speed > 0 and
                    wolf.rect.bottom <= animal.rect.top + 10
                )
            if wolf.rect.colliderect(animal.rect):

                if loup_above:
                    if animal.take_damage(1):
                        level.son_fermier_degat.play()
                        bloods.append(BloodEffect(animal.rect.center))
                    wolf.jump_speed = -8  # rebond

                elif wolf.hit_timer <= 0 and not animal.attack_zone_active and shield_timer <=0:
                        wolf.take_damage(animal,level)
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
                    and shield_timer <= 0
                ):
                    wolf.take_damage(animal,level)

        elif isinstance(animal, animals.Dog):
            animal.update(wolf, platforms)
        elif isinstance(animal, animals.PigBoss):
            animal.update(wolf=wolf, platforms=platforms)
            if wolf.rect.colliderect(animal.rect):
                loup_above_boss = (
                    previous_bottom <= animal.rect.top and
                    wolf.jump_speed > 0 and
                    wolf.rect.bottom <= animal.rect.top + 10
                )
                
                if loup_above_boss:
                    if animal.take_damage(1):
                        level.son_boss_cochon_degat.play()
                        animal.knockback()
                        if random.randint(1, 100) <= 20:
                            heals.append(Heal(animal.rect.center))
                        bloods.append(BloodEffect(animal.rect.center))
                    wolf.jump_speed = -8

                elif wolf.hit_timer <= 0 and shield_timer <= 0:
                    animal.crush_effect(wolf, level)

        else:
            animal.update(platforms)

        if not animal.alive:
            continue

        if wolf.rect.colliderect(animal.rect) and not isinstance(animal, animals.PigBoss) and not isinstance(animal, animals.FinalBoss):
            loup_above = (
                previous_bottom <= animal.rect.top and
                wolf.jump_speed > 0 and
                wolf.rect.bottom <= animal.rect.top + 10
            )

            if loup_above:
                if animal.take_damage(1) and not isinstance(animal, (animals.Charger, animals.RoosterBoss, animals.PigBoss, animals.BossFemme)):
                    # Effets sonores selon l'animal touché
                    if isinstance(animal, animals.Chicken):
                        level.son_poulet_mort.play()
                    elif isinstance(animal, animals.Cow):
                        level.son_vache_mort.play()
                    elif isinstance(animal, animals.Pig):
                        level.son_cochon_mort.play()
                    elif isinstance(animal, animals.Dog):
                        level.son_chien_mort.play()
                    
                    # Si on est dans les 20% de chance
                    if random.randint(1,100) <= 20:
                        # Drop un os avec de la viande au bout 
                        heal_x = animal.rect.centerx
                        heal_y = animal.rect.centery  # pour poser au sol, ajustable selon taille du sprite
                        heals.append(Heal((heal_x, heal_y)))

                    # Calcul dynamique du point d’impact en bas du mob
                    if isinstance(animal, animals.PigBoss):
                        print("PigBoss rect:", animal.rect)
                        print("Blood position:", animal.get_blood_position())

                    bloods.append(BloodEffect(animal.get_blood_position()))

                else:
                    # Son de dégât (animal toujours vivant)
                    if isinstance(animal, animals.Chicken):
                        level.son_poulet_degat.play()
                    elif isinstance(animal, animals.Cow):
                        level.son_vache_degat.play()
                    elif isinstance(animal, animals.Pig):
                        level.son_cochon_degat.play()
                    elif isinstance(animal, animals.Dog):
                        level.son_chien_degat.play()

                wolf.jump_speed = -8
            elif wolf.hit_timer <= 0 and shield_timer <= 0:
                wolf.take_damage(animal,level)
                if isinstance(animal, animals.PigBoss):
                    animal.crush_effect(wolf)

                # Knockback si c'est un Charger
                if isinstance(animal, animals.Charger):
                    camera_shake = 50  # durée de la secousse en frames

                    wolf.jump_speed = -20
                    wolf.jumping = True

        if not animal.alive and animal.was_alive:
            animal.was_alive = False 

            if isinstance(animal, (animals.Charger, animals.RoosterBoss, animals.PigBoss, animals.BossFemme)):
                if isinstance(animal, animals.Charger):
                    level.son_boss_vache_mort.play()
                elif isinstance(animal, animals.PigBoss):
                    level.son_boss_cochon_mort.play()
                elif isinstance(animal, animals.RoosterBoss):
                    level.son_boss_poulet_mort.play()
                elif isinstance(animal, animals.BossFemme):
                    level.son_femme_mort.play()
                x = animal.rect.centerx
                y = animal.rect.bottom +40 
                speedboosts.append(SpeedBoost((x, y)))

            elif random.randint(1, 100) <= 20:
                    heals.append(Heal(animal.rect.center))
            if animal.take_damage(1) and animal.health > 0:
                if isinstance(animal, animals.PigBoss):
                    level.son_boss_cochon_degat.play()    
                    
        if level_number == 6 and isinstance(level, Level6):
            shield_spawn_timer -= 1
            if shield_spawn_timer <= 0:
                x = random.randint(100, LEVEL_WIDTH - 100)
                level.shield_powerups.append(Shield((x, -50)))
                shield_spawn_timer = random.randint(180, 600)
                    
    # Affichage des heals
    for heal in heals[:]:
        heal.update()
        heal.draw(screen, camera_offset, camera_y)

        # Ramassage
        if wolf.rect.colliderect(heal.rect):
            wolf.health = min(wolf.health + 1, wolf.max_health)
            heals.remove(heal)
            level.son_heal.play()

        # Disparition naturelle
        elif heal.timer <= 0:
            heals.remove(heal)
    
    # Affichage et ramassage des SpeedBoosts
    for boost in speedboosts[:]:
        boost.update(platforms)
        boost.draw(screen, camera_offset, camera_y)

        # Ramassage
        if wolf.rect.colliderect(boost.rect):
            speedboosts.remove(boost)
            speedboost_timer = 600  # 10 secondes
            wolf.move_speed = 10
            wolf.jump = lambda: setattr(wolf, 'jump_speed', -20) or setattr(wolf, 'jumping', True)
            level.power_up_loup.play()

        elif boost.timer <= 0:
            speedboosts.remove(boost)

    # Affichage et ramassage des boucliers
    if hasattr(level, "shield_powerups"):
        for shield in level.shield_powerups[:]:
            shield.update(platforms)
            shield.draw(screen, camera_offset, camera_y)

            if wolf.rect.colliderect(shield.rect):
                level.shield_powerups.remove(shield)
                shield_timer = 600  # 10 secondes d’invincibilité
                level.power_up_loup.play()

            elif shield.timer <= 0:
                level.shield_powerups.remove(shield)

    if shield_timer > 0:
        shield_timer -= 1
        aura_rect = level.aura_image.get_rect(center=wolf.rect.center)
        screen.blit(level.aura_image, aura_rect.move(-camera_offset, -camera_y))

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
        image = heart_image if i < wolf.health else heart_empty
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
            pygame.time.wait(1000)
            level.fond_jeu.stop()
            level = Level6(LEVEL_WIDTH, LEVEL_HEIGHT)
        elif level_number > 6:
            if shield_timer > 0:
                shield_timer -= 1
            
            if shield_timer > 0:
                aura_rect = level.aura_image.get_rect(center=wolf.rect.center)
                screen.blit(level.aura_image, aura_rect.move(-camera_offset, -camera_y))
                # Affichage et ramassage des boucliers
                for shield in level.shield_powerups[:]:
                    shield.update(platforms)
                    shield.draw(screen, camera_offset, camera_y)

            # === FIN DU JEU ===
            level.son_boss.stop()
            level.fond_jeu.stop()
            level.victoire.play()
            waiting = True
            while waiting:
                victory_img = pygame.image.load("data/fond_win.png").convert()
                victory_img = pygame.transform.scale(victory_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(victory_img, (0, 0))
                #pygame.time.wait(5000)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
                pygame.display.flip()

        # Reset du niveau
        platforms = level.platforms
        liste_animals = level.animals
        background_image = pygame.transform.scale(level.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        wolf.rect.topleft = (150, 700)
        camera_offset = 0
        camera_y = LEVEL_HEIGHT - SCREEN_HEIGHT


    if wolf.health <= 0:
        game_over = True
        running = False
        level.fond_jeu.stop()
        level.son_boss.stop()
        level.game_over.play(-1)

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