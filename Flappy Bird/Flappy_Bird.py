import pygame
import random

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# ---------- LOAD SOUNDS ----------
flap_sound = pygame.mixer.Sound("flap.wav")
point_sound = pygame.mixer.Sound("point.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
die_sound = pygame.mixer.Sound("die.wav")
swoosh_sound = pygame.mixer.Sound("swoosh.wav")

flap_sound.set_volume(0.5)
point_sound.set_volume(0.5)
hit_sound.set_volume(0.6)
die_sound.set_volume(0.7)
swoosh_sound.set_volume(0.4)

# ---------- BIRD SPRITES ----------
bird_up = pygame.image.load("flappy_up.png").convert_alpha()
bird_down = pygame.image.load("flappy_down.png").convert_alpha()
bird_up = pygame.transform.scale(bird_up, (40, 30))
bird_down = pygame.transform.scale(bird_down, (40, 30))

bird_x = 80
bird_y = HEIGHT // 2
velocity = 0
gravity = 0.4

wing_timer = 0
wing_state = "up"   

# ---------- COIN SPRITE ----------
coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (40, 40))
coin_x = -100  # Start off-screen to the left
coin_y = random.randint(200, 300)
coin_visible = False  # Start invisible
coin_spawned = False  # Track if coin has been spawned for current pipe cycle

# ---------- GAME STATE ----------
game_started = False
game_over = False
death_time = 0

# ---------- PIPES ----------
pipe_width = 60
pipe_x = WIDTH
pipe_gap = 150
top_height = random.randint(100, 350)

# ---------- SCORE ----------
score = 0
passed_pipe = False
font = pygame.font.SysFont("Arial", 40)
big_font = pygame.font.SysFont("Arial", 60)

# ---------- CLOUDS ----------
WHITE = (255, 255, 255)
clouds = []
for _ in range(4):
    clouds.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT // 2),
        random.uniform(0.5, 1.5)
    ])

def draw_cloud(x, y):
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), 20)
    pygame.draw.circle(screen, WHITE, (int(x + 25), int(y - 10)), 25)
    pygame.draw.circle(screen, WHITE, (int(x + 55), int(y)), 20)
    pygame.draw.circle(screen, WHITE, (int(x + 25), int(y + 10)), 20)

# ---------- GAME LOOP ----------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_started:
                game_started = True
                velocity = 0
                swoosh_sound.play()
            else:
                velocity = -7
                flap_sound.play()

    if game_started and not game_over:
        velocity += gravity
        bird_y += velocity
        pipe_x -= 3
        if coin_spawned:  # Only move coin if it's been spawned
            coin_x -= 3

    # Wing animation
    wing_timer += 1
    if wing_timer > 8:
        wing_state = "down" if wing_state == "up" else "up"
        wing_timer = 0

    # Pipe scoring
    if (pipe_x + pipe_width) < bird_x and not passed_pipe and game_started and not game_over:
        score += 1
        passed_pipe = True
        point_sound.play()

    # Reset pipe & coin
    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        top_height = random.randint(100, 350)
        passed_pipe = False

        # 80% chance to spawn a coin
        if random.random() < 0.8:
            # Spawn coin in the space between the old pipe position and new pipe
            coin_x = WIDTH + 150  # Position after the new pipe
            coin_y = random.randint(100, HEIGHT - 100)  # Random height
            coin_visible = True
            coin_spawned = True
        else:
            coin_visible = False
            coin_spawned = False
            coin_x = -100  # Move off-screen

    # Hide coin if it goes off screen to the left
    if coin_x < -50:
        coin_visible = False
        coin_spawned = False

    # Collision rectangles
    bird_rect = pygame.Rect(bird_x, bird_y, 40, 30)
    top_pipe_rect = pygame.Rect(pipe_x, 0, pipe_width, top_height)
    bottom_pipe_rect = pygame.Rect(pipe_x, top_height + pipe_gap,
                                   pipe_width, HEIGHT)
    
    # ---------- COIN COLLISION (+5 POINTS) ----------
    # Only check collision if coin is spawned and visible
    if coin_visible and coin_spawned:
        coin_rect = pygame.Rect(coin_x, coin_y, 40, 40)
        if bird_rect.colliderect(coin_rect):
            score += 5
            coin_visible = False
            coin_spawned = False
            point_sound.play()

    # ---------- DEATH COLLISION ----------
    if game_started and not game_over:
        if (bird_rect.colliderect(top_pipe_rect)
            or bird_rect.colliderect(bottom_pipe_rect)
            or bird_y <= 0
            or bird_y + 30 >= HEIGHT):

            hit_sound.play()
            pygame.time.delay(150)
            die_sound.play()
            game_over = True
            death_time = pygame.time.get_ticks()

    # ---------- DRAW ----------
    screen.fill((28, 226, 240))

    # Clouds
    for cloud in clouds:
        draw_cloud(cloud[0], cloud[1])
        cloud[0] += cloud[2]
        if cloud[0] > WIDTH + 60:
            cloud[0] = random.randint(-200, -60)
            cloud[1] = random.randint(0, HEIGHT // 2)

    # Pipes
    pygame.draw.rect(screen, (82, 220, 82), (pipe_x, 0, pipe_width, top_height))
    pygame.draw.rect(screen, (82, 220, 82),
                     (pipe_x, top_height + pipe_gap, pipe_width, HEIGHT))

    # Coin
    if coin_visible and coin_spawned:
        screen.blit(coin_img, (coin_x, coin_y))

    # Bird
    if wing_state == "up":
        screen.blit(bird_up, (bird_x, bird_y))
    else:
        screen.blit(bird_down, (bird_x, bird_y))

    # Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Start screen
    if not game_started:
        start_text = font.render("Press SPACE to Start", True, (0, 0, 0))
        screen.blit(start_text, (WIDTH // 2 - 170, HEIGHT // 2 - 20))

    # Game over screen
    if game_over:
        lose_text = big_font.render("YOU LOSE", True, (255, 0, 0))
        final_score = font.render(f"Final Score: {score}", True, (0, 0, 0))
        screen.blit(lose_text, (WIDTH // 2 - 130, HEIGHT // 2 - 80))
        screen.blit(final_score, (WIDTH // 2 - 110, HEIGHT // 2 - 20))

        if pygame.time.get_ticks() - death_time > 5000:
            running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()