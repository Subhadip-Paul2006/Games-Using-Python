import pygame
import pdb
import random
import math
import block
import constants

# Main game engine class that handles the loop, inputs, and game state
class Tetris(object):

    def __init__(self,bx,by):
        # Calculate screen resolution based on grid size
        self.resx = bx*constants.BWIDTH+2*constants.BOARD_HEIGHT+constants.BOARD_MARGIN
        self.resy = by*constants.BHEIGHT+2*constants.BOARD_HEIGHT+constants.BOARD_MARGIN
        
        # Define the 4 wall boundaries for collision detection
        self.board_up    = pygame.Rect(0,constants.BOARD_UP_MARGIN,self.resx,constants.BOARD_HEIGHT)
        self.board_down  = pygame.Rect(0,self.resy-constants.BOARD_HEIGHT,self.resx,constants.BOARD_HEIGHT)
        self.board_left  = pygame.Rect(0,constants.BOARD_UP_MARGIN,constants.BOARD_HEIGHT,self.resy)
        self.board_right = pygame.Rect(self.resx-constants.BOARD_HEIGHT,constants.BOARD_UP_MARGIN,constants.BOARD_HEIGHT,self.resy)
        
        # Keep track of all the finalized pieces lying at the bottom
        self.blk_list    = []
        
        # Pieces spawn near the top center of the board
        self.start_x = math.ceil(self.resx/2.0)
        self.start_y = constants.BOARD_UP_MARGIN + constants.BOARD_HEIGHT + constants.BOARD_MARGIN
        
        # All 7 tetris shapes defined by [X, Y], Color, and if they can rotate
        self.block_data = (
            ([[0,0],[1,0],[2,0],[3,0]],constants.RED,True),     # I piece
            ([[0,0],[1,0],[0,1],[-1,1]],constants.GREEN,True),  # S piece
            ([[0,0],[1,0],[2,0],[2,1]],constants.BLUE,True),    # J piece
            ([[0,0],[0,1],[1,0],[1,1]],constants.ORANGE,False), # O piece (No rotation)
            ([[-1,0],[0,0],[0,1],[1,1]],constants.GOLD,True),   # Z piece
            ([[0,0],[1,0],[2,0],[1,1]],constants.PURPLE,True),  # T piece
            ([[0,0],[1,0],[2,0],[0,1]],constants.CYAN,True),    # L piece
        )
        
        self.blocks_in_line = bx if bx%2 == 0 else bx-1
        self.blocks_in_pile = by
        self.score = 0
        self.speed = 1
        self.score_level = constants.SCORE_LEVEL

    # Reads keyboard presses and timer events
    def apply_action(self):
        for ev in pygame.event.get():
            # If the user clicks 'X' or hits 'q', quit the game
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.unicode == 'q'):
                self.done = True
            
            # WASD Movement bindings mapped to PyGame keys
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_s:
                    self.active_block.move(0,constants.BHEIGHT)
                    self.sound_move.play()
                if ev.key == pygame.K_a:
                    self.active_block.move(-constants.BWIDTH,0)
                    self.sound_move.play()
                if ev.key == pygame.K_d:
                    self.active_block.move(constants.BWIDTH,0)
                    self.sound_move.play()
                if ev.key == pygame.K_w:
                    self.active_block.rotate()
                    self.sound_rotate.play()
                if ev.key == pygame.K_p:
                    self.pause()
       
            # Triggered periodically by our set_move_timer
            if ev.type == constants.TIMER_MOVE_EVENT:
                self.active_block.move(0,constants.BHEIGHT) # Gravity pull
       
    # Stops game updates until 'p' is pressed again
    def pause(self):
        self.print_center(["PAUSE","Press \"p\" to continue"])
        pygame.display.flip()
        
        # Loop infinitely waiting for unpause
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_p:
                    return # Exits the infinite loop back to the game
       
    # Calculates and sets how fast the block falls
    def set_move_timer(self):
        speed = math.floor(constants.MOVE_TICK / self.speed)
        speed = max(1,speed) # Prevent division by zero or negative timers
        pygame.time.set_timer(constants.TIMER_MOVE_EVENT,speed)
 
    # The main game loop and setup
    def run(self):
        # Initialize sub-components of Pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        
        # Pre-load audio effects
        self.sound_move = pygame.mixer.Sound("move.wav")
        self.sound_rotate = pygame.mixer.Sound("rotate.wav")
        self.sound_clear = pygame.mixer.Sound("clear.wav")
        self.sound_game_over = pygame.mixer.Sound("game_over.wav")
        
        self.myfont = pygame.font.SysFont(pygame.font.get_default_font(),constants.FONT_SIZE)
        self.screen = pygame.display.set_mode((self.resx,self.resy))
        pygame.display.set_caption("Tetris")
        
        self.set_move_timer()
        
        self.done = False
        self.game_over = False
        self.new_block = True
        
        self.print_status_line()
        
        # Loop while the game is running and we haven't lost
        while not(self.done) and not(self.game_over):
            self.get_block()
            self.game_logic()
            self.draw_game()
        
        # Post-game clean up
        if self.game_over:
            self.print_game_over()
        
        pygame.font.quit()
        pygame.display.quit()        
   
    # Draw the score and speed multiplier
    def print_status_line(self):
        string = ["SCORE: {0}   SPEED: {1}x".format(self.score,self.speed)]
        self.print_text(string,constants.POINT_MARGIN,constants.POINT_MARGIN)        

    # Display death screen and wait for user exit
    def print_game_over(self):
        self.print_center(["Game Over","Press \"q\" to exit"])
        pygame.display.flip()
        
        while True: 
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.unicode == 'q'):
                    return

    # Helper function to print a list of strings vertically on the screen
    def print_text(self,str_lst,x,y):
        prev_y = 0
        for string in str_lst:
            size_x,size_y = self.myfont.size(string)
            txt_surf = self.myfont.render(string,False,(255,255,255))
            self.screen.blit(txt_surf,(x,y+prev_y))
            prev_y += size_y # Move down to text line

    # Helper function to print text exactly in the center of the window
    def print_center(self,str_list):
        max_xsize = max([tmp[0] for tmp in map(self.myfont.size,str_list)])
        self.print_text(str_list,self.resx/2-max_xsize/2,self.resy/2)

    # Scans the board to see if the active piece is hitting a settled piece
    def block_colides(self):
        for blk in self.blk_list:
            if blk == self.active_block:
                continue 
            if(blk.check_collision(self.active_block.shape)):
                return True
        return False

    # The master method orchestrating game rules, physics, and interactions
    def game_logic(self):
        # Save state before attempting player inputs
        self.active_block.backup()
        self.apply_action()
        
        # Test boundaries
        down_board  = self.active_block.check_collision([self.board_down])
        any_border  = self.active_block.check_collision([self.board_left,self.board_up,self.board_right])
        block_any   = self.block_colides()
        
        # If the player move caused a crash, reverse it
        if down_board or any_border or block_any:
            self.active_block.restore()
            
        # Re-save safe state to test a downward gravity drop natively
        self.active_block.backup()
        self.active_block.move(0,constants.BHEIGHT)
        can_move_down = not self.block_colides()  
        
        # Revert the gravity drop; we were just testing if it's possible
        self.active_block.restore()
        
        # Game over condition: Can't move down, and we're at the top spawn point
        if not can_move_down and (self.start_x == self.active_block.x and self.start_y == self.active_block.y):
            self.game_over = True
            self.sound_game_over.play()
            
        # If we hit the floor or topped out on other blocks, settle this piece
        if down_board or not can_move_down:     
            self.new_block = True
            self.detect_line() # Check for full lines  
 
    # Check if a row is completely full to clear it
    def detect_line(self):
        # Scan each fragment of the piece that just fell
        for shape_block in self.active_block.shape:
            tmp_y = shape_block.y
            tmp_cnt = self.get_blocks_in_line(tmp_y)
            
            # If the count isn't the width of the board, skip
            if tmp_cnt != self.blocks_in_line:
                continue 
                
            # Line is full, wipe it out
            self.remove_line(tmp_y)
            self.sound_clear.play()
            
            # Tally score
            self.score += self.blocks_in_line * constants.POINT_VALUE 
            
            # Check for level up
            if self.score > self.score_level:
                self.score_level *= constants.SCORE_LEVEL_RATIO
                self.speed       *= constants.GAME_SPEEDUP_RATIO
                self.set_move_timer() # Speed up dropping

    # Deletes all blocks on a specific row and shifts appropriate blocks down
    def remove_line(self,y):
        for block in self.blk_list:
            block.remove_blocks(y)
            
        # Prune empty block groupings from the list to save memory
        self.blk_list = [blk for blk in self.blk_list if blk.has_blocks()]

    # Returns the total number of blocks spanning horizontally on row 'y'
    def get_blocks_in_line(self,y):
        tmp_cnt = 0
        for block in self.blk_list:
            for shape_block in block.shape:
                tmp_cnt += (1 if y == shape_block.y else 0)            
        return tmp_cnt

    # Draw the main playing area, including the grid layout
    def draw_board(self):
        # Draw background grid columns
        for x in range(constants.BOARD_HEIGHT, self.resx - constants.BOARD_HEIGHT, constants.BWIDTH):
            pygame.draw.line(self.screen, constants.GRID_CLR, (x, constants.BOARD_UP_MARGIN), (x, self.resy - constants.BOARD_HEIGHT))
            
        # Draw background grid rows
        for y in range(constants.BOARD_UP_MARGIN, self.resy - constants.BOARD_HEIGHT, constants.BHEIGHT):
            pygame.draw.line(self.screen, constants.GRID_CLR, (constants.BOARD_HEIGHT, y), (self.resx - constants.BOARD_HEIGHT, y))
            
        # Draw bold white borders defining the play area
        pygame.draw.rect(self.screen,constants.WHITE,self.board_up)
        pygame.draw.rect(self.screen,constants.WHITE,self.board_down)
        pygame.draw.rect(self.screen,constants.WHITE,self.board_left)
        pygame.draw.rect(self.screen,constants.WHITE,self.board_right)
        
        self.print_status_line()

    # Spawns a random new Tetris piece
    def get_block(self):
        if self.new_block:
            tmp = random.randint(0,len(self.block_data)-1)
            data = self.block_data[tmp]
            
            # Spawn block instance and append to game memory
            self.active_block = block.Block(data[0],self.start_x,self.start_y,self.screen,data[1],data[2])
            self.blk_list.append(self.active_block)
            self.new_block = False

    # Top-level screen render update called every frame
    def draw_game(self):
        # Clear screen to black
        self.screen.fill(constants.BLACK)
        self.draw_board()
        
        for blk in self.blk_list:
            blk.draw() # Each block renders itself
            
        pygame.display.flip()

if __name__ == "__main__":
    # Standard board: 16 wide, 30 high
    Tetris(16,30).run()