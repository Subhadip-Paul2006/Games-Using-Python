import pygame
import random
import sys
import math

#########################################################
## File Name: main.py
## Description: Modern UI Overhaul for Hangman
#########################################################

pygame.init()
pygame.mixer.init()

# Setup Display
WIN_WIDTH = 800
WIN_HEIGHT = 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Hangman")
clock = pygame.time.Clock()

# ---------------------------------------
# Colors - Modern Dark Theme
# ---------------------------------------
BG_COLOR = (30, 30, 46)          # Catppuccin Mocha Base
PANEL_COLOR = (49, 50, 68)       # Surface color
HIGHLIGHT = (166, 227, 161)      # Green (Win/Correct)
ERROR_COLOR = (243, 139, 168)    # Red (Loss/Wrong)
TEXT_COLOR = (205, 214, 244)     # White text
BTN_DEFAULT = (69, 71, 90)       # Button resting
BTN_HOVER = (88, 91, 112)        # Button hovered
DISABLED_COLOR = (24, 24, 37)    # Disabled button
WHITE = (255, 255, 255)

# ---------------------------------------
# Fonts
# ---------------------------------------
title_font = pygame.font.SysFont("trebuchetms", 60, bold=True)
guess_font = pygame.font.SysFont("monospace", 40, bold=True)
btn_font = pygame.font.SysFont("arial", 22, bold=True)
info_font = pygame.font.SysFont("arial", 18)
msg_font = pygame.font.SysFont("trebuchetms", 45, bold=True)

# ---------------------------------------
# Assets & Sounds
# ---------------------------------------
hangmanPics = [
    pygame.image.load('hangman0.png').convert_alpha(),
    pygame.image.load('hangman1.png').convert_alpha(),
    pygame.image.load('hangman2.png').convert_alpha(),
    pygame.image.load('hangman3.png').convert_alpha(),
    pygame.image.load('hangman4.png').convert_alpha(),
    pygame.image.load('hangman5.png').convert_alpha(),
    pygame.image.load('hangman6.png').convert_alpha()
]

# Sounds (Fail gracefully if not present)
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

snd_correct = load_sound('Correct.wav')
snd_wrong = load_sound('Wrong.wav')
snd_win = load_sound('Win.wav')
snd_loose = load_sound('Loose.wav')

# ---------------------------------------
# Game State Variables
# ---------------------------------------
STATE_START = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2

current_state = STATE_START
word = ''
guessed_letters = []
limbs = 0
buttons = []  # will store dicts: {'char': 'A', 'rect': Rect, 'visible': True, 'hover': False}
game_won = False

# Animation vars
letter_pop_time = 0
last_guess_correct = False
anim_time = 0

def randomWord():
    try:
        with open('words.txt') as file:
            f = file.readlines()
        if not f: return "ERROR"
        i = random.randrange(0, len(f))
        return f[i].strip().upper()
    except Exception:
        return "PYTHON"

def reset_game():
    global word, guessed_letters, limbs, buttons, game_won, current_state
    word = randomWord()
    guessed_letters = []
    limbs = 0
    game_won = False
    
    # Setup onscreen keyboard (A-Z)
    buttons.clear()
    start_x = (WIN_WIDTH - (13 * 50)) // 2 + 10 # Center keyboard
    start_y = 450
    for i in range(26):
        row = i // 13
        col = i % 13
        x = start_x + (col * 50)
        y = start_y + (row * 60)
        buttons.append({
            'char': chr(65 + i),
            'rect': pygame.Rect(x, y, 40, 40),
            'visible': True,
            'hover': False
        })
    current_state = STATE_PLAYING

def play_sound(snd):
    if snd: snd.play()

