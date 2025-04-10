import pygame
import random
import gamelib.animals as animals
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

right_images_charger_walk = [
    pygame.image.load("data/boss_vache_marche_1.png").convert_alpha(),
    pygame.image.load("data/boss_vache_marche_2.png").convert_alpha()
]
left_images_charger_walk = [pygame.transform.flip(img, True, False) for img in right_images_charger_walk]

right_images_charger_charge = [
    pygame.image.load("data/boss_vache_charge_1.png").convert_alpha(),
    pygame.image.load("data/boss_vache_charge_2.png").convert_alpha()
]
left_images_charger_charge = [pygame.transform.flip(img, True, False) for img in right_images_charger_charge]

# Sprites marche boss cochon
right_walk_pigboss = [
    pygame.image.load("data/boss_cochon_1.png").convert_alpha(),
    pygame.image.load("data/boss_cochon_2.png").convert_alpha(),
    pygame.image.load("data/boss_cochon_3.png").convert_alpha()
]
left_walk_pigboss = [pygame.transform.flip(img, True, False) for img in right_walk_pigboss]

# Sprites charge boss cochon
right_charge_pigboss = [
    pygame.image.load("data/boss_cochon_2.png").convert_alpha()
]
left_charge_pigboss = [pygame.transform.flip(img, True, False) for img in right_charge_pigboss]

# Dog sprites
right_walk_dog = [
    pygame.image.load("data/chien_marche1.png").convert_alpha(),
    pygame.image.load("data/chien_marche2.png").convert_alpha(),
    pygame.image.load("data/chien_marche3.png").convert_alpha(),
    pygame.image.load("data/chien_marche4.png").convert_alpha()
]
left_walk_dog = [pygame.transform.flip(img, True, False) for img in right_walk_dog]

dog_jump_prep = pygame.image.load("data/chien_prep_saut.png").convert_alpha()
dog_jump_air = pygame.image.load("data/chien_saut.png").convert_alpha()
dog_jump_prep_left = pygame.transform.flip(dog_jump_prep, True, False)
dog_jump_air_left = pygame.transform.flip(dog_jump_air, True, False)

# Boss final sprites
boss_walk_images  = [
    pygame.image.load("data/fermier_marche1.png").convert_alpha(),
    pygame.image.load("data/fermier_marche2.png").convert_alpha(),
    pygame.image.load("data/fermier_marche3.png").convert_alpha()
]
boss_jump_start  = pygame.image.load("data/fermier_saut1.png").convert_alpha()
boss_jump_air  = pygame.image.load("data/fermier_saut2.png").convert_alpha()
boss_attack_ground  = pygame.image.load("data/fermier_saut3.png").convert_alpha()

boss_walk_images_left = [pygame.transform.flip(img, True, False) for img in boss_walk_images]
boss_jump_start_left = pygame.transform.flip(boss_jump_start, True, False)
boss_jump_air_left = pygame.transform.flip(boss_jump_air, True, False)
boss_attack_ground_left = pygame.transform.flip(boss_attack_ground, True, False)

#attaque de zone
zone_attack_img = pygame.image.load("data/attaque_de_zone.png").convert_alpha()
zone_attack_img = pygame.transform.scale(zone_attack_img, (600, 20))

# Sprites de la femme
femme_walk_images = [
    pygame.image.load("data/femme_marche1.png").convert_alpha(),
    pygame.image.load("data/femme_marche2.png").convert_alpha(),
    pygame.image.load("data/femme_marche3.png").convert_alpha(),
    pygame.image.load("data/femme_marche4.png").convert_alpha()
]
femme_walk_images_left = [pygame.transform.flip(img, True, False) for img in femme_walk_images]

femme_throw_images = [
    pygame.image.load("data/femme_lancer1.png").convert_alpha(),
    pygame.image.load("data/femme_lancer2.png").convert_alpha()
]
femme_throw_images_left = [pygame.transform.flip(img, True, False) for img in femme_throw_images]

