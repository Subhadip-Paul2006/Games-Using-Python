from pygame.locals import *

# Block dimensions
BWIDTH     = 20
BHEIGHT    = 20
MESH_WIDTH = 1 # The border thickness around each block

# Board layout settings
BOARD_HEIGHT     = 7
BOARD_UP_MARGIN  = 40 # Space at the top for the score text
BOARD_MARGIN     = 2

# Game color palette (RGB format)
WHITE    = (255,255,255)
RED      = (255,50,50)
GREEN    = (50,255,50)
BLUE     = (50,100,255)
ORANGE   = (255,165,0)
GOLD     = (255,215,0)
PURPLE   = (160,32,240)
CYAN     = (0,255,255) 
BLACK    = (20,20,30) # Background color
GRID_CLR = (40,40,50) # Color of the board grid lines

# Game timing and speed
MOVE_TICK          = 1000 # Milliseconds between automatic block drops
TIMER_MOVE_EVENT   = USEREVENT+1 # Custom pygame event for dropping the block
GAME_SPEEDUP_RATIO = 1.5 # How much faster the game gets after leveling up
SCORE_LEVEL        = 2000 # Score needed to reach the next speed level
SCORE_LEVEL_RATIO  = 2 # Multiplier for the next score threshold

# Scoring details
POINT_VALUE       = 100 # Points earned per block cleared
POINT_MARGIN      = 10 # UI spacing for the score text
FONT_SIZE           = 25 # Font size for UI text