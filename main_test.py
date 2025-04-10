import pygame
import random
import gamelib.animals as animals
from gamelib.sprites import Wolf
from gamelib.items import Heal, SpeedBoost, MovingPlatform
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

# === Level Selection ===
selected_level = "enclos"  # Change this to test different levels

# Load level data based on selection
if selected_level == "enclos":
    background_image, platforms = create_level_enclos()
elif selected_level == "etable":
    background_image, platforms = create_level_etable()
elif selected_level == "jardin":
    background_image, platforms = create_level_jardin()
elif selected_level == "jardin_boss":
    background_image, platforms = create_level_jardin_boss()
elif selected_level == "salon":
    background_image, platforms = create_level_salon()
elif selected_level == "chambre":
    background_image, platforms = create_level_chambre()

background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Entities
wolf = Wolf((150, 700))

    elif level == "enclos":
        # 1ère tile : quelques vaches et cochons
        animals_list.append(animals.Pig((400, 300), right_images_pig, left_images_pig))
        animals_list.append(animals.Pig((800, 700), right_images_pig, left_images_pig))
        animals_list.append(animals.Cow((900, 400), right_images_cow, left_images_cow))
        animals_list.append(animals.Cow((1100, 700), right_images_cow, left_images_cow))

        # 2ème tile : boss cochon + cochon
        animals_list.append(
            animals.PigBoss((1600, 700), right_walk_pigboss, left_walk_pigboss,
                            right_charge_pigboss, left_charge_pigboss)
        )
        animals_list.append(animals.Pig((1750, 700), right_images_cow, left_images_cow))

    elif level == "jardin":
        # 1ère tile : poulets, cochons, vaches
        animals_list.append(animals.Chicken((400, 300), right_images_chicken, left_images_chicken))
        animals_list.append(animals.Pig((700, 200), right_images_pig, left_images_pig))
        animals_list.append(animals.Cow((1000, 700), right_images_cow, left_images_cow))

        # 2ème tile : Boss poulet + 1 de chaque
        rooster_boss = animals.RoosterBoss((1600, 700), right_images_chicken, left_images_chicken)
        animals_list.append(rooster_boss)
        animals_list.append(animals.Cow((1800, 700), right_images_cow, left_images_cow))
        animals_list.append(animals.Pig((1900, 700), right_images_pig, left_images_pig))
        animals_list.append(animals.Chicken((1700, 700), right_images_chicken, left_images_chicken))

    elif level == "salon":
        # Plusieurs chiens de garde (niveau salon)
        animals_list.append(animals.Dog((300, 350), right_walk_dog, left_walk_dog,
                                            dog_jump_prep, dog_jump_prep_left,
                                            dog_jump_air, dog_jump_air_left))
        animals_list.append(animals.Dog((500, 250), right_walk_dog, left_walk_dog,
                                            dog_jump_prep, dog_jump_prep_left,
                                            dog_jump_air, dog_jump_air_left))
        animals_list.append(animals.Dog((1700, 700), right_walk_dog, left_walk_dog,
                                            dog_jump_prep, dog_jump_prep_left,
                                            dog_jump_air, dog_jump_air_left))
        animals_list.append(animals.Dog((100, 700), right_walk_dog, left_walk_dog,
                                            dog_jump_prep, dog_jump_prep_left,
                                            dog_jump_air, dog_jump_air_left))
        

    elif level == "chambre":
        # Boss fermière
        animals_list.append(animals.FinalBoss((1200, 700)))

    elif level == "jardin_boss":
        # Boss fermier
        animals_list.append(animals.FinalBoss((1200, 700)))

    return animals_list

# Charger les monstres selon le niveau
liste_animals = load_animals_for_level(selected_level)
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
            # ... (le reste de la gestion FinalBoss, inchangé)
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