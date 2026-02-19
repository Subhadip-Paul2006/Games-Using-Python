"""
SNAKE GAME WITH POSTGRESQL DATABASE INTEGRATION & PYGAME 

DATABASE SETUP:
Ensure PostgreSQL is running with the following configuration:
Database: <Use Your>
Table: <Use Your>
Host: <Use Your>
Port: <Use Your>
User: <Use Your>
Password: <Use Your>

CONTROLS:
W = Up
A = Left
S = Down
D = Right
ENTER = Start Game
"""

import pygame
import random
import time
import sys
import psycopg2
from psycopg2 import Error

# Game setup & constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
FPS = 10

# Colors used inside the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
DARK_GREEN = (0, 155, 0)

# Snake colors (from head to tail)
CYAN = (0, 255, 255)
TEAL = (0, 200, 200)
SKY_BLUE = (135, 206, 235)
PURPLE = (150, 100, 255)
MAGENTA = (200, 50, 200)

# Food colors
BRIGHT_RED = (255, 50, 50)
ORANGE_RED = (255, 69, 0)

# Database Configuration and passwords
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'snake_game_db',
    'user': 'postgres',
    'password': 'subh06'
}

def get_db_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None


def fetch_high_score():
    connection = get_db_connection()
    if not connection:
        return 0
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(score) FROM snake_game_scores")
        result = cursor.fetchone()
        high_score = result[0] if result[0] is not None else 0
        cursor.close()
        connection.close()
        return high_score
    except Error as e:
        print(f"Error fetching high score: {e}")
        if connection:
            connection.close()
        return 0


def save_score_to_db(player_name, score, high_score):
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
        is_new_high_score = score > high_score
        
        if is_new_high_score:
            cursor.execute("UPDATE snake_game_scores SET is_high_score = FALSE WHERE is_high_score = TRUE")
        
        cursor.execute("""INSERT INTO snake_game_scores (player_name, score, is_high_score, played_at)VALUES (%s, %s, %s, NOW())""", (player_name, score, is_new_high_score))
        
        connection.commit()
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error saving score to database: {e}")
        if connection:
            connection.rollback()
            connection.close()


def draw_text(surface, text, size, x, y, color=WHITE, align='left'):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if align == 'center':
        text_rect.center = (x, y)
    elif align == 'right':
        text_rect.right = x
        text_rect.top = y
    else: 
        text_rect.left = x
        text_rect.top = y
    
    surface.blit(text_surface, text_rect)


def draw_circle_cell(surface, x, y, color, outline_color=None):
    center_x = x * GRID_SIZE + GRID_SIZE // 2
    center_y = y * GRID_SIZE + GRID_SIZE // 2
    radius = GRID_SIZE // 2 - 2
    
    pygame.draw.circle(surface, color, (center_x, center_y), radius)
    
    if outline_color:
        pygame.draw.circle(surface, outline_color, (center_x, center_y), radius, 2)


def spawn_food(snake_body):
    while True:
        food_x = random.randint(0, GRID_WIDTH - 1)
        food_y = random.randint(0, GRID_HEIGHT - 1)
        if [food_x, food_y] not in snake_body:
            return [food_x, food_y]


def spawn_bonus_food(snake_body, normal_food):
    while True:
        bonus_x = random.randint(0, GRID_WIDTH - 1)
        bonus_y = random.randint(0, GRID_HEIGHT - 1)
        if [bonus_x, bonus_y] not in snake_body and [bonus_x, bonus_y] != normal_food:
            return [bonus_x, bonus_y]


