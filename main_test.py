import pygame
from gamelib.sprites import Wolf

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bad Wolf – Test Zone")
clock = pygame.time.Clock()

# Définir des images temporaires
Wolf.right_images = [pygame.Surface((50, 50)) for _ in range(6)]
for surf in Wolf.right_images:
    surf.fill((120, 120, 120))

# Supprimer les appels à load_sound dans Wolf
Wolf.jump_sound = None
Wolf.hit_sound = None
Wolf.spring_sound = None

# Création du loup et des plateformes
wolf = Wolf((150, 300))
platforms = [
    pygame.Rect(100, 500, 300, 30),
    pygame.Rect(450, 400, 150, 30),
    pygame.Rect(650, 300, 100, 30)
]

# Création d'un ennemi
enemy = pygame.Rect(400,460,50,50)
enemy_color = (200,50,50)

# Cœurs de vie (carrés rouges pour l’instant)
heart_image = pygame.Surface((30, 30))
heart_image.fill((255, 0, 0))

# Boucle principale
running = True
while running:
    screen.fill((135, 206, 235))  # ciel bleu

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        dx = -5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = 5
    if (keys[pygame.K_SPACE] or keys[pygame.K_z] or keys[pygame.K_w] or keys[pygame.K_UP]) and not wolf.jumping:
        wolf.jump()

    wolf.move(dx, 0)

    # Appliquer gravité
    wolf.jump_speed += wolf.jump_accel
    if wolf.jump_speed > 10:
        wolf.jump_speed = 10
    wolf.move(0, wolf.jump_speed)

    # Collision avec plateformes
    wolf.jumping = True
    for platform in platforms:
        if wolf.rect.colliderect(platform) and wolf.jump_speed >= 0:
            wolf.rect.bottom = platform.top
            wolf.jump_speed = 0
            wolf.jumping = False
            break

    # Collision avec l’ennemi
    if wolf.rect.colliderect(enemy):
        wolf.hit_timer -= 1
        if wolf.hit_timer <= 0:
            wolf.hp -= 1
            wolf.hit_timer = 60  # délai entre 2 dégâts
            print(f"Ouch ! Il te reste {wolf.hp} cœur(s).")
            if wolf.hp <= 0:
                print("Game Over 🐺💀")
                running = False
    else:
        wolf.hit_timer = max(wolf.hit_timer - 1, 0)



    # Dessin
    for plat in platforms:
        pygame.draw.rect(screen, (100, 100, 100), plat)

    wolf.update()
    screen.blit(wolf.image, wolf.rect)

    for i in range(wolf.hp):
        screen.blit(heart_image, (10 + i * 35, 10))

    pygame.draw.rect(screen, enemy_color, enemy)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
