# Name: 
# Program: SnakeClone
import time
import random
import pygame
import sys

from pygame.locals import *

# Note that Global variables are generally not recomended to prevent difficult to trace bugs
# Global variables are used in this program.
# The justification is that all of these global variables are actually CONSTANTS
# so thier values should never change (preventing that difficult to trace bug)
FPS = 10
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0,  "cell size must divide WINDOW_WIDTH"
assert WINDOW_HEIGHT % CELL_SIZE == 0,  "cell size must divide WINDOW_HEIGHT"

CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE     = (255, 255, 255)  
BLACK     = (  0,   0,   0)  
RED       = (255,   0,   0)  
GREEN     = (  0, 255,   0)  
DARKGREEN = (  0, 155,   0) 
DARKGRAY  = ( 40,  40,  40)  
BGCOLOR = BLACK  

UP = 'up'  
DOWN = 'down'  
LEFT = 'left'  
RIGHT = 'right'  
HEAD = 0        # syntactic sugar: index of the worm's head 
X = 0
Y = 1

def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption("sNaKe_ClOnE")
    showStartScreen()  # Not yet defined
    while True:
        runGame()  # Needs work
        showGameOverScreen()  # Needs work


def showStartScreen():
    print("Start the Snake Game!!!")
                            # Hover over render to see what the params mean
    instText = BASIC_FONT.render("Use wasd or Arrows to turn.", False, RED, BLACK)
    startText = BASIC_FONT.render("Press Any key to start", True, GREEN, BLACK)
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(instText, (WINDOW_WIDTH/10, WINDOW_HEIGHT//8))
    DISPLAY_SURF.blit(startText, (WINDOW_WIDTH/10, WINDOW_HEIGHT-50))
    pygame.display.update()
    while True: 
        ## CHECK FOR USER INPUT ##
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:  
                terminate()   # to be implemented pygame.quit() then sys.exit()
            elif event.type == KEYDOWN: 
                if event.key == K_ESCAPE:  
                    terminate()
                return
        

 
#done needs 
def drawGrid():
    pygame.draw.rect(DISPLAY_SURF, BLACK, Rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT))
    # Use loops to draw lines (or rectangles) for the grid background
    
    #vertical lines
    for x in range(CELL_WIDTH):
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (x*CELL_SIZE, 0), (x*CELL_SIZE, WINDOW_HEIGHT))    
    #horizontal lines
    for y in range(CELL_HEIGHT):
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (0, y*CELL_SIZE), (WINDOW_WIDTH, y*CELL_SIZE))


def terminate():
    pygame.quit()
    sys.exit()


def drawApple(appleLocation):
    apple = pygame.Rect(appleLocation[X]*CELL_SIZE, appleLocation[Y]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, RED, apple)


def drawSnake(snakeCoords):
    for segment in snakeCoords:
        snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE, segment[Y]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, GREEN, snakeBodySeg)
        snakeBodySeg = pygame.Rect(segment[X]*CELL_SIZE+2, segment[Y]*CELL_SIZE+2, CELL_SIZE-4, CELL_SIZE-4)
        pygame.draw.rect(DISPLAY_SURF, DARKGREEN, snakeBodySeg)


def showGameOverScreen():
    # loop to get player "stuck" on game over
    # break the loop when they prpess a button like the start screen
    while True:
        goFont = pygame.font.Font('freesansbold.ttf', 100)
        gameText = goFont.render("Game", True, GREEN, BLACK)
        overText = goFont.render("Over", True, GREEN, BLACK)
        playText = BASIC_FONT.render("Press any key to play again.", True, RED, BLACK)
        DISPLAY_SURF.fill(BLACK)
        DISPLAY_SURF.blit(gameText, (WINDOW_WIDTH/10, WINDOW_HEIGHT//8))
        DISPLAY_SURF.blit(overText, (WINDOW_WIDTH/8, WINDOW_HEIGHT//2))
        DISPLAY_SURF.blit(playText, (WINDOW_WIDTH/10, WINDOW_HEIGHT-50))
        pygame.display.update()
        time.sleep(1)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:  
                terminate()   # to be implemented pygame.quit() then sys.exit()
            elif event.type == KEYDOWN: 
                if event.key == K_ESCAPE:  
                    terminate()
                # Improve to start game again...


def getRandomLocation(snakeCoords):
    # return a tuple (#,#) that represent an x,y corrdinate
    x = random.randint(0, CELL_WIDTH-1)
    y = random.randint(0, CELL_HEIGHT-1)
    # needs to be improved to prevent spawning on top of snake

    return (x, y)

def runGame():
    startX = CELL_WIDTH // 2
    startY = CELL_HEIGHT // 2
    snakeCoords = [(startX, startY)]
    direction = random.choice([RIGHT, LEFT, UP, DOWN])
    apple = getRandomLocation(snakeCoords)  # to be implemented
    
    # Event handling loop
    while True: 
        ## CHECK FOR USER INPUT ##
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:  
                terminate()   # to be implemented pygame.quit() then sys.exit()
            elif event.type == KEYDOWN: 
                if (event.key == K_LEFT or event.key == K_a): 
                    direction = LEFT  
                elif (event.key == K_RIGHT or event.key == K_d):  
                    direction = RIGHT  
                elif (event.key == K_UP or event.key == K_w):  
                    direction = UP  
                elif (event.key == K_DOWN or event.key == K_s):  
                    direction = DOWN 
                elif event.key == K_ESCAPE:  
                    terminate()
                    
            ## END OF USER INPUT ##
            
        ## ~~~~~Game Logic section~~~~##
        # Move the snake (add a new head and remove the tail)
        
        if direction == RIGHT:
            newHead = (snakeCoords[HEAD][X]+1, snakeCoords[HEAD][Y])
        elif direction == LEFT:
            newHead = (snakeCoords[HEAD][X]-1, snakeCoords[HEAD][Y])
        elif direction == DOWN:
            newHead = (snakeCoords[HEAD][X], snakeCoords[HEAD][Y]+1)
        elif direction == UP:
            newHead = (snakeCoords[HEAD][X], snakeCoords[HEAD][Y]-1)
        
        snakeCoords.insert(0,newHead)
        # Check for collision If the snake collides what should it do
        #       What is it colliding with ?

        
        
        ## ~~~~~End of Logic Section~~~ ##
        
        
        ## Draw stuff then update screen
        
        drawGrid()
        drawSnake(snakeCoords)
        drawApple(apple)
        # drawScore 
        
        pygame.display.update()
        FPS_CLOCK.tick(FPS)




if __name__ == "__main__":
    main()