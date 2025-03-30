import pygame

class Wolf(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.right_images = Wolf.right_images
        self.left_images = Wolf.left_images
        self.images = self.right_images
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.jump_speed = 0
        self.jump_accel = 0.6
        self.max_fall_speed = 14
        self.move_speed = 6
        self.jumping = False

        self.max_health = 3
        self.health = 3
        self.hp = self.health
        self.hit_timer = 0
        self.flash_timer = 0

        self.knockback_speed = 0
        self.knockback_direction = 0  # -1 = gauche, 1 = droite
        self.direction = 1

        self.frame = 0
        self.frame_timer = 0
        self._last_x = self.rect.x

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        self.jump_speed = -13
        self.jumping = True

    def take_damage(self, enemy):
        if self.hit_timer <= 0:
            self.health -= 1
            self.hp = self.health
            self.hit_timer = 180  # 3 secondes d'invulnérabilité
            self.flash_timer = 6  # petit flash visuel
            self.knockback_speed = 12

            if enemy.rect.centerx < self.rect.centerx:
                self.knockback_direction = 1
            else:
                self.knockback_direction = -1

    def update(self):
        if self.hit_timer > 0:
            self.hit_timer -= 1

        if self.knockback_speed > 0:
            self.rect.x += int(self.knockback_speed) * self.knockback_direction
            self.knockback_speed -= 1

        self.images = self.right_images if self.direction > 0 else self.left_images

        if abs(self.rect.x - self._last_x) > 0:
            self.frame_timer += 1
            if self.frame_timer >= 6:
                self.frame = (self.frame + 1) % len(self.images)
                self.frame_timer = 0
        else:
            self.frame = 0

        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        # Flash blanc quand touché
        if self.flash_timer > 0:
            self.image = self.image.copy()
            self.image.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_ADD)
            self.flash_timer -= 1

        # Clignotement pendant invulnérabilité
        if self.hit_timer > 0 and (self.hit_timer // 5) % 2 == 0:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

        self._last_x = self.rect.x
