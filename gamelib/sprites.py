import pygame

class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.right_images = Wolf.right_images
        self.left_images = Wolf.left_images
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.level_width = 3100
        self.at_edge = False

        self.jump_speed = 0
        self.jump_accel = 0.6
        self.max_fall_speed = 14
        self.move_speed = 6
        self.jumping = False

        self.max_health = 3333
        self.health = 3333
        self.hit_timer = 0
        self.flash_timer = 0

        self.knockback_speed = 0
        self.knockback_direction = 0  # -1 = gauche, 1 = droite
        self.direction = 1

        self.frame = 0
        self.frame_timer = 0
        self._last_x = self.rect.x

        self.default_right_images = self.right_images.copy()
        self.default_left_images = self.left_images.copy()
        self.squished_right_images = [pygame.transform.scale(img, (img.get_width(), int(img.get_height() * 0.6))) for img in self.right_images]
        self.squished_left_images = [pygame.transform.flip(img, True, False) for img in self.squished_right_images]
        self.squished_sit_image_right = pygame.transform.scale(self.sit_image_right, (self.sit_image_right.get_width(), int(self.sit_image_right.get_height() * 0.6)))
        self.squished_sit_image_left = pygame.transform.scale(self.sit_image_left, (self.sit_image_left.get_width(), int(self.sit_image_left.get_height() * 0.6)))

    def move(self, dx, dy):
        self.at_edge = False  # reset à chaque déplacement

        # Gérer dx (horizontal)
        if self.rect.x + dx <= 0:
            self.rect.x = 0
            self.at_edge = True
            if self.jumping:
                self.rect.x += 2  # petit recul vers la droite
                self.jumping = False
        elif self.rect.x + dx >= self.level_width - 75:
            self.rect.x = self.level_width - 75
            self.at_edge = True
            if self.jumping:
                self.rect.x -= 2  # petit recul vers la gauche
                self.jumping = False
        else:
            self.rect.x += dx

        # Toujours appliquer dy
        self.rect.y += dy

    def jump(self):
        self.jump_speed = -13
        self.jumping = True

    def take_damage(self, enemy, level):
        level.son_loup_degat.play()
        if self.hit_timer <= 0:
            self.health -= 1
            self.hit_timer = 180  # 3 secondes d'invulnérabilité
            self.flash_timer = 6  # petit flash visuel
            self.knockback_speed = 12

            if enemy.rect.centerx < self.rect.centerx:
                self.knockback_direction = 1
            else:
                self.knockback_direction = -1

    def projectile_damage(self, level):
        level.son_loup_degat.play()
        if self.hit_timer <= 0:
            self.health -= 1
            self.hit_timer = 180  
            self.flash_timer = 6  

    def heal(self):
        if self.health < self.max_health:
            self.health += 1

    def update(self):
        if self.hit_timer > 0:
            self.hit_timer -= 1

        if self.knockback_speed > 0:
            self.rect.x += int(self.knockback_speed) * self.knockback_direction
            self.knockback_speed -= 1

        self.images = self.right_images if self.direction > 0 else self.left_images

        if self.at_edge:
            base_image = self.sit_image_right if self.direction > 0 else self.sit_image_left
        elif self.jumping:
            base_image = self.right_images[4] if self.direction > 0 else self.left_images[4]
        elif abs(self.rect.x - self._last_x) > 0:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame = (self.frame + 1) % len(self.images)
                self.frame_timer = 0
            base_image = self.images[self.frame]
        else:
            if hasattr(self, 'slowed_timer') and self.slowed_timer > 0:
                base_image = self.squished_sit_image_right if self.direction > 0 else self.squished_sit_image_left
            else:
                base_image = self.sit_image_right if self.direction > 0 else self.sit_image_left

        image = base_image.copy()

        # Flash rouge
        if self.flash_timer > 0:
            red_overlay = pygame.Surface(image.get_size(), flags=pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 80))
            image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1

        # Clignotement pendant invincibilité
        if self.hit_timer > 0 and (self.hit_timer // 5) % 2 == 0:
            image.set_alpha(128)
        else:
            image.set_alpha(255)

        self.image = image
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        self._last_x = self.rect.x