def handle_guess(letter):
    global limbs, game_won, current_state, letter_pop_time, last_guess_correct
    if current_state != STATE_PLAYING: return
    
    letter = letter.upper()
    
    # Disable button
    for btn in buttons:
        if btn['char'] == letter and btn['visible']:
            btn['visible'] = False
            guessed_letters.append(letter)
            
            # Check logic
            if letter in word:
                play_sound(snd_correct)
                last_guess_correct = True
                letter_pop_time = pygame.time.get_ticks()
                if check_win():
                    game_won = True
                    current_state = STATE_GAME_OVER
                    play_sound(snd_win)
            else:
                play_sound(snd_wrong)
                last_guess_correct = False
                letter_pop_time = pygame.time.get_ticks()
                limbs += 1
                if limbs >= 6:
                    game_won = False
                    current_state = STATE_GAME_OVER
                    play_sound(snd_loose)
            break

def check_win():
    for char in word:
        if char != ' ' and char not in guessed_letters:
            return False
    return True

def draw_gradient_bg():
    # Subtle vertical gradient background
    color1 = pygame.Color(BG_COLOR)
    color2 = pygame.Color(17, 17, 27) # Darker crust color
    for y in range(WIN_HEIGHT):
        blend = y / WIN_HEIGHT
        r = int(color1.r * (1 - blend) + color2.r * blend)
        g = int(color1.g * (1 - blend) + color2.g * blend)
        b = int(color1.b * (1 - blend) + color2.b * blend)
        pygame.draw.line(win, (r, g, b), (0, y), (WIN_WIDTH, y))

