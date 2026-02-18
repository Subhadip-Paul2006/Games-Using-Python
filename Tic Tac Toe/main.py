import pygame
import sys
from db_manager import DBManager

pygame.init()

WIDTH, HEIGHT = 600, 700
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

FONT = pygame.font.Font(None, 40)
BIG_FONT = pygame.font.Font(None, 80)


player1_name = ""
player2_name = ""
current_player = 1
board = [[0] * 3 for _ in range(3)]
game_over = False
winner = None
db_manager = DBManager()

def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * 200 + 100), int(row * 200 + 100)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + 200 - SPACE), (col * 200 + 200 - SPACE, row * 200 + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + SPACE, row * 200 + SPACE), (col * 200 + 200 - SPACE, row * 200 + 200 - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
            
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_desc_diagonal(player)
        return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True

    return False


def draw_vertical_winning_line(col, player):
    posX = col * 200 + 100
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 100 - 15), 15)

def draw_horizontal_winning_line(row, player):
    posY = row * 200 + 100
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 100 - 15), (WIDTH - 15, 15), 15)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 100 - 15), 15)

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def input_screen():
    global player1_name, player2_name
    input_box1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
    input_box2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('gray15')
    color1 = color_active
    color2 = color_passive
    active1 = True
    active2 = False
    text1 = ''
    text2 = ''
    done = False
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = True
                    active2 = False
                elif input_box2.collidepoint(event.pos):
                    active1 = False
                    active2 = True
                else:
                    active1 = False
                    active2 = False
                color1 = color_active if active1 else color_passive
                color2 = color_active if active2 else color_passive
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                       active1 = False
                       active2 = True
                       color1 = color_passive
                       color2 = color_active
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif active2:
                    if event.key == pygame.K_RETURN:
                        if text1 and text2:
                            player1_name = text1
                            player2_name = text2
                            done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        screen.fill(BG_COLOR)
        
        title_surf = BIG_FONT.render("Enter Names", True, WHITE)
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 50))

        inst_surf = FONT.render("Press Enter to switch/confirm", True, WHITE)
        screen.blit(inst_surf, (WIDTH // 2 - inst_surf.get_width() // 2, HEIGHT - 100))

        
        label1 = FONT.render("Player 1 (O):", True, WHITE)
        screen.blit(label1, (WIDTH // 2 - 100, HEIGHT // 2 - 140))
        
        txt_surf1 = FONT.render(text1, True, WHITE)
        width1 = max(200, txt_surf1.get_width()+10)
        input_box1.w = width1
        pygame.draw.rect(screen, color1, input_box1, 2)
        screen.blit(txt_surf1, (input_box1.x+5, input_box1.y+10))
        
        label2 = FONT.render("Player 2 (X):", True, WHITE)
        screen.blit(label2, (WIDTH // 2 - 100, HEIGHT // 2 - 40))
        
        txt_surf2 = FONT.render(text2, True, WHITE)
        width2 = max(200, txt_surf2.get_width()+10)
        input_box2.w = width2
        pygame.draw.rect(screen, color2, input_box2, 2)
        screen.blit(txt_surf2, (input_box2.x+5, input_box2.y+10))
        
        pygame.display.flip()

def main():
    global current_player, game_over, winner, player1_name, player2_name

    input_screen()
    screen.fill(BG_COLOR)
    draw_lines()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.close()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                if mouseY < 600: # Only register clicks on the board
                    clicked_row = int(mouseY // 200)
                    clicked_col = int(mouseX // 200)

                    if available_square(clicked_row, clicked_col):
                        mark_square(clicked_row, clicked_col, current_player)
                        
                        if check_win(current_player):
                            game_over = True
                            winner_name = player1_name if current_player == 1 else player2_name
                            db_manager.log_game(player1_name, player2_name, winner_name) # Fixed variable name
                            winner = current_player 
                        
                        current_player = 2 if current_player == 1 else 1
                        draw_figures()
        
        if not game_over and winner is None:
            is_full = True
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board[row][col] == 0:
                        is_full = False
                        break
            if is_full:
                game_over = True
                winner = 0 # 0 for draw
                db_manager.log_game(player1_name, player2_name, "Draw")

        if game_over:
            if winner == 1:
                result_text = f"{player1_name} Wins!"
            elif winner == 2:
                result_text = f"{player2_name} Wins!"
            else:
                result_text = "It's a Draw!"
            
            text_surf = FONT.render(result_text, True, WHITE)
            screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, 630))
            
            restart_text = FONT.render("Press R to Restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 660))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and game_over:
            restart_game()
            game_over = False
            winner = None
            current_player = 1

        pygame.display.update()

if __name__ == "__main__":
    main()
