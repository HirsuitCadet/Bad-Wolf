import pygame
import random
import math
from gamelib.effects import EggProjectile, HomingProjectile

LEVEL_WIDTH = 1900

class Animal:
    def __init__(self, pos, right_images, left_images, speed=2, health=1):
        self.right_images = right_images
        self.left_images = left_images
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.direction = 1
        self.health = health
        self.alive = True
        self.frame = 0
        self.frame_timer = 0
        self.flash_timer = 0
        self.gravity = 1
        self.fall_speed = 0
        self.on_ground = False


    def update(self,platforms):
        if not self.alive:
            return

        self.rect.x += self.speed * self.direction

        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.fall_speed >= 0 and self.rect.bottom <= plat.bottom:
                    self.rect.bottom = plat.top
                    self.fall_speed = 0
                    self.on_ground = True

        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1

        self.images = self.right_images if self.direction > 0 else self.left_images

        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
            self.frame_timer = 0

        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1
            

    def draw(self, screen, offset_x=0, offset_y=0):
        if self.alive:
            screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

    def take_damage(self, amount):
        self.health -= amount
        self.flash_timer = 6
        if self.health <= 0:
            self.alive = False
            self.rect.width = 0
            self.rect.height = 0
            return True
        return False
    
    def get_blood_position(self):
        visible_height = self.image.get_height()
        x = self.rect.left + self.image.get_width() // 2
        y = self.rect.top + visible_height - visible_height // 4
        return (x, y)



class Chicken(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=3, health=1)

class Cow(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=1, health=3)

class Pig(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images, speed=2, health=2)

class Charger(Animal):
    def __init__(self, pos, walk_right, walk_left, charge_right, charge_left):
        super().__init__(pos, walk_right, walk_left, speed=3, health=3)
        self.walk_right_images = walk_right
        self.walk_left_images = walk_left
        self.charge_right_images = charge_right
        self.charge_left_images = charge_left
        self.is_charging = False
        self.flee_timer = 0
        self.normal_speed = self.speed
        self.flee_speed = 10

    def update(self, wolf=None):
        if not self.alive:
            return

        # Distance entre le loup et le Charger
        dx = wolf.rect.centerx - self.rect.centerx
        dy = wolf.rect.centery - self.rect.centery

        if self.flee_timer > 0:
            self.speed = self.flee_speed
            self.flee_timer -= 1
        elif abs(dx) < 500 and abs(dy) < 100 and ((dx > 0 and self.direction > 0) or (dx < 0 and self.direction < 0)):
            self.speed = 7
            self.is_charging = True
        else:
            self.speed = self.normal_speed
            self.is_charging = False
        
        if self.is_charging:
            self.images = self.charge_right_images if self.direction > 0 else self.charge_left_images
        else:
            self.images = self.walk_right_images if self.direction > 0 else self.walk_left_images

        self.frame_timer += 1
        if self.frame_timer >= 6:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
            self.frame_timer = 0
        
        self.rect.x += self.speed * self.direction

        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1

        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1

    def take_damage(self, amount):
        result = super().take_damage(amount)  # applique la logique de base (flash, invincibilité, mort)
        if self.alive:  # S’il est encore en vie, on déclenche la fuite
            self.flee_timer = 30
            self.direction *= -1  # facultatif : il fuit dans l’autre sens
        return result