def draw_hangman_box():
    # Draw a lighter glowing box so the black line-art hangman stands out
    box_rect = pygame.Rect(WIN_WIDTH//2 - 120, 100, 240, 260)
    
    # Glow/Shadow logic
    glow_surface = pygame.Surface((260, 280), pygame.SRCALPHA)
    pygame.draw.rect(glow_surface, (255, 255, 255, 10), glow_surface.get_rect(), border_radius=15)
    win.blit(glow_surface, (box_rect.x - 10, box_rect.y - 10))
    
    # White/Light panel
    pygame.draw.rect(win, (220, 224, 232), box_rect, border_radius=15)
    
    # Draw hangman
    pic = hangmanPics[limbs]
    pic_rect = pic.get_rect(center=box_rect.center)
    win.blit(pic, pic_rect)

def draw_info_panel():
    survive_text = info_font.render(f"Mistakes Left: {6 - limbs}", True, HIGHLIGHT if limbs < 4 else ERROR_COLOR)
    win.blit(survive_text, (20, 20))

def get_spaced_word():
    display = ""
    for char in word:
        if char == ' ':
            display += "  "
        elif char in guessed_letters:
            display += char + " "
        else:
            display += "_ "
    return display.strip()

def draw_playing():
    draw_hangman_box()
    draw_info_panel()
    
    # Draw Title
    title = title_font.render("HANGMAN", True, HIGHLIGHT)
    win.blit(title, (WIN_WIDTH//2 - title.get_width()//2, 20))
    
    # Draw Word Spaces
    # Animation effects on guess
    scale_y = 0
    now = pygame.time.get_ticks()
    diff = now - letter_pop_time
    if diff < 200: # 200ms animation
        scale_y = math.sin(diff / 200.0 * math.pi) * 10
        if not last_guess_correct:
            scale_y = -scale_y
            
    spaced_str = get_spaced_word()
    word_surf = guess_font.render(spaced_str, True, TEXT_COLOR)
    word_rect = word_surf.get_rect(center=(WIN_WIDTH//2, 400 + scale_y))
    win.blit(word_surf, word_rect)
    
    # Draw Keyboard Buttons
    for btn in buttons:
        color = BTN_HOVER if btn['hover'] else BTN_DEFAULT
        txt_col = TEXT_COLOR
        if not btn['visible']:
            color = DISABLED_COLOR
            txt_col = (100, 100, 100)
            
        pygame.draw.rect(win, color, btn['rect'], border_radius=20)
        
        lbl = btn_font.render(btn['char'], True, txt_col)
        win.blit(lbl, (btn['rect'].centerx - lbl.get_width()//2, btn['rect'].centery - lbl.get_height()//2))

def draw_start_screen():
    anim = math.sin(pygame.time.get_ticks() / 300.0) * 10
    title = title_font.render("HANGMAN", True, HIGHLIGHT)
    win.blit(title, (WIN_WIDTH//2 - title.get_width()//2, WIN_HEIGHT//3 + anim))
    
    msg = btn_font.render("Press any key or click to start", True, TEXT_COLOR)
    win.blit(msg, (WIN_WIDTH//2 - msg.get_width()//2, WIN_HEIGHT//2 + 50))

def draw_game_over(mouse_pos):
    # Dark overlay
    overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    win.blit(overlay, (0,0))
    
    if game_won:
        msg = msg_font.render("YOU WON!", True, HIGHLIGHT)
    else:
        msg = msg_font.render("GAME OVER", True, ERROR_COLOR)
    win.blit(msg, (WIN_WIDTH//2 - msg.get_width()//2, 150))
    
    word_msg = guess_font.render(word, True, TEXT_COLOR)
    win.blit(word_msg, (WIN_WIDTH//2 - word_msg.get_width()//2, 230))
    
    # Buttons
    btn_w, btn_h = 200, 50
    play_rect = pygame.Rect(WIN_WIDTH//2 - btn_w//2, 350, btn_w, btn_h)
    exit_rect = pygame.Rect(WIN_WIDTH//2 - btn_w//2, 430, btn_w, btn_h)
    
    p_hover = play_rect.collidepoint(mouse_pos)
    e_hover = exit_rect.collidepoint(mouse_pos)
    
    pygame.draw.rect(win, HIGHLIGHT if p_hover else BTN_DEFAULT, play_rect, border_radius=10)
    pygame.draw.rect(win, ERROR_COLOR if e_hover else BTN_DEFAULT, exit_rect, border_radius=10)
    
    p_txt = btn_font.render("Play Again", True, BACKGROUND if p_hover else TEXT_COLOR)
    e_txt = btn_font.render("Exit", True, BACKGROUND if e_hover else TEXT_COLOR)
    
    win.blit(p_txt, (play_rect.centerx - p_txt.get_width()//2, play_rect.centery - p_txt.get_height()//2))
    win.blit(e_txt, (exit_rect.centerx - e_txt.get_width()//2, exit_rect.centery - e_txt.get_height()//2))
    
    return play_rect, exit_rect

BACKGROUND = BG_COLOR

def main():
    global current_state
    run = True
    
    # Just in case they start with STATE_PLAYING instead of START
    # reset_game() 
    
    while run:
        clock.tick(60)
        draw_gradient_bg()
        mouse_pos = pygame.mouse.get_pos()
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if current_state == STATE_START:
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        run = False
                    else:
                        reset_game()
                        
            elif current_state == STATE_PLAYING:
                if event.type == pygame.MOUSEMOTION:
                    for btn in buttons:
                        btn['hover'] = btn['rect'].collidepoint(mouse_pos) and btn['visible']
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in buttons:
                        if btn['rect'].collidepoint(mouse_pos) and btn['visible']:
                            handle_guess(btn['char'])
                            break
                            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    elif pygame.K_a <= event.key <= pygame.K_z:
                        handle_guess(chr(event.key))
                        
            elif current_state == STATE_GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    p_rect, e_rect = draw_game_over(mouse_pos)
                    if p_rect.collidepoint(mouse_pos):
                        reset_game()
                    elif e_rect.collidepoint(mouse_pos):
                        run = False
                        
        # Drawing
        if current_state == STATE_START:
            draw_start_screen()
        elif current_state == STATE_PLAYING:
            draw_playing()
        elif current_state == STATE_GAME_OVER:
            draw_playing() # draw background stuff
            draw_game_over(mouse_pos)
            
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()