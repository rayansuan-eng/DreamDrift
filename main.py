import pygame
import sys
import os
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dream Drift")

# Load background
background_img = pygame.image.load(
    os.path.join("assets", "images", "background.png")
).convert()
background_img = pygame.transform.smoothscale(
    background_img, (WIDTH, HEIGHT)
)

# Overlay used only on the start and game-over screens
menu_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
menu_overlay.fill((0, 0, 0, 150))

# Load images
player_img = pygame.image.load(
    os.path.join("assets", "images", "player.png")
).convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))

moon_img = pygame.image.load(
    os.path.join("assets", "images", "moon_dream.png")
).convert_alpha()
moon_img = pygame.transform.scale(moon_img, (50, 50))

dreamcatcher_img = pygame.image.load(
    os.path.join("assets", "images", "dreamcatcher.png")
).convert_alpha()
dreamcatcher_img = pygame.transform.scale(dreamcatcher_img, (50, 50))

storm_img = pygame.image.load(
    os.path.join("assets", "images", "storm_cloud.png")
).convert_alpha()
storm_img = pygame.transform.scale(storm_img, (50, 50))

alarm_img = pygame.image.load(
    os.path.join("assets", "images", "alarm_clock.png")
).convert_alpha()
alarm_img = pygame.transform.scale(alarm_img, (50, 50))

# Sounds
pygame.mixer.init()
pygame.mixer.music.load(
    os.path.join("assets", "sounds", "background.mp3")
)
pygame.mixer.music.play(-1)

collect_sound = pygame.mixer.Sound(
    os.path.join("assets", "sounds", "collect.wav")
)
hit_sound = pygame.mixer.Sound(
    os.path.join("assets", "sounds", "hit.wav")
)

muted = False

# Colors
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Arial", 28)

# Player setup
player_radius = 25
player_x = WIDTH // 2
player_y = 100
player_speed = 5

# Score, lives, level
score = 0
lives = 3
level = 1
level_up_flash_timer = 0
max_level = 6
last_level_up_score = 0
last_burst_time = time.time()


# Object burst
def burst_objects(num=5):
    for _ in range(num):
        falling_objects.append(FallingObject())


# Falling object class
class FallingObject:
    def __init__(self):
        self.radius = 20
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = HEIGHT + self.radius
        self.is_good = random.choice([True, False])

        if self.is_good:
            self.type = random.choice(["moon", "dreamcatcher"])
        else:
            self.type = random.choice(["alarm", "storm"])

        if level < 4:
            self.speed = random.randint(2 + level, 3 + level)
        else:
            self.speed = random.randint(4, 5)

    def update(self):
        self.y -= self.speed

    def draw(self):
        if self.type == "moon":
            img = moon_img
        elif self.type == "dreamcatcher":
            img = dreamcatcher_img
        elif self.type == "alarm":
            img = alarm_img
        else:
            img = storm_img

        screen.blit(img, (self.x - 20, self.y - 20))

    def collides_with_player(self, px, py, pradius):
        dx = self.x - px
        dy = self.y - py
        return (dx**2 + dy**2)**0.5 < self.radius + pradius


# Object list and timers
falling_objects = []
spawn_timer = 0
burst_cooldown = random.randint(10, 15)


# Start screen
def show_start():
    screen.blit(background_img, (0, 0))
    screen.blit(menu_overlay, (0, 0))

    title = pygame.font.SysFont("Arial", 60, bold=True).render(
        "DreamDrift", True, TEXT_COLOR
    )
    instructions = font.render(
        "Catch good dreams, avoid nightmares.", True, TEXT_COLOR
    )
    prompt = font.render(
        "Press any key to start", True, (200, 200, 255)
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100)
    )
    screen.blit(
        instructions,
        (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2)
    )
    screen.blit(
        prompt,
        (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 50)
    )
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return


# Game over screen
def show_game_over(score):
    screen.blit(background_img, (0, 0))
    screen.blit(menu_overlay, (0, 0))

    title = pygame.font.SysFont("Arial", 60, bold=True).render(
        "Game Over", True, (255, 80, 80)
    )
    final_score = font.render(
        f"Final Score: {score}", True, TEXT_COLOR
    )
    prompt = font.render(
        "Press R to restart or Q to quit", True, (200, 200, 255)
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100)
    )
    screen.blit(
        final_score,
        (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2)
    )
    screen.blit(
        prompt,
        (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 50)
    )
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return


# Game start
show_start()
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # Full-brightness background during gameplay
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                muted = not muted
                if muted:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x - player_radius > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x + player_radius < WIDTH:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y - player_radius > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y + player_radius < HEIGHT:
        player_y += player_speed

    if score >= last_level_up_score + 10 and level < max_level:
        level += 1
        last_level_up_score = score
        burst_objects(5)
        level_up_flash_timer = 60

    if level == max_level:
        now = time.time()
        if now - last_burst_time > burst_cooldown:
            burst_objects(3)
            last_burst_time = now
            burst_cooldown = random.randint(10, 15)

    spawn_timer += 1
    if spawn_timer >= max(10, 90 - level * 10):
        falling_objects.append(FallingObject())
        spawn_timer = 0

    for obj in falling_objects[:]:
        obj.update()
        obj.draw()

        if obj.collides_with_player(player_x, player_y, player_radius):
            if obj.is_good:
                score += 1
                if not muted:
                    collect_sound.play()
            else:
                lives -= 1
                if not muted:
                    hit_sound.play()

            falling_objects.remove(obj)

        elif obj.y < -obj.radius:
            falling_objects.remove(obj)

    screen.blit(player_img, (player_x - 25, player_y - 25))

    screen.blit(
        font.render(f"Score: {score}", True, TEXT_COLOR),
        (10, 10)
    )
    screen.blit(
        font.render(f"Lives: {lives}", True, TEXT_COLOR),
        (WIDTH - 150, 10)
    )

    if level < max_level:
        level_text = f"Level: {level}"
    else:
        level_text = "Max Level"

    screen.blit(
        font.render(level_text, True, TEXT_COLOR),
        (WIDTH // 2 - 60, 10)
    )

    if level_up_flash_timer > 0:
        flash_font = pygame.font.SysFont("Arial", 32, bold=True)
        flash_text = flash_font.render(
            "Level Up!" if level < max_level else "Max Level!",
            True,
            (255, 255, 100)
        )
        screen.blit(flash_text, (player_x - 40, player_y - 60))
        level_up_flash_timer -= 1

    if lives <= 0:
        show_game_over(score)
        player_x, player_y = WIDTH // 2, 100
        score = 0
        lives = 3
        level = 1
        last_level_up_score = 0
        falling_objects.clear()
        spawn_timer = 0
        last_burst_time = time.time()

    pygame.display.flip()

pygame.quit()
sys.exit()