class RoosterBoss(Animal):
    def __init__(self, pos, right_images, left_images, charge_right, charge_left, shoot_right, shoot_left):
        super().__init__(pos, right_images, left_images)
        self.health = 3
        self.speed = 3
        self.normal_speed = 3
        self.flee_speed = 10
        self.flee_timer = 0
        self.projectiles = []
        self.shooting = False
        self.shoot_timer = 0
        self.pre_attack_duration = 15
        self.shoot_direction = (0, 0)
        self.charge_right = charge_right
        self.charge_left = charge_left
        self.shoot_right = shoot_right
        self.shoot_left = shoot_left

        self.shoot_interval = random.randint(60, 120)
        self.flash_timer = 0
        self.invincibility_timer = 0
        self.last_damage_frame = -1000

        self.explosion_frames = [
            pygame.image.load("data/oeuf1.png").convert_alpha(),
            pygame.image.load("data/oeuf2.png").convert_alpha(),
            pygame.image.load("data/oeuf3.png").convert_alpha(),
            pygame.image.load("data/oeuf4.png").convert_alpha()
        ]

        self.frame = 0
        self.frame_timer = 0
        self.image = self.right_images[0]
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, wolf_rect=None, wolf=None, effects=None, current_frame=None):
        if not self.alive:
            for egg in self.projectiles:
                egg.update()
            self.projectiles = [e for e in self.projectiles if not e.finished]
            return

        # Gravité
        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        # Collisions avec les plateformes (comme dans Animal)
        self.on_ground = False
        if effects:  # on t'utilise déjà `effects` pour les bloods → c’est ta liste de plateformes
            for plat in effects:
                if self.rect.colliderect(plat):
                    if self.fall_speed >= 0 and self.rect.bottom <= plat.bottom:
                        self.rect.bottom = plat.top
                        self.fall_speed = 0
                        self.on_ground = True


        if self.flash_timer > 0:
            self.flee_timer = 30

        self.rect.x += self.speed * self.direction

        if self.flee_timer > 0:
            self.speed = self.flee_speed
            self.flee_timer -= 1
        elif random.random() < 0.01:
            self.direction *= -1
        else :
            self.speed = self.normal_speed

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right > LEVEL_WIDTH:
            self.rect.right = LEVEL_WIDTH
            self.direction = -1

        self.images = self.right_images if self.direction > 0 else self.left_images

        if not self.shooting:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame = (self.frame + 1) % len(self.images)
                
                self.frame_timer = 0
                self.set_image(self.images[self.frame])


        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        if self.shooting:
            self.shoot_timer -= 1
            if self.shoot_timer <= 0:
                egg = EggProjectile(self.rect.center, self.shoot_direction, self.explosion_frames)
                self.projectiles.append(egg)
                self.shooting = False
        else:
            self.shoot_interval -= 1
            if self.shoot_interval <= 0:
                if wolf_rect and abs(self.rect.centerx - wolf_rect.centerx) < 400:
                    dir_x = 1 if wolf_rect.centerx > self.rect.centerx else -1
                    dir_y = random.choice([-1, -2])
                    self.shoot_direction = (dir_x, dir_y)
                    self.shooting = True
                    self.shoot_timer = self.pre_attack_duration
                cooldown_map = {3: 90, 2: 60, 1: 30}
                base_cd = cooldown_map.get(self.health, 30)
                self.shoot_interval = base_cd + random.randint(0, 20)

        for egg in self.projectiles:
            egg.update()
            if wolf and egg.rect.colliderect(wolf.rect) and not egg.exploding:
                egg.explode()
                wolf.projectile_damage()

        self.projectiles = [egg for egg in self.projectiles if not egg.finished]

    def draw(self, screen, offset_x, offset_y):
        if self.alive:
            
            if self.shooting:
                if self.shoot_timer > 5:
                    self.set_image(self.charge_right if self.direction > 0 else self.charge_left)
                else:
                    self.set_image(self.shoot_right if self.direction > 0 else self.shoot_left)

            screen.blit(self.image, self.rect.move(-offset_x, -offset_y))
        for egg in self.projectiles:
            egg.draw(screen, offset_x, offset_y)

    def set_image(self, new_image):
        old_midbottom = self.rect.midbottom
        self.image = new_image
        self.rect = self.image.get_rect(midbottom=old_midbottom)
        

