
import pygame
import random
import time
import math

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

        # Si le loup est devant lui et à portée → charge
        if abs(dx) < 500 and abs(dy) < 100 and ((dx > 0 and self.direction > 0) or (dx < 0 and self.direction < 0)):
            self.speed = 7
            self.is_charging = True
        else:
            self.speed = 3
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


        if self.flee_timer > 0:
            self.flee_timer -= 1
            if self.flee_timer == 0:
                self.speed = self.normal_speed

        self.rect.x += self.speed * self.direction


        if self.rect.left < 0 or self.rect.right > 1900:
            self.direction *= -1


        if self.flash_timer > 0:
            self.image = self.image.copy()
            red_overlay = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 100))
            self.image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1
            
    def knockback(self):
        self.flee_timer = 10
        self.direction *= -1
        self.speed = self.flee_speed


class EggProjectile:
    def __init__(self, pos, direction):
        self.image = pygame.image.load("data/oeuf.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed_x = 6 * direction[0]
        self.speed_y = 5 * direction[1]
        self.gravity = 0.3 if direction[1] != 0 else 0
        self.alive = True

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_y += self.gravity

        if self.rect.right < 0 or self.rect.left > 2000 or self.rect.top > 1200:
            self.alive = False

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.image, self.rect.move(-offset_x, -offset_y))

class RoosterBoss(Animal):
    def __init__(self, pos, right_images, left_images):
        super().__init__(pos, right_images, left_images)
        self.health = 3
        self.speed = 2.5
        self.normal_speed = 2.5
        self.flee_speed = 10
        self.flee_timer = 0
        self.projectiles = []
        self.shooting = False
        self.shoot_timer = 0
        self.pre_attack_duration = 15
        self.shoot_direction = (0, 0)
        self.charge_image = pygame.Surface((80, 80))
        self.charge_image.fill((255, 200, 200))

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

    def update(self, wolf_rect=None, wolf=None, effects=None):
        if not self.alive:
            for egg in self.projectiles:
                egg.update()
            self.projectiles = [e for e in self.projectiles if e.alive]
            return

        self.speed = self.flee_speed if self.flee_timer > 0 else self.normal_speed
        self.rect.x += self.speed * self.direction

        if self.flee_timer > 0:
            self.flee_timer -= 1
        elif random.random() < 0.01:
            self.direction *= -1

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
                self.image = self.images[self.frame]
                self.frame_timer = 0
                self.rect = self.image.get_rect(topleft=self.rect.topleft)

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
                self.projectiles.append(EggProjectile(self.rect.center, self.shoot_direction))
                self.shooting = False
        else:
            self.shoot_interval -= 1
            if self.shoot_interval <= 0:
                prob_map = {3: 30, 2: 60, 1: 90}
                shoot_chance = prob_map.get(self.health, 90)
                if random.randint(1, 100) <= shoot_chance:
                    if wolf_rect and abs(self.rect.centerx - wolf_rect.centerx) < 400:
                        dir_x = 1 if wolf_rect.centerx > self.rect.centerx else -1
                        dir_y = random.choice([0, -1])
                        self.shoot_direction = (dir_x, dir_y)
                        self.shooting = True
                        self.shoot_timer = self.pre_attack_duration
                cooldown_map = {3: 90, 2: 60, 1: 30}
                base_cd = cooldown_map.get(self.health, 30)
                self.shoot_interval = base_cd + random.randint(0, 20)

        for egg in self.projectiles[:]:
            egg.update()
            if wolf and egg.rect.colliderect(wolf.rect):
                egg.alive = False
                if wolf.hit_timer <= 0:
                    wolf.hp -= 1
                    wolf.hit_timer = 60
                    if effects is not None:
                        for i, frame in enumerate(self.explosion_frames):
                            rect = frame.get_rect(center=egg.rect.center)
                            effects.append((frame, rect.topleft, i * 3))
        self.projectiles = [e for e in self.projectiles if e.alive]

    def take_damage(self, amount, wolf_rect=None, current_frame=None, effects=None):
        if self.invincibility_timer > 0:
            return False

        if current_frame is not None and current_frame - self.last_damage_frame < 20:
            return False

        self.last_damage_frame = current_frame if current_frame is not None else 0

        self.health -= amount
        self.flash_timer = 6
        self.invincibility_timer = 30
        self.flee_timer = 20

        if self.health <= 0:
            self.alive = False
            if effects is not None:
                blood_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.circle(blood_surface, (180, 0, 0, 160), (30, 30), 30)
                effects.append((blood_surface, self.rect.center))
            return True

        if wolf_rect:
            self.direction = 1 if wolf_rect.centerx < self.rect.centerx else -1

        return False

    def draw(self, screen, offset_x, offset_y):
        if self.alive:
            image = self.charge_image if self.shooting else self.image
            screen.blit(image, self.rect.move(-offset_x, -offset_y))
        for egg in self.projectiles:
            egg.draw(screen, offset_x, offset_y)
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
        self.flee_timer = 0



    def update(self, wolf, platforms):
        if not self.alive:
            return

        # Appliquer la gravité et les collisions avec le sol
        super().update(platforms)

        dx = wolf.rect.centerx - self.rect.centerx
        dy = wolf.rect.centery - self.rect.centery

        # Détection pour enclencher la charge
        if abs(dx) < 500 and abs(dy) < 100 and ((dx > 0 and self.direction > 0) or (dx < 0 and self.direction < 0)):
            self.speed = 4
            self.is_charging = True
        else:
            self.speed = 2
            self.is_charging = False

        # Choix des sprites
        if self.is_charging:
            self.images = self.charge_right_images if self.direction > 0 else self.charge_left_images
        else:
            self.images = self.walk_right_images if self.direction > 0 else self.walk_left_images

        # Animation
        self.frame_timer += 1
        if self.frame_timer >= 15:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
            self.frame_timer = 0

        # Déplacement horizontal
        if self.flee_timer > 0:
            self.rect.x += 6 * self.direction  # vitesse de fuite
            self.flee_timer -= 1
        else:
            self.rect.x += self.speed * self.direction


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
    def __init__(self, pos):
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


        super().__init__(pos, self.phase_images[1], self.phase_images[1], speed=2, health=6)
        self.direction = 1
        self.phase_changed = False

        self.attacking = False
        self.attack_cooldown = 180  # frames entre les attaques (~3 secondes)
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

        self.images = self.right_images if self.direction > 0 else self.left_images

        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame = (self.frame + 1) % len(self.images)
            self.image = self.images[self.frame]
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

        # Attaque spéciale (phase 1 uniquement, mais tu peux adapter à chaque phase)
        if self.phase == 1:
            self.attack_phase_1(wolf)

        if self.phase == 2:
            self.attack_phase_2(wolf)

        if self.phase == 3:
            self.attack_phase_3(wolf)


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