def show_start_screen(screen, high_score):
    player_name = ""
    input_active = True
    clock = pygame.time.Clock()
    
    while input_active:
        screen.fill(BLACK)
        
        draw_text(screen, "SNAKE GAME", 80, WINDOW_WIDTH // 2, 100, GREEN, 'center')
        
        draw_text(screen, f"High Score: {high_score}", 40, WINDOW_WIDTH // 2, 180, GOLD, 'center')
        
        draw_text(screen, "Enter Your Name:", 40, WINDOW_WIDTH // 2, 260, WHITE, 'center')
        
        input_box = pygame.Rect(WINDOW_WIDTH // 2 - 150, 320, 300, 50)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        draw_text(screen, player_name, 36, WINDOW_WIDTH // 2, 345, WHITE, 'center')
        
        draw_text(screen, "CONTROLS:", 36, WINDOW_WIDTH // 2, 420, YELLOW, 'center')
        draw_text(screen, "W = Up  |  A = Left  |  S = Down  |  D = Right", 30, WINDOW_WIDTH // 2, 460, WHITE, 'center')
        
        draw_text(screen, "Press ENTER to Start", 32, WINDOW_WIDTH // 2, 520, GREEN, 'center')
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif len(player_name) < 20 and event.unicode.isprintable():
                    player_name += event.unicode
        
        clock.tick(30)
    
    return player_name


def show_game_over_screen(screen, player_name, score, high_score):
    screen.fill(BLACK)
    
    draw_text(screen, "GAME OVER!", 80, WINDOW_WIDTH // 2, 150, RED, 'center')
    
    # Player info and storing 
    draw_text(screen, f"Player: {player_name}", 40, WINDOW_WIDTH // 2, 250, WHITE, 'center')
    draw_text(screen, f"Your Score: {score}", 50, WINDOW_WIDTH // 2, 310, YELLOW, 'center')
    
    if score > high_score:
        draw_text(screen, "NEW HIGH SCORE!", 60, WINDOW_WIDTH // 2, 380, GOLD, 'center')
    else:
        draw_text(screen, f"High Score: {high_score}", 40, WINDOW_WIDTH // 2, 380, GOLD, 'center')
    
    draw_text(screen, "Closing in 5 seconds...", 30, WINDOW_WIDTH // 2, 480, WHITE, 'center')
    
    pygame.display.flip()
    time.sleep(5)

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    high_score = fetch_high_score()
    
    player_name = show_start_screen(screen, high_score)
    
    snake_body = [[GRID_WIDTH // 2, GRID_HEIGHT // 2]]
    direction = [1, 0]  
    next_direction = [1, 0]
    
    food = spawn_food(snake_body)
    score = 0
    
    bonus_food = None
    bonus_active = False
    bonus_spawn_time = time.time() + random.uniform(7, 10)
    bonus_disappear_time = 0
    
    game_running = True
    
    while game_running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != [0, 1]:
                    next_direction = [0, -1]
                elif event.key == pygame.K_s and direction != [0, -1]:
                    next_direction = [0, 1]
                elif event.key == pygame.K_a and direction != [1, 0]:
                    next_direction = [-1, 0]
                elif event.key == pygame.K_d and direction != [-1, 0]:
                    next_direction = [1, 0]
        
        direction = next_direction
        
        new_head = [snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]]
        
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            game_running = False
            continue
        
        if new_head in snake_body:
            game_running = False
            continue
        
        snake_body.insert(0, new_head)
        
        if new_head == food:
            score += 10
            food = spawn_food(snake_body)
        elif bonus_active and new_head == bonus_food:
            score += 50  # Bonus points
            bonus_active = False
            bonus_food = None
        else:
            snake_body.pop()
        
        if not bonus_active and current_time >= bonus_spawn_time:
            bonus_food = spawn_bonus_food(snake_body, food)
            bonus_active = True
            bonus_disappear_time = current_time + random.uniform(2.5, 3.5) 
        
        if bonus_active and current_time >= bonus_disappear_time:
            bonus_active = False
            bonus_food = None
            bonus_spawn_time = current_time + random.uniform(7, 10)
        
        screen.fill(BLACK)
        
        # Drawing snake with gradient colors
        for i, segment in enumerate(snake_body):
            if i == 0:
                # Head - brightest cyan
                draw_circle_cell(screen, segment[0], segment[1], CYAN, WHITE)
            else:
                # Body - gradient from teal to purple
                progress = i / max(len(snake_body) - 1, 1)
                r = int(TEAL[0] + (PURPLE[0] - TEAL[0]) * progress)
                g = int(TEAL[1] + (PURPLE[1] - TEAL[1]) * progress)
                b = int(TEAL[2] + (PURPLE[2] - TEAL[2]) * progress)
                draw_circle_cell(screen, segment[0], segment[1], (r, g, b))
        
        # Drawing normal food
        draw_circle_cell(screen, food[0], food[1], BRIGHT_RED, ORANGE_RED)
        
        # Drawing the bonus food with pulsing effect in time interval
        if bonus_active and bonus_food:
            pulse = abs(int((current_time * 5) % 2) - 1)  # Creates pulsing effect
            bonus_color = (255, 215 + pulse * 40, 0)
            draw_circle_cell(screen, bonus_food[0], bonus_food[1], bonus_color, YELLOW)
        
        draw_text(screen, f"Score: {score}", 30, 10, 10, WHITE)
        
        current_high = max(high_score, score)
        draw_text(screen, f"High Score: {current_high}", 30, WINDOW_WIDTH - 10, 10, GOLD, 'right')
        
        pygame.display.flip()
        clock.tick(FPS)
    
    save_score_to_db(player_name, score, high_score)
    
    final_high_score = max(high_score, score)
    show_game_over_screen(screen, player_name, score, high_score)
    
    pygame.quit()



if __name__ == "__main__":
    run_game()