class Dog(Animal):
    def __init__(self, pos, right_walk, left_walk, jump_prep, jump_prep_left, jump_air, jump_air_left):
        self.attack_delay = 0
        self.attacking = False
        self.target_x = None
        self.target_y = None
        self.vel_x = 0
        self.vel_y = 0
        self.jump_duration = 30

        self.right_walk = right_walk
        self.left_walk = left_walk
        self.jump_prep = jump_prep
        self.jump_prep_left = jump_prep_left
        self.jump_air = jump_air
        self.jump_air_left = jump_air_left

        super().__init__(pos, right_walk, left_walk, speed=4, health=2)
        self.rect = self.image.get_rect(topleft=pos)
        self.jump_timer = random.randint(60, 180)

    def update(self, wolf, platforms):
        super().update(platforms)

        # Choix de l'image selon état
        if self.attacking and self.attack_delay > 0:
            self.image = self.jump_prep if self.direction > 0 else self.jump_prep_left
        elif self.target_x is not None and not self.attacking:
            self.image = self.jump_air if self.direction > 0 else self.jump_air_left
        else:
            self.images = self.right_walk if self.direction > 0 else self.left_walk
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame = (self.frame + 1) % len(self.images)
                self.image = self.images[self.frame]
                self.frame_timer = 0



        dx = wolf.rect.centerx - self.rect.centerx
        dy = wolf.rect.centery - self.rect.centery

        # Préparer l'attaque si le loup est proche
        if abs(dx) < 400 and abs(dy) < 150 and self.on_ground and not self.attacking and self.target_x is None:
            self.target_x = wolf.rect.centerx
            self.target_y = wolf.rect.centery
            self.attack_delay = 60  # 1 seconde
            self.attacking = True
            self.speed = 0

        elif self.attacking:
            self.attack_delay -= 1
            if self.attack_delay <= 0:
                # Calculer une trajectoire vers la position enregistrée
                dx = self.target_x - self.rect.centerx
                dy = self.target_y - self.rect.centery

                self.vel_x = dx / self.jump_duration
                self.vel_y = dy / self.jump_duration - 0.5 * self.gravity * self.jump_duration

                self.attacking = False
                self.speed = 0
                self.fall_speed = self.vel_y  # initialise la chute

        # Appliquer mouvement si trajectoire active
        if self.target_x is not None and not self.attacking:
            self.rect.x += int(self.vel_x)

            if abs(self.rect.centerx - self.target_x) < 10 and self.on_ground:
                self.target_x = None
                self.target_y = None
                self.speed = 4  # Reprend son déplacement normal

class PigBoss(Animal):
    def __init__(self, pos, walk_right, walk_left, charge_right, charge_left):
        super().__init__(pos, walk_right, walk_left, speed=2, health=4)
        self.walk_right_images = walk_right
        self.walk_left_images = walk_left
        self.charge_right_images = charge_right
        self.charge_left_images = charge_left
        self.is_charging = False
        self.custom_animation = True
        self.flee_timer = 0
        self.normal_speed = 2
        self.charge_speed = 7
        self.flee_speed = 10

    def take_damage(self, amount):
        result = super().take_damage(amount)
        if self.alive:
            self.flee_timer = 30  # 0.5s de fuite
            self.direction *= -1
        return result

    def update(self, wolf, platforms):
        if not self.alive:
            return

        # Appliquer la gravité et collisions
        super().update(platforms)

        dx = wolf.rect.centerx - self.rect.centerx
        dy = wolf.rect.centery - self.rect.centery

        if self.flee_timer > 0:
            self.speed = self.flee_speed
            self.flee_timer -= 1
            self.is_charging = False
        elif abs(dx) < 500 and abs(dy) < 100 and ((dx > 0 and self.direction > 0) or (dx < 0 and self.direction < 0)):
            self.speed = self.charge_speed
            self.is_charging = True
        else:
            self.speed = self.normal_speed
            self.is_charging = False

        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1

        # Choix des sprites
        if self.is_charging:
            self.images = self.charge_right_images if self.direction > 0 else self.charge_left_images
        else:
            self.images = self.walk_right_images if self.direction > 0 else self.walk_left_images

        # Animation
        if self.frame_timer >= 6 and not hasattr(self, 'custom_animation'):
            self.frame = (self.frame + 1) % len(self.images)
            bottom = self.rect.bottom
            centerx = self.rect.centerx
            self.image = self.images[self.frame]
            self.rect = self.image.get_rect(midbottom=(centerx, bottom)) 
            self.frame_timer = 0

        # Collision avec les bords
        if self.rect.left < 0 or self.rect.right > LEVEL_WIDTH:
            self.direction *= -1

        # Flash rouge si touché
        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1

    def crush_effect(self, wolf):
        wolf.take_damage(self)
        wolf.move_speed = 3
        wolf.jump = lambda: setattr(wolf, 'jump_speed', -6) or setattr(wolf, 'jumping', True)
        wolf.slowed_timer = 180  # 3 secondes
        wolf.hit_timer = 60
        wolf.right_images = wolf.squished_right_images
        wolf.left_images = wolf.squished_left_images
        self.direction *= -1

    def knockback(self):
        self.flee_timer = 15
        self.direction *= -1

