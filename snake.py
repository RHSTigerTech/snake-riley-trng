# Name: Riley Truong
# Program: SnakeClone
import time
import random
import pygame
import sys
from pygame.locals import *

# Note that Global variables are generally not recommended to prevent difficult to trace bugs
# Global variables are used in this program.
# The justification is that all of these global variables are actually CONSTANTS
# so their values should never change (preventing that difficult to trace bug)
FPS = 10
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0,  "cell size must divide WINDOW_WIDTH"
assert WINDOW_HEIGHT % CELL_SIZE == 0,  "cell size must divide WINDOW_HEIGHT"

CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
RED = (255, 0, 0)  
GREEN = (0, 255, 0)  
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)  
BGCOLOR = BLACK

UP = 'up'  
DOWN = 'down'  
LEFT = 'left'  
RIGHT = 'right'  
HEAD = 0        # syntactic sugar: index of the worm's head
X = 0
Y = 1
highScore = 0
currentMode = "Normal"  # Default mode is Normal


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption("sNaKe_ClOnE")
    showStartScreen()
    while True:
        chooseMode()  # Show select screen for game mode
        runGame(currentMode)  # Pass the selected mode to the game loop
        showGameOverScreen()  # Show game over screen


def showStartScreen():
    print("Start the Snake Game!!!")
    instText = BASIC_FONT.render("Use WASD or Arrow keys to turn.", False, RED, BLACK)
    startText = BASIC_FONT.render("Press Any key to start", True, GREEN, BLACK)
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(instText, (WINDOW_WIDTH/10, WINDOW_HEIGHT//8))
    DISPLAY_SURF.blit(startText, (WINDOW_WIDTH/10, WINDOW_HEIGHT-50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():  # Event handling loop
            if event.type == QUIT:  
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  
                    terminate()
                return  # Start the game


def chooseMode():
    global currentMode
    modeText = BASIC_FONT.render("Choose Game Mode: Normal (N) or Poison Apple (P)", True, WHITE)
    DISPLAY_SURF.fill(BLACK)
    DISPLAY_SURF.blit(modeText, (WINDOW_WIDTH / 10, WINDOW_HEIGHT / 3))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_n:
                    currentMode = "Normal"
                    return
                elif event.key == K_p:
                    currentMode = "Poison Apple"
                    return


def terminate():
    pygame.quit()
    sys.exit()


def drawGrid():
    pygame.draw.rect(DISPLAY_SURF, BLACK, Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    for x in range(CELL_WIDTH):
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, WINDOW_HEIGHT))
    for y in range(CELL_HEIGHT):
        pygame.draw.line(DISPLAY_SURF, DARKGRAY, (0, y * CELL_SIZE), (WINDOW_WIDTH, y * CELL_SIZE))


def drawApple(appleLocation, isPoisonApple=False):
    apple = pygame.Rect(appleLocation[X] * CELL_SIZE, appleLocation[Y] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    if isPoisonApple:
        pygame.draw.rect(DISPLAY_SURF, (128, 0, 128), apple)  # Red color for poison apple
    else:
        pygame.draw.rect(DISPLAY_SURF, RED, apple)  # Normal apple


def drawSnake(snakeCoords):
    for segment in snakeCoords:
        snakeBodySeg = pygame.Rect(segment[X] * CELL_SIZE, segment[Y] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, GREEN, snakeBodySeg)
        snakeBodySeg = pygame.Rect(segment[X] * CELL_SIZE + 2, segment[Y] * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
        pygame.draw.rect(DISPLAY_SURF, DARKGREEN, snakeBodySeg)


def showGameOverScreen():
    global highScore
    while True:
        goFont = pygame.font.Font('freesansbold.ttf', 100)
        gameText = goFont.render("Game", True, GREEN, BLACK)
        overText = goFont.render("Over", True, GREEN, BLACK)
        playText = BASIC_FONT.render("Press any key to play again.", True, RED, BLACK)
        highScoreText = BASIC_FONT.render(f"High Score: {highScore}", True, WHITE, BLACK)
        DISPLAY_SURF.fill(BLACK)
        DISPLAY_SURF.blit(gameText, (WINDOW_WIDTH / 10, WINDOW_HEIGHT // 8))
        DISPLAY_SURF.blit(overText, (WINDOW_WIDTH / 8, WINDOW_HEIGHT // 2))
        DISPLAY_SURF.blit(playText, (WINDOW_WIDTH / 10, WINDOW_HEIGHT - 50))
        DISPLAY_SURF.blit(highScoreText, (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT - 100))
        pygame.display.update()
        time.sleep(1)
        for event in pygame.event.get():  # Event handling loop
            if event.type == QUIT:  
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  
                    terminate()
                return  # Restart the game


def getRandomLocation(snakeCoords, isPoisonApple=False):
    x = random.randint(0, CELL_WIDTH - 1)
    y = random.randint(0, CELL_HEIGHT - 1)
    while (x, y) in snakeCoords:
        x = random.randint(0, CELL_WIDTH - 1)
        y = random.randint(0, CELL_HEIGHT - 1)
    return (x, y)




def runGame(mode):
    global highScore
    startX = CELL_WIDTH // 2
    startY = CELL_HEIGHT // 2
    snakeCoords = [(startX, startY)]
    direction = RIGHT
    apple = getRandomLocation(snakeCoords)
    poisonApple = None  # Initially no poison apple
    score = 0
    regularAppleCount = 0  # Counter for regular apples eaten
    paused = False


    while True:
        for event in pygame.event.get():  # Event handling loop
            if event.type == QUIT:  
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT  
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:  
                    direction = RIGHT  
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:  
                    direction = UP  
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:  
                    direction = DOWN
                elif event.key == K_ESCAPE:  
                    terminate()
                elif event.key == K_p:  # Paused when pressed "P"
                    paused = not paused


        if paused:
            pausedText = BASIC_FONT.render("Paused", True, WHITE, BLACK)
            DISPLAY_SURF.fill(BLACK)
            DISPLAY_SURF.blit(pausedText, (WINDOW_WIDTH / 2 - 50, WINDOW_HEIGHT / 2))
            pygame.display.update()
            continue


        # Move the snake
        if direction == RIGHT:
            newHead = (snakeCoords[0][X] + 1, snakeCoords[0][Y])
        elif direction == LEFT:
            newHead = (snakeCoords[0][X] - 1, snakeCoords[0][Y])
        elif direction == DOWN:
            newHead = (snakeCoords[0][X], snakeCoords[0][Y] + 1)
        elif direction == UP:
            newHead = (snakeCoords[0][X], snakeCoords[0][Y] - 1)


        # Check for collision with walls or self
        if newHead in snakeCoords or not (0 <= newHead[X] < CELL_WIDTH and 0 <= newHead[Y] < CELL_HEIGHT):
            showGameOverScreen()  # Show game over screen
            if score > highScore:
                highScore = score
            return


        # Add new head and check if apple is eaten
        snakeCoords.insert(0, newHead)
        if newHead == apple:
            score += 1
            regularAppleCount += 1  # Increment regular apple count
            apple = getRandomLocation(snakeCoords)  # Respawn regular apple


            # Check if it's time for a poison apple
            if regularAppleCount == 1:
                poisonApple = getRandomLocation(snakeCoords)  # Spawn a poison apple
                regularAppleCount = 0  # Reset the regular apple count

        elif newHead == poisonApple and mode == "Poison Apple":
            if score == 0:
                showGameOverScreen()
                if score > highScore:
                    highScore = score
                return
            else:
                # Poison apple behavior (cut score in half)
                snakeCoords = snakeCoords[:len(snakeCoords) // 2]  # Cut the snake in half
                score = score // 2  # Halve the score when a poison apple is eaten
                poisonApple = getRandomLocation(snakeCoords)  # Respawn a new poison apple immediately
        else:
            snakeCoords.pop()  # Remove tail if no apple eaten

        # Draw the game elements
        drawGrid()
        drawSnake(snakeCoords)
        drawApple(apple)
        if mode == "Poison Apple" and poisonApple:
            drawApple(poisonApple, isPoisonApple=True)


        # Display score
        scoreText = BASIC_FONT.render(f"Score: {score}", True, WHITE)
        highScoreText = BASIC_FONT.render(f"High Score: {highScore}", True, WHITE)
        DISPLAY_SURF.blit(scoreText, (10, 10))
        DISPLAY_SURF.blit(highScoreText, (WINDOW_WIDTH - 150, 10))


        pygame.display.update()
        FPS_CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
