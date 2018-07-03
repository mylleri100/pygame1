import pygame
import random
 
# Define some constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
SPEED = 2
SIZE = 3
BLOCKSIZE = 12*SIZE
WALLSIZE = 2*SIZE
 
# --- Classes
 
 
class Block(pygame.sprite.Sprite):
    """ This class represents the gamearea builing block. Color, width (w) and height(h) passed as arguments """
    def __init__(self, color, w, h):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        self.rect = self.image.get_rect()             
####MODIFIED###
class Player(pygame.sprite.Sprite):    
    def __init__(self, x, y):   
        # Call the parent class (Sprite) constructor
        super().__init__()        
        self.count=-1
        self.dir="stop"
        self.image = pygame.Surface([10*SIZE,10*SIZE])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y 
        
    def update(self):
        """ Update the player's position. """
        orig_x=self.rect.x
        orig_y=self.rect.y
        prev_dir=self.dir 

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: self.dir="left"
        elif pressed[pygame.K_RIGHT]: self.dir="right"
        elif pressed[pygame.K_UP] and self.nogo!="up" : self.dir="up"
        elif pressed[pygame.K_DOWN]: self.dir="down"
        
        if self.dir=="left": self.rect.x -= SPEED
        if self.dir=="right": self.rect.x += SPEED
        if self.dir=="up" : self.rect.y -= SPEED
        if self.dir=="down": self.rect.y += SPEED

        if pygame.sprite.spritecollideany(self,outer_wall_list) != None:
            self.rect.x=orig_x
            self.rect.y=orig_y
            ## direction that collides=nogo
            self.nogo=self.dir
            self.dir=prev_dir
            self.count=5
        else:
            self.count-=1
            if self.count<0:
                self.nogo = "none"
        #DEBUGGING
        #print("nogo:", self.nogo)

# --- Create the window
# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 112*SIZE
screen_height = 112*SIZE
screen = pygame.display.set_mode([screen_width, screen_height])
 
# --- Sprite lists
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each WALL in the game
outer_wall_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
 
""" create game area """
block = Block(BLUE,screen_width,WALLSIZE)
block.rect.x = 0
block.rect.y = 0
all_sprites_list.add(block)
outer_wall_list.add(block)
block = Block(BLUE,screen_width,WALLSIZE)
block.rect.x = 0
block.rect.y = screen_height-WALLSIZE
all_sprites_list.add(block)
outer_wall_list.add(block)
block = Block(BLUE,WALLSIZE,screen_height)
block.rect.x = 0
block.rect.y = 0
all_sprites_list.add(block)
outer_wall_list.add(block)                                         
block = Block(BLUE,WALLSIZE,screen_height)
block.rect.x = screen_width-WALLSIZE
block.rect.y = 0
all_sprites_list.add(block)
outer_wall_list.add(block)                                         
"""End of game area"""


block_offset=WALLSIZE+BLOCKSIZE
for i in range(0,4):
    for j in range(0,4):
        block = Block(BLUE,BLOCKSIZE,BLOCKSIZE)
        block.rect.x = block_offset+i*2*BLOCKSIZE
        block.rect.y = block_offset+j*2*BLOCKSIZE
        # Add the block to the list of objects
        print("tehtiin palikka kohtaan (x,y)", block.rect.x, " ", block.rect.y)
        wall_list.add(block)
        all_sprites_list.add(block)
 
# Create player block
player = Player(WALLSIZE, WALLSIZE)
all_sprites_list.add(player)


# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0


#INIT PLAYFIELD
screen.fill(BLACK)
all_sprites_list.draw(screen)
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
    all_sprites_list.update()
    screen.fill(BLACK)       
    all_sprites_list.draw(screen)
    # update the screen
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()