#Boss poulet
# Marche
rooster_walk_right = [
    pygame.image.load("data/boss_poulet_marche1.png").convert_alpha(),
    pygame.image.load("data/boss_poulet_marche2.png").convert_alpha()
]
rooster_walk_left = [pygame.transform.flip(img, True, False) for img in rooster_walk_right]

# Préparation de tir
rooster_charge_right = pygame.image.load("data/boss_poulet_tire1.png").convert_alpha()
rooster_charge_left = pygame.transform.flip(rooster_charge_right, True, False)

# Tir
rooster_shoot_right = pygame.image.load("data/boss_poulet_tire2.png").convert_alpha()
rooster_shoot_left = pygame.transform.flip(rooster_shoot_right, True, False)

aura_image = pygame.image.load("data/aura.png").convert_alpha()


# Entities
wolf = Wolf((150, 700))
liste_animals = [
    animals.Chicken((1000, 700), 0, LEVEL_WIDTH, right_images_chicken, left_images_chicken),
    animals.Chicken((1500, 700), 0, LEVEL_WIDTH, right_images_chicken, left_images_chicken),
    #animals.Cow((1200, 700), 0, LEVEL_WIDTH, right_images_cow, left_images_cow),
    #animals.Cow((1700, 700), 0, LEVEL_WIDTH, right_images_cow, left_images_cow),
    #animals.Pig((1500, 700), right_images_pig, left_images_pig),
    #animals.Pig((1900, 700), right_images_pig, left_images_pig),
    #animals.Charger((1600, 700), 0,LEVEL_WIDTH, right_images_charger_walk, left_images_charger_walk, right_images_charger_charge, left_images_charger_charge),
    #animals.RoosterBoss((1000, 700),right_images=rooster_walk_right,left_images=rooster_walk_left,charge_right=rooster_charge_right,charge_left=rooster_charge_left,shoot_right=rooster_shoot_right,shoot_left=rooster_shoot_left),
    #animals.Dog((800, 700), right_walk_dog, left_walk_dog, dog_jump_prep, dog_jump_prep_left, dog_jump_air, dog_jump_air_left),
    #animals.Dog((800, 700), 0,LEVEL_WIDTH,right_walk_dog, left_walk_dog, dog_jump_prep, dog_jump_prep_left, dog_jump_air, dog_jump_air_left),
    #animals.PigBoss((1700, 700), 0, LEVEL_WIDTH,right_walk_pigboss, left_walk_pigboss, right_charge_pigboss, left_charge_pigboss),
    #animals.FinalBoss((500, 500),0, LEVEL_WIDTH,walk_right=boss_walk_images,walk_left=boss_walk_images_left,jump_start_right=boss_jump_start,jump_start_left=boss_jump_start_left,jump_air_right=boss_jump_air,jump_air_left=boss_jump_air_left,attack_ground_right=boss_attack_ground,attack_ground_left=boss_attack_ground_left),
    #animals.BossFemme((1300, 500), femme_walk_images, femme_walk_images_left, femme_throw_images, femme_throw_images_left)
    #animals.FinalBoss((500, 500),walk_right=boss_walk_images,walk_left=boss_walk_images_left,jump_start_right=boss_jump_start,jump_start_left=boss_jump_start_left,jump_air_right=boss_jump_air,jump_air_left=boss_jump_air_left,attack_ground_right=boss_attack_ground,attack_ground_left=boss_attack_ground_left),
    #animals.BossFemme((1300, 500), femme_walk_images, femme_walk_images_left, femme_throw_images, femme_throw_images_left)
    ]
heals = []
speedboosts = []
speedboost_timer = 0
speedboosts.append(SpeedBoost((600, 700)))
bloods = []
egg_explosions = []
frame_counter = 0

shield_powerups = []
shield_timer = 0


