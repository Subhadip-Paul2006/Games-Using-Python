import pdb
import constants
import pygame
import math
import copy
import sys

# Represents an individual falling Tetris piece
class Block(object):

    def __init__(self,shape,x,y,screen,color,rotate_en):
        self.shape = [] # List to hold the 4 distinct squares making up the piece
        
        # Convert grid coordinates into actual pixel coordinates on the screen
        for sh in shape:
            bx = sh[0]*constants.BWIDTH + x
            by = sh[1]*constants.BHEIGHT + y
            block = pygame.Rect(bx,by,constants.BWIDTH,constants.BHEIGHT)
            self.shape.append(block)     
            
        self.rotate_en = rotate_en # Can this block rotate? (O-blocks shouldn't)
        self.x = x # Center X position
        self.y = y # Center Y position
        self.diffx = 0 # Track pending X moves
        self.diffy = 0 # Track pending Y moves
        self.screen = screen # Where to draw the block
        self.color = color 
        self.diff_rotation = 0 # Track pending rotation

    def draw(self):
        # Draw each of the squares making up the piece
        for bl in self.shape:
            # Main color
            pygame.draw.rect(self.screen,self.color,bl)
            
            # Draw semi-transparent edges to make the block look 3D and glossy
            highlight = pygame.Surface((bl.width, bl.height), pygame.SRCALPHA)
            pygame.draw.rect(highlight, (255,255,255,100), (0,0,bl.width,4)) # Top highlight
            pygame.draw.rect(highlight, (255,255,255,60), (0,0,4,bl.height)) # Left highlight
            pygame.draw.rect(highlight, (0,0,0,100), (0,bl.height-4,bl.width,4)) # Bottom shadow
            pygame.draw.rect(highlight, (0,0,0,100), (bl.width-4,0,4,bl.height)) # Right shadow
            self.screen.blit(highlight, (bl.x, bl.y))

            # Black border around the block
            pygame.draw.rect(self.screen,constants.BLACK,bl,constants.MESH_WIDTH)
        
    # Rotate a point around the origin (0,0) using a standard 2D rotation matrix
    def get_rotated(self,x,y):
        rads = self.diff_rotation * (math.pi / 180.0) # Convert degrees to radians
        newx = x*math.cos(rads) - y*math.sin(rads)
        newy = y*math.cos(rads) + x*math.sin(rads)
        return (newx,newy)        

    # Request a movement update
    def move(self,x,y):
        self.diffx += x
        self.diffy += y  
        self._update()

    # Removes segments of this block if they are on a line that was just cleared
    def remove_blocks(self,y):
        new_shape = []
        for shape_i in range(len(self.shape)):
            tmp_shape = self.shape[shape_i]
            
            # If the block segment is above the cleared line, it falls down one row
            if tmp_shape.y < y:
                new_shape.append(tmp_shape)  
                tmp_shape.move_ip(0,constants.BHEIGHT)
            # If it's below the cleared line, leave it where it is
            elif tmp_shape.y > y:
                new_shape.append(tmp_shape)
                
        # Update shape to only contain blocks that survived
        self.shape = new_shape

    # Returns True if this piece still has any segments left on the board
    def has_blocks(self):
        return len(self.shape) > 0

    # Request a 90 degree clockwise rotation
    def rotate(self):
        if self.rotate_en:
            self.diff_rotation = 90
            self._update()

    # Applies any pending moves or rotations to the block segments
    def _update(self):
        for bl in self.shape:
            # Figure out where this segment is relative to the center top-left
            origX = (bl.x - self.x)/constants.BWIDTH
            origY = (bl.y - self.y)/constants.BHEIGHT
            
            # Calculate the math rotation coordinates
            rx,ry = self.get_rotated(origX,origY)
            
            # Determine the new absolute screen positions
            newX = rx*constants.BWIDTH  + self.x + self.diffx
            newY = ry*constants.BHEIGHT + self.y + self.diffy
            
            # Find the difference and move the Pygame Rect
            newPosX = newX - bl.x
            newPosY = newY - bl.y
            bl.move_ip(newPosX,newPosY)
            
        # Commit the changes to the central tracking coordinates
        self.x += self.diffx
        self.y += self.diffy
        
        # Reset modifiers so they don't apply twice
        self.diffx = 0
        self.diffy = 0
        self.diff_rotation = 0

    # Save a snapshot of everything before we attempt a move (in case we hit a wall)
    def backup(self):
        self.shape_copy = copy.deepcopy(self.shape)
        self.x_copy = self.x
        self.y_copy = self.y
        self.rotation_copy = self.diff_rotation     

    # Revert back to the saved snapshot (usually because the attempted move caused a collision)
    def restore(self):
        self.shape = self.shape_copy
        self.x = self.x_copy
        self.y = self.y_copy
        self.diff_rotation = self.rotation_copy

    # Check if this block hits the walls or any other settled blocks
    def check_collision(self,rect_list):
        for blk in rect_list:
            # Uses built in Pygame collision detection against our shape rects
            collist = blk.collidelistall(self.shape)
            if len(collist):
                return True
        return False