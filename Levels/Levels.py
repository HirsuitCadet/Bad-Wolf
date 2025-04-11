import pygame
from gamelib.sprites import Wolf

class Levels():
    def __init__(self):
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

        Wolf.sit_image_right = pygame.image.load("data/Loup_sit.png").convert_alpha()
        Wolf.sit_image_left = pygame.transform.flip(Wolf.sit_image_right, True, False)

        # Chicken
        self.right_images_chicken = [
            pygame.image.load("data/Poule1.png").convert_alpha(),
            pygame.image.load("data/Poule2.png").convert_alpha(),
            pygame.image.load("data/Poule3.png").convert_alpha(),
            pygame.image.load("data/Poule4.png").convert_alpha(),
        ]
        self.left_images_chicken = [pygame.transform.flip(img, True, False) for img in self.right_images_chicken]

        # Cow
        self.right_images_cow = [
            pygame.image.load("data/Vache1.png").convert_alpha(),
            pygame.image.load("data/Vache2.png").convert_alpha(),
            pygame.image.load("data/Vache3.png").convert_alpha(),
        ]
        self.left_images_cow = [pygame.transform.flip(img, True, False) for img in self.right_images_cow]

        # Pig
        self.right_images_pig = [
            pygame.image.load("data/Cochon1.png").convert_alpha(),
            pygame.image.load("data/Cochon2.png").convert_alpha(),
            pygame.image.load("data/Cochon3.png").convert_alpha(),
            pygame.image.load("data/Cochon4.png").convert_alpha(),
        ]
        self.left_images_pig = [pygame.transform.flip(img, True, False) for img in self.right_images_pig]

        # Charger
        self.right_images_charger_walk = [
            pygame.image.load("data/boss_vache_marche_1.png").convert_alpha(),
            pygame.image.load("data/boss_vache_marche_2.png").convert_alpha()
        ]
        self.left_images_charger_walk = [pygame.transform.flip(img, True, False) for img in self.right_images_charger_walk]

        self.right_images_charger_charge = [
            pygame.image.load("data/boss_vache_charge_1.png").convert_alpha(),
            pygame.image.load("data/boss_vache_charge_2.png").convert_alpha()
        ]
        self.left_images_charger_charge = [pygame.transform.flip(img, True, False) for img in self.right_images_charger_charge]

        # PigBoss
        self.right_walk_pigboss = [
            pygame.image.load("data/boss_cochon_1.png").convert_alpha(),
            pygame.image.load("data/boss_cochon_2.png").convert_alpha(),
            pygame.image.load("data/boss_cochon_3.png").convert_alpha()
        ]
        self.left_walk_pigboss = [pygame.transform.flip(img, True, False) for img in self.right_walk_pigboss]

        self.right_charge_pigboss = [
            pygame.image.load("data/boss_cochon_2.png").convert_alpha()
        ]
        self.left_charge_pigboss = [pygame.transform.flip(img, True, False) for img in self.right_charge_pigboss]

        # Dog
        self.right_walk_dog = [
            pygame.image.load("data/chien_marche1.png").convert_alpha(),
            pygame.image.load("data/chien_marche2.png").convert_alpha(),
            pygame.image.load("data/chien_marche3.png").convert_alpha(),
            pygame.image.load("data/chien_marche4.png").convert_alpha()
        ]
        self.left_walk_dog = [pygame.transform.flip(img, True, False) for img in self.right_walk_dog]

        self.dog_jump_prep = pygame.image.load("data/chien_prep_saut.png").convert_alpha()
        self.dog_jump_air = pygame.image.load("data/chien_saut.png").convert_alpha()
        self.dog_jump_prep_left = pygame.transform.flip(self.dog_jump_prep, True, False)
        self.dog_jump_air_left = pygame.transform.flip(self.dog_jump_air, True, False)

        # Final Boss
        self.boss_walk_images = [
            pygame.image.load("data/fermier_marche1.png").convert_alpha(),
            pygame.image.load("data/fermier_marche2.png").convert_alpha(),
            pygame.image.load("data/fermier_marche3.png").convert_alpha()
        ]
        self.boss_jump_start = pygame.image.load("data/fermier_saut1.png").convert_alpha()
        self.boss_jump_air = pygame.image.load("data/fermier_saut2.png").convert_alpha()
        self.boss_attack_ground = pygame.image.load("data/fermier_saut3.png").convert_alpha()

        self.boss_walk_images_left = [pygame.transform.flip(img, True, False) for img in self.boss_walk_images]
        self.boss_charge_images = [
            pygame.image.load("data/fermier_charge1.png").convert_alpha(),
            pygame.image.load("data/fermier_charge2.png").convert_alpha()
        ]
        self.boss_charge_images_left = [pygame.transform.flip(img, True, False) for img in self.boss_charge_images]
        self.boss_jump_start_left = pygame.transform.flip(self.boss_jump_start, True, False)
        self.boss_jump_air_left = pygame.transform.flip(self.boss_jump_air, True, False)
        self.boss_attack_ground_left = pygame.transform.flip(self.boss_attack_ground, True, False)
        self.zone_attack_img = pygame.image.load("data/attaque_de_zone.png").convert_alpha()
        self.zone_attack_img = pygame.transform.scale(self.zone_attack_img, (600, 20))
        self.fork_image = pygame.image.load("data/fourche.png").convert_alpha()

        # BossFemme
        self.femme_walk_images = [
            pygame.image.load("data/femme_marche1.png").convert_alpha(),
            pygame.image.load("data/femme_marche2.png").convert_alpha(),
            pygame.image.load("data/femme_marche3.png").convert_alpha(),
            pygame.image.load("data/femme_marche4.png").convert_alpha()
        ]
        self.femme_walk_images_left = [pygame.transform.flip(img, True, False) for img in self.femme_walk_images]

        self.femme_throw_images = [
            pygame.image.load("data/femme_lancer1.png").convert_alpha(),
            pygame.image.load("data/femme_lancer2.png").convert_alpha()
        ]
        self.femme_throw_images_left = [pygame.transform.flip(img, True, False) for img in self.femme_throw_images]

        # RoosterBoss
        self.rooster_walk_right = [
            pygame.image.load("data/boss_poulet_marche1.png").convert_alpha(),
            pygame.image.load("data/boss_poulet_marche2.png").convert_alpha()
        ]
        self.rooster_walk_left = [pygame.transform.flip(img, True, False) for img in self.rooster_walk_right]

        self.rooster_charge_right = pygame.image.load("data/boss_poulet_tire1.png").convert_alpha()
        self.rooster_charge_left = pygame.transform.flip(self.rooster_charge_right, True, False)

        self.rooster_shoot_right = pygame.image.load("data/boss_poulet_tire2.png").convert_alpha()
        self.rooster_shoot_left = pygame.transform.flip(self.rooster_shoot_right, True, False)

        self.moon_image = pygame.image.load("data/moon.png").convert_alpha()
        self.aura_image = pygame.image.load("data/aura.png").convert_alpha()

        #Song
        pygame.mixer.init()
        son_chien_degat = pygame.mixer.Sound("data/son_chien_degat.wav")
        son_chien_degat.set_volume(0.5)
        son_chien_mort = pygame.mixer.Sound("data/son_chien_mort.wav")
        son_chien_mort.set_volume(0.5)
        son_chien_saut = pygame.mixer.Sound("data/son_chien_saut.wav")
        son_chien_saut.set_volume(0.5)
        son_cochon_degat = pygame.mixer.Sound("data/son_cochon_degat.wav")
        son_cochon_degat.set_volume(0.5)
        son_cochon_mort = pygame.mixer.Sound("data/son_cochon_mort.wav")
        son_cochon_mort.set_volume(0.5)
        son_femme_degat = pygame.mixer.Sound("data/son_femme_degat.wav")
        son_femme_degat.set_volume(0.5)
        son_femme_mort = pygame.mixer.Sound("data/son_femme_mort.wav")
        son_femme_mort.set_volume(0.5)
        son_fermier_degat = pygame.mixer.Sound("data/son_fermier_degat.wav")
        son_fermier_degat.set_volume(0.5)
        son_heal = pygame.mixer.Sound("data/son_heal.wav")
        son_heal.set_volume(0.5)
        son_loup_degat = pygame.mixer.Sound("data/son_loup_degat.wav")
        son_loup_degat.set_volume(0.5)
        son_atterissage_phase_1 = pygame.mixer.Sound("data/son_phase_1.wav")
        son_atterissage_phase_1.set_volume(0.5)
        son_phase_2 = pygame.mixer.Sound("data/son_phase_2.wav")
        son_phase_2.set_volume(0.5)
        son_phase_3 = pygame.mixer.Sound("data/son_phase_3.wav")
        son_phase_3.set_volume(0.5)
        son_poulet_degat = pygame.mixer.Sound("data/son_poulet_degat.wav")
        son_poulet_degat.set_volume(0.5)
        son_poulet_mort = pygame.mixer.Sound("data/son_poulet_mort.wav")
        son_poulet_mort.set_volume(0.5)
        son_spawn_fermier = pygame.mixer.Sound("data/son_spawn_fermier.wav")
        son_spawn_fermier.set_volume(0.5)
        son_vache_degat = pygame.mixer.Sound("data/son_vache_degat.wav")
        son_vache_degat.set_volume(0.5)
        son_vache_mort = pygame.mixer.Sound("data/son_vache_mort.wav")
        son_vache_mort.set_volume(0.5)
        son_boss_cochon_degat = pygame.mixer.Sound("data/son_boss_cochon_degat.wav")
        son_boss_cochon_degat.set_volume(0.5)
        son_boss_vache_degat = pygame.mixer.Sound("data/son_boss_vache_degat.wav")
        son_boss_vache_degat.set_volume(0.5)
        son_boss_poulet_degat = pygame.mixer.Sound("data/son_boss_poulet_degat.wav")
        son_boss_poulet_degat.set_volume(0.5)
        son_boss_poulet_mort = pygame.mixer.Sound("data/Poulet_boss_mort.wav")
        son_boss_poulet_mort.set_volume(0.5)
        son_boss_vache_mort = pygame.mixer.Sound("data/son_boss_vache_mort.wav")
        son_boss_vache_mort.set_volume(0.5)
        son_boss_cochon_mort = pygame.mixer.Sound("data/son_boss_cochon_mort.wav")
        son_boss_cochon_mort.set_volume(0.5)
        power_up_loup = pygame.mixer.Sound("data/Power-up-loup.wav")
        power_up_loup.set_volume(0.5)
        changement_phase = pygame.mixer.Sound("data/Boss-changement-de-phase.wav")
        changement_phase.set_volume(0.5)
        attaque_phase1 = pygame.mixer.Sound("data/Saut-fermier.wav")
        attaque_phase1.set_volume(0.5)
        debut_jeu = pygame.mixer.Sound("data/DÃ©but_jeu.wav")
        debut_jeu.set_volume(0.5)
        fond_jeu = pygame.mixer.Sound("data/Fond_jeu.wav")
        fond_jeu.set_volume(0.5)
        game_over = pygame.mixer.Sound("data/Game_over.wav")
        game_over.set_volume(0.5)
        victoire = pygame.mixer.Sound("data/Victoire.wav")
        victoire.set_volume(0.5)
        son_boss = pygame.mixer.Sound("data/son_boss.wav")
        son_boss.set_volume(0.5)