# Plateformes
platforms = [
    pygame.Rect(0, 800, 3100, 50),
    #pygame.Rect(200, 700, 120, 20),
    #pygame.Rect(400, 600, 100, 20),
    #pygame.Rect(600, 500, 100, 20),
    #pygame.Rect(850, 700, 150, 20),
    #pygame.Rect(1050, 600, 100, 20),
    #pygame.Rect(1250, 500, 120, 20),
    #pygame.Rect(1450, 400, 120, 20),
    #pygame.Rect(1650, 650, 100, 20),
    #pygame.Rect(1750, 550, 100, 20),
    #pygame.Rect(1800, 450, 80, 20)
]

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

#A METTRE DANS LE DERNIER NIVEAU
    # Spawning aléatoire du bouclier (1/800 chance chaque frame)
    if random.randint(1, 800) == 1:
        x = random.randint(200, LEVEL_WIDTH - 200)
        shield_powerups.append(Shield((x, -50)))  # spawn dans le ciel

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
    
    for animal in liste_animals:   
        # Initialisation du flag de suivi de vie
        if not hasattr(animal, "was_alive"):
            animal.was_alive = True

        if isinstance(animal, animals.RoosterBoss):
            animal.update(wolf.rect, wolf, platforms)
        elif isinstance(animal, animals.Charger):
            animal.update(wolf)
        elif isinstance(animal, animals.BossFemme):
            animal.update(wolf, platforms)
            
            to_remove = []
            for proj in animal.projectiles:
                if wolf.rect.colliderect(proj.rect) and wolf.hit_timer <= 0 and shield_timer <= 0:
                    wolf.take_damage(animal)
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
                wolf.take_damage(animal)
                camera_shake = 30
            for proj in animal.projectiles:
                rect, vx, vy = proj
                pygame.draw.rect(screen, (255, 255, 0), rect.move(-camera_offset, -camera_y))
                if rect.colliderect(wolf.rect) and wolf.hit_timer <= 0 and shield_timer <= 0:
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
                screen.blit(zone_attack_img, (zone_x - camera_offset, zone_y - camera_y))

                # Collision avec le loup
                if (
                    zone_rect.colliderect(wolf.rect)
                    and not loup_above
                    and wolf.hit_timer <= 0
                    and shield_timer <= 0
                ):
                    wolf.take_damage(animal)

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
                        animal.knockback()
                        if random.randint(1, 100) <= 20:
                            heals.append(Heal(animal.rect.center))
                        bloods.append(BloodEffect(animal.rect.center))
                    wolf.jump_speed = -8

                elif wolf.hit_timer <= 0 and shield_timer <= 0:
                    animal.crush_effect(wolf)

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


                wolf.jump_speed = -8

            elif wolf.hit_timer <= 0 and shield_timer <= 0:
                wolf.take_damage(animal)
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
                x = animal.rect.centerx
                y = animal.rect.bottom +40 
                speedboosts.append(SpeedBoost((x, y)))

            elif random.randint(1, 100) <= 20:
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
        boost.update(platforms)
        boost.draw(screen, camera_offset, camera_y)

        # Ramassage
        if wolf.rect.colliderect(boost.rect):
            speedboosts.remove(boost)
            speedboost_timer = 600  # 10 secondes
            wolf.move_speed = 10
            wolf.jump = lambda: setattr(wolf, 'jump_speed', -20) or setattr(wolf, 'jumping', True)

        elif boost.timer <= 0:
            speedboosts.remove(boost)

    # Affichage et ramassage des boucliers
    for shield in shield_powerups[:]:
        shield.update(platforms)
        shield.draw(screen, camera_offset, camera_y)

        if wolf.rect.colliderect(shield.rect):
            shield_powerups.remove(shield)
            shield_timer = 600  # 10 secondes d’invincibilité
        elif shield.timer <= 0:
            shield_powerups.remove(shield)
    if shield_timer > 0:
        shield_timer -= 1



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

    if shield_timer > 0:
        aura_rect = aura_image.get_rect(center=wolf.rect.center)
        screen.blit(aura_image, aura_rect.move(-camera_offset, -camera_y))


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

    if wolf.hp <= 0:
        game_over = True
        running = False

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