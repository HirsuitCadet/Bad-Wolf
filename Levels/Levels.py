import pygame
from gamelib.sprites import Wolf

class Level():
    def __init__(self):
        # Wolf sprites
        left_images_wolf = [
            pygame.image.load("../data/Loup1.png").convert_alpha(),
            pygame.image.load("../data/Loup2.png").convert_alpha(),
            pygame.image.load("../data/Loup3.png").convert_alpha(),
            pygame.image.load("../data/Loup4.png").convert_alpha(),
            pygame.image.load("../data/Loup5.png").convert_alpha(),
            pygame.image.load("../data/Loup6.png").convert_alpha(),
            pygame.image.load("../data/Loup7.png").convert_alpha(),
            pygame.image.load("../data/Loup8.png").convert_alpha(),
        ]
        right_images_wolf = [pygame.transform.flip(img, True, False) for img in left_images_wolf]

        Wolf.right_images = right_images_wolf
        Wolf.left_images = left_images_wolf

        wolf_sit_right = pygame.image.load("../data/Loup_sit.png").convert_alpha()
        wolf_sit_left = pygame.transform.flip(wolf_sit_right, True, False)

        Wolf.sit_image_right = wolf_sit_right
        Wolf.sit_image_left = wolf_sit_left

        # Chicken sprites
        right_images_chicken = [
            pygame.image.load("../data/Poule1.png").convert_alpha(),
            pygame.image.load("../data/Poule2.png").convert_alpha(),
            pygame.image.load("../data/Poule3.png").convert_alpha(),
            pygame.image.load("../data/Poule4.png").convert_alpha(),
        ]
        left_images_chicken = [pygame.transform.flip(img, True, False) for img in right_images_chicken]

        #Cow sprites
        right_images_cow = [
            pygame.image.load("../data/Vache1.png").convert_alpha(),
            pygame.image.load("../data/Vache2.png").convert_alpha(),
            pygame.image.load("../data/Vache3.png").convert_alpha(),
        ]
        left_images_cow = [pygame.transform.flip(img, True, False) for img in right_images_cow]

        #Pig sprites
        right_images_pig = [
            pygame.image.load("../data/Cochon1.png").convert_alpha(),
            pygame.image.load("../data/Cochon2.png").convert_alpha(),
            pygame.image.load("../data/Cochon3.png").convert_alpha(),
            pygame.image.load("../data/Cochon4.png").convert_alpha(),
        ]
        left_images_pig = [pygame.transform.flip(img, True, False) for img in right_images_pig]

        right_images_charger_walk = [
            pygame.image.load("../data/boss_vache_marche_1.png").convert_alpha(),
            pygame.image.load("../data/boss_vache_marche_2.png").convert_alpha()
        ]
        left_images_charger_walk = [pygame.transform.flip(img, True, False) for img in right_images_charger_walk]

        right_images_charger_charge = [
            pygame.image.load("../data/boss_vache_charge_1.png").convert_alpha(),
            pygame.image.load("../data/boss_vache_charge_2.png").convert_alpha()
        ]
        left_images_charger_charge = [pygame.transform.flip(img, True, False) for img in right_images_charger_charge]

        # Sprites marche boss cochon
        right_walk_pigboss = [
            pygame.image.load("../data/boss_cochon_1.png").convert_alpha(),
            pygame.image.load("../data/boss_cochon_2.png").convert_alpha(),
            pygame.image.load("../data/boss_cochon_3.png").convert_alpha()
        ]
        left_walk_pigboss = [pygame.transform.flip(img, True, False) for img in right_walk_pigboss]

        # Sprites charge boss cochon
        right_charge_pigboss = [
            pygame.image.load("../data/boss_cochon_2.png").convert_alpha()
        ]
        left_charge_pigboss = [pygame.transform.flip(img, True, False) for img in right_charge_pigboss]

        # Dog sprites
        right_walk_dog = [
            pygame.image.load("../data/chien_marche1.png").convert_alpha(),
            pygame.image.load("../data/chien_marche2.png").convert_alpha(),
            pygame.image.load("../data/chien_marche3.png").convert_alpha(),
            pygame.image.load("../data/chien_marche4.png").convert_alpha()
        ]
        left_walk_dog = [pygame.transform.flip(img, True, False) for img in right_walk_dog]

        dog_jump_prep = pygame.image.load("../data/chien_prep_saut.png").convert_alpha()
        dog_jump_air = pygame.image.load("../data/chien_saut.png").convert_alpha()
        dog_jump_prep_left = pygame.transform.flip(dog_jump_prep, True, False)
        dog_jump_air_left = pygame.transform.flip(dog_jump_air, True, False)

        # Boss final sprites
        boss_walk_images  = [
            pygame.image.load("../data/fermier_marche1.png").convert_alpha(),
            pygame.image.load("../data/fermier_marche2.png").convert_alpha(),
            pygame.image.load("../data/fermier_marche3.png").convert_alpha()
        ]
        boss_jump_start  = pygame.image.load("../data/fermier_saut1.png").convert_alpha()
        boss_jump_air  = pygame.image.load("../data/fermier_saut2.png").convert_alpha()
        boss_attack_ground  = pygame.image.load("../data/fermier_saut3.png").convert_alpha()

        boss_walk_images_left = [pygame.transform.flip(img, True, False) for img in boss_walk_images]
        boss_jump_start_left = pygame.transform.flip(boss_jump_start, True, False)
        boss_jump_air_left = pygame.transform.flip(boss_jump_air, True, False)
        boss_attack_ground_left = pygame.transform.flip(boss_attack_ground, True, False)

        # Sprites de la femme
        femme_walk_images = [
            pygame.image.load("../data/femme_marche1.png").convert_alpha(),
            pygame.image.load("../data/femme_marche2.png").convert_alpha(),
            pygame.image.load("../data/femme_marche3.png").convert_alpha(),
            pygame.image.load("../data/femme_marche4.png").convert_alpha()
        ]
        femme_walk_images_left = [pygame.transform.flip(img, True, False) for img in femme_walk_images]

        femme_throw_images = [
            pygame.image.load("../data/femme_lancer1.png").convert_alpha(),
            pygame.image.load("../data/femme_lancer2.png").convert_alpha()
        ]
        femme_throw_images_left = [pygame.transform.flip(img, True, False) for img in femme_throw_images]

        #Boss poulet
        # Marche
        rooster_walk_right = [
            pygame.image.load("../data/boss_poulet_marche1.png").convert_alpha(),
            pygame.image.load("../data/boss_poulet_marche2.png").convert_alpha()
        ]
        rooster_walk_left = [pygame.transform.flip(img, True, False) for img in rooster_walk_right]

        # Préparation de tir
        rooster_charge_right = pygame.image.load("../data/boss_poulet_tire1.png").convert_alpha()
        rooster_charge_left = pygame.transform.flip(rooster_charge_right, True, False)

        # Tir
        rooster_shoot_right = pygame.image.load("../data/boss_poulet_tire2.png").convert_alpha()
        rooster_shoot_left = pygame.transform.flip(rooster_shoot_right, True, False)