class FinalBoss(Animal):
    def __init__(self, pos, walk_right, walk_left, jump_start_right, jump_start_left, jump_air_right, jump_air_left, attack_ground_right, attack_ground_left):
        # 3 phases : rouge, orange, violet
        self.phase = 1
        surface1 = pygame.Surface((50, 50), pygame.SRCALPHA)
        surface1.fill((255, 0, 0))  # Phase 1 : rouge
        surface2 = pygame.Surface((50, 50), pygame.SRCALPHA)
        surface2.fill((255, 165, 0))  # Phase 2 : orange
        surface3 = pygame.Surface((50, 50), pygame.SRCALPHA)
        surface3.fill((138, 43, 226))  # Phase 3 : violet

        self.phase_images = {
            1: [surface1],
            2: [surface2],
            3: [surface3]
        }

        self.projectiles = []  # Liste de projectiles de phase 2 (rect, vx, vy)

        self.walk_right = walk_right
        self.walk_left = walk_left
        self.jump_start_right = jump_start_right
        self.jump_start_left = jump_start_left
        self.jump_air_right = jump_air_right
        self.jump_air_left = jump_air_left
        self.attack_ground_right = attack_ground_right
        self.attack_ground_left = attack_ground_left

        super().__init__(pos, walk_right, walk_left, speed=2, health=6)


        self.direction = 1
        self.phase_changed = False

        self.attacking = False
        self.attack_cooldown = 180  # frames entre les attaques (~3 secondes)
        self.attack_cooldown_4 = 60
        self.attack_timer = 0
        self.attack_zone_active = False
        self.attack_zone_duration = 60  # durée visible de l'attaque de zone
        self.movement_locked = False
        self.has_jumped = False

        self.charging = False
        self.charge_timer = 0
        self.charge_speed = 17
        self.charge_cooldown = 180
        self.current_charge_time = 0
        self.max_charge_duration = 60  # durée max de la charge en frames
        self.walk_speed = 5  # vitesse normale
        self.speed = self.walk_speed  # valeur par défaut

        self.current_phase4_action = None
        self.phase4_action_done = False

        self.shake_on_impact = False


    def update(self, wolf=None, platforms=None):
        if not self.alive:
            return

        # Toujours appliquer la gravité
        self.fall_speed += self.gravity
        self.rect.y += self.fall_speed

        self.on_ground = False
        if platforms:
            for plat in platforms:
                if self.rect.colliderect(plat):
                    if self.fall_speed >= 0 and self.rect.bottom <= plat.bottom:
                        self.rect.bottom = plat.top
                        self.fall_speed = 0
                        self.on_ground = True

        # MOUVEMENT HORIZONTAL si pas en attaque
        if not self.movement_locked:
            if not hasattr(self, 'direction_timer'):
                self.direction_timer = 0

            self.direction_timer += 1
            if self.direction_timer > 30:
                if random.random() < 0.02:
                    self.direction *= -1
                self.direction_timer = 0

            self.rect.x += self.speed * self.direction

        # Empêche le boss de sortir du niveau
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction = 1
        elif self.rect.right > 1550:
            self.rect.right = 1550
            self.direction = -1

        # phase update
        if self.health <= 4 and self.phase == 1:
            self.phase = 2
            self.right_images = self.left_images = self.phase_images[2]
            self.speed = 3
        elif self.health <= 2 and self.phase == 2:
            self.phase = 3
            self.right_images = self.left_images = self.phase_images[3]
            self.speed = 4
        elif self.health <= 1 and self.phase == 3:
            self.phase = 4
            self.right_images = self.left_images = self.phase_images[3]
            self.speed = 5  # optionnel : vitesse plus élevée


        # Sélection dynamique du sprite
        if self.attack_zone_active and self.phase in [1, 2]:
            image = self.attack_ground_right if self.direction > 0 else self.attack_ground_left
            self.set_image(image)

        elif not self.on_ground and self.has_jumped:
            image = self.jump_air_right if self.direction > 0 else self.jump_air_left
            self.set_image(image)

        elif self.attacking and self.has_jumped:
            image = self.jump_start_right if self.direction > 0 else self.jump_start_left
            self.set_image(image)

        else:
            self.frame_timer += 1
            if self.frame_timer >= 10:
                self.frame = (self.frame + 1) % len(self.walk_right)
                image = self.walk_right[self.frame] if self.direction > 0 else self.walk_left[self.frame]
                self.set_image(image)
                self.frame_timer = 0



        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1
        if not hasattr(self, 'direction_timer'):
            self.direction_timer = 0

        self.direction_timer += 1
        if self.direction_timer > 30:  # toutes les 30 frames (~0.5s), possibilité de changer de sens
            if random.random() < 0.02:  # 2% de chance de changer de sens
                self.direction *= -1
            self.direction_timer = 0

        # Attaque spéciale
        if self.phase == 4:
            self.attack_phase_4(wolf)
        elif self.phase == 3:
            self.attack_phase_3(wolf)
        elif self.phase == 2:
            self.attack_phase_2(wolf)
        else:
            self.attack_phase_1(wolf)
        # Gestion visuelle de la zone d'attaque au sol
        if self.attack_zone_active:
            self.attack_zone_duration -= 1
            if self.attack_zone_duration <= 0:
                self.attack_zone_active = False
                self.attack_zone_duration = 60
                self.movement_locked = False

        # Mise à jour des projectiles (rebondit vers le bas)
        for proj in self.projectiles:
            rect, vx, vy = proj
            rect.x += vx
            #vy += 0.4  # gravité appliquée
            rect.y += vy
            proj[2] = vy  # on met à jour le vy dans la liste

        # Supprime les projectiles trop bas
        self.projectiles = [p for p in self.projectiles if p[0].y < 2000]

    def set_image(self, new_image):
        old_midbottom = self.rect.midbottom
        self.image = new_image
        self.rect = self.image.get_rect(midbottom=old_midbottom)

    def attack_phase_1(self, wolf):
        if not self.attacking:
            if self.attack_timer > 0:
                self.attack_timer -= 1
            elif self.on_ground:
                # Déclenche un saut vertical
                self.fall_speed = -20
                self.attacking = True
                self.movement_locked = True
                self.has_jumped = True  # nouvelle variable pour suivre le saut

        elif self.attacking:
            # On attend que le boss soit revenu au sol pour frapper
            if self.has_jumped and self.on_ground:
                self.attack_zone_active = True
                self.attacking = False
                self.attack_timer = self.attack_cooldown
                self.has_jumped = False
                self.shake_on_impact = True

    def attack_phase_2(self, wolf):
        if not self.attacking:
            if self.attack_timer > 0:
                self.attack_timer -= 1
            elif self.on_ground:
                self.fall_speed = -12
                self.attacking = True
                self.movement_locked = True
                self.has_jumped = True

        elif self.attacking and self.on_ground:
            self.attacking = False
            self.attack_timer = self.attack_cooldown
            self.movement_locked = False
            self.has_jumped = False

            # Lancer des projectiles à l’atterrissage
            for i in range(10):
                # Position légèrement aléatoire autour du haut du boss
                spawn_x = self.rect.centerx + random.randint(-30, 30)
                spawn_y = self.rect.bottom
                proj_rect = pygame.Rect(spawn_x, spawn_y, 10, 10)

                # Génère un angle uniquement vers le haut ou horizontal
                valid = False
                while not valid:
                    angle = random.uniform(0, 2 * math.pi)
                    speed = random.uniform(5, 9)
                    vx = math.cos(angle) * speed
                    vy = math.sin(angle) * speed

                    if vy <= 0:  # interdit les tirs vers le bas
                        valid = True

                self.projectiles.append([proj_rect, vx, vy])

    def attack_phase_3(self, wolf):
        if not self.charging:
            if self.charge_timer > 0:
                self.charge_timer -= 1
            else:
                self.charging = True
                self.movement_locked = True
                self.speed = self.charge_speed
                self.current_charge_time = 0
        else:
            # Charge en cours
            self.rect.x += self.speed * self.direction
            self.current_charge_time += 1

            # Rebonds aux limites
            if self.rect.left < 0:
                self.rect.left = 0
                self.direction = 1
                self._end_charge()
            elif self.rect.right > LEVEL_WIDTH:
                self.rect.right = LEVEL_WIDTH
                self.direction = -1
                self._end_charge()

            # Stop la charge si trop longue
            elif self.current_charge_time >= self.max_charge_duration:
                self._end_charge()

    def _end_charge(self):
        self.charging = False
        self.movement_locked = False
        self.charge_timer = self.charge_cooldown
        self.speed = self.walk_speed  # ← on remet la vitesse normale ici

    def attack_phase_4(self, wolf):
        self.speed = 7

        if self.current_phase4_action is None:
            if self.attack_timer > 0:
                self.attack_timer -= 1
            else:
                self.current_phase4_action = random.choice(["phase_1", "phase_2", "phase_3"])
                self.attacking = False
                self.charging = False
                self.movement_locked = False
                self.has_jumped = False
                self.current_charge_time = 0
                self.charge_timer = 0
        else:
            # Appelle dynamiquement la méthode de la phase choisie
            if self.current_phase4_action == "phase_1":
                self.attack_phase_1(wolf)
            elif self.current_phase4_action == "phase_2":
                self.attack_phase_2(wolf)
            elif self.current_phase4_action == "phase_3":
                self.attack_phase_3(wolf)

            # Une fois l’attaque terminée, on reset
            if not self.attacking and not self.charging:
                self.current_phase4_action = None
                self.attack_timer = self.attack_cooldown_4

