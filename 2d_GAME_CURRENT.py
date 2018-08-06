import pygame
import random

""" human controlled pacman, will be evolved to AI control later """ 
# Define some constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (30, 74, 250)
YELLOW = (220,255,0)
CRAPCOLOR = (255,255,0)
SPEED =2
PLAYER_SIZE=12
SIZE = 3
BLOCKSIZE = 12*SIZE # set 12 for normal, 6 for double, 3 for quadruple
HOWMANYBLOCKS = 4  # 4 for normal, 8 for double, 16 for quad...
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

class Crap(pygame.sprite.Sprite):
    def __init__(self,color):
        super().__init__()
        self.image = pygame.Surface([2*SIZE, 2*SIZE])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        #new attrib..
        self.eaten=False
    def update(self):
        if pygame.sprite.spritecollideany(self,player_list) != None:
            self.eaten=True
            all_sprites_list.remove(self)
            
            
        

class Player(pygame.sprite.Sprite):    
    def __init__(self, x, y):   
        # Call the parent class (Sprite) constructor
        super().__init__()        
        self.dir="stop"
        self.buffer_dir="empty"
        self.size=PLAYER_SIZE*SIZE 
        self.image = pygame.Surface([self.size,self.size])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        #boundaries for game area
        self.max_x=screen_width-WALLSIZE-self.size
        self.min_x=WALLSIZE
        self.max_y=screen_height-WALLSIZE-self.size
        self.min_y=WALLSIZE
        
    def update(self):
        """ Update the player's position. """
        orig_x=self.rect.x
        orig_y=self.rect.y

        prev_dir=self.dir

        #print("SELFDIR: ",self.dir)
        #print("BUFFER: ", self.buffer_dir)
              
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]: self.dir="left"
        elif pressed[pygame.K_RIGHT]: self.dir="right"
        elif pressed[pygame.K_UP] : self.dir="up"
        elif pressed[pygame.K_DOWN]: self.dir="down"
        elif self.buffer_dir != "empty":
            self.dir=self.buffer_dir
        
        if self.dir=="left": self.rect.x -= SPEED
        if self.dir=="right": self.rect.x += SPEED
        if self.dir=="up" : self.rect.y -= SPEED
        if self.dir=="down": self.rect.y += SPEED

        #clear buffer before it might be used
        self.buffer_dir="empty"
        
        if pygame.sprite.spritecollideany(self,outer_wall_list) != None:
            # prevent player to go out from playfield corners
            if prev_dir==self.dir:
                self.rect.x = orig_x
                self.rect.y = orig_y
            # player continues move forward if tries to turn/collide a block
            elif prev_dir=="left":
                self.rect.x = orig_x-SPEED
                self.rect.y = orig_y
                self.buffer_dir=self.dir
            elif prev_dir=="right":
                self.rect.x = orig_x+SPEED
                self.rect.y = orig_y
                self.buffer_dir=self.dir
            elif prev_dir=="up" :
                self.rect.y = orig_y-SPEED
                self.rect.x = orig_x
                self.buffer_dir=self.dir
            elif prev_dir=="down":
                self.rect.y = orig_y+SPEED
                self.rect.x = orig_x
                self.buffer_dir=self.dir    
            
            # reset direction to continue forward 
            self.dir=prev_dir
            #prevent corner bug again (does not affect other code)
            if (self.rect.x < self.min_x) or (self.rect.x > self.max_x) or (self.rect.y > self.max_y) or (self.rect.y < self.min_y):
                self.rect.x = orig_x
                self.rect.y = orig_y
            
# --- Create the window
# Initialize Pygame
pygame.init()

#game music
pygame.mixer.music.load('mario.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Set the height and width of the screen
screen_width = 112*SIZE
screen_height = 112*SIZE
screen = pygame.display.set_mode([screen_width, screen_height])
 
# --- Sprite lists
 
all_sprites_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
# List of each WALL in the game
outer_wall_list = pygame.sprite.Group()
# List of crap :)
crap_list = pygame.sprite.Group()

 
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

# create blocks in square matrix
block_offset=WALLSIZE+BLOCKSIZE
for i in range(0,HOWMANYBLOCKS):
    for j in range(0,HOWMANYBLOCKS):
        block = Block(BLUE,BLOCKSIZE,BLOCKSIZE)
        block.rect.x = block_offset+i*2*BLOCKSIZE
        block.rect.y = block_offset+j*2*BLOCKSIZE
        # Add the block to the list of objects
        # print("tehtiin palikka kohtaan (x,y)", block.rect.x, " ", block.rect.y)
        outer_wall_list.add(block)
        all_sprites_list.add(block)       
"""End of game area"""

""" create some crap to eat """
craps=HOWMANYBLOCKS*2+1
crap_offset=(WALLSIZE+BLOCKSIZE/2)-SIZE
for i in range (0,craps):
    for j in range (0,craps):
        crap = Crap(CRAPCOLOR)
        crap.rect.x = crap_offset+12*SIZE*i
        crap.rect.y = crap_offset+12*SIZE*j
        crap_list.add(crap)
        all_sprites_list.add(crap)  
        
        #remove crap inside blueblocks, replace this with more elegant later?
        if pygame.sprite.spritecollideany(crap,outer_wall_list) != None:
            crap_list.remove(crap)
            all_sprites_list.remove(crap)
""" end crapping for now """
 
# Create player block
player = Player(WALLSIZE, WALLSIZE)
all_sprites_list.add(player)
player_list.add(player)

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
#score = 0


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