class BossFemme(Animal):
    def __init__(self, pos, walk_right, walk_left, throw_right, throw_left):
        super().__init__(pos, walk_right, walk_left, speed=1, health=5)
        self.speed = 4
        self.walk_right = walk_right
        self.walk_left = walk_left
        self.throw_right = throw_right
        self.throw_left = throw_left

        self.projectiles = []
        self.shoot_cooldown = 300
        self.shoot_timer = self.shoot_cooldown

        self.shooting = False
        self.shoot_anim_timer = 0

    def update(self, wolf, platforms=None):
        if not self.alive:
            self.projectiles.clear()
            return

        super().update(platforms)

        # === Gestion du tir ===
        if self.shoot_timer <= 0:
            proj = self.create_homing_projectile(wolf)
            self.projectiles.append(proj)
            self.shoot_timer = self.shoot_cooldown
            self.shooting = True
            self.shoot_anim_timer = 30
        else:
            self.shoot_timer -= 1

        if self.shooting:
            self.shoot_anim_timer -= 1
            if self.shoot_anim_timer <= 0:
                self.shooting = False

        # Projectiles
        for proj in self.projectiles:
            proj.update(wolf.rect)

        self.projectiles = [p for p in self.projectiles if p.lifetime > 0]

    def draw(self, screen, offset_x, offset_y):
        if self.shooting:
            phase = (self.shoot_anim_timer // 8) % 2  # alterne toutes les 8 frames
            image = self.throw_right[phase] if self.direction > 0 else self.throw_left[phase]
        else:
            image = self.image

        screen.blit(image, self.rect.move(-offset_x, -offset_y))

        for proj in self.projectiles:
            proj.draw(screen, offset_x, offset_y)

    def create_homing_projectile(self, wolf):
        return HomingProjectile(self.rect.center, wolf.rect.center)