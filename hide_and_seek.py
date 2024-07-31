import pygame
import random
import sys #module used to be able to exit the program after game is over 

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 3
CELL_SIZE = 100
MARGIN = 10
WIDTH = GRID_SIZE * (CELL_SIZE + MARGIN) - MARGIN
HEIGHT = GRID_SIZE * (CELL_SIZE + MARGIN) - MARGIN
BG_COLOR = (200, 200, 200)
CELL_COLOR = (150, 150, 150)
HIGHLIGHT_COLOR = (100, 100, 250)
TEXT_COLOR = (0, 0, 0)

# Canvas setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hide and Seek")


font = pygame.font.Font(None, 36)

# Hide pet randomly in one of the cells
pet_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))

def draw_grid(highlight=None):
    """
    Draw the grid and highlight a cell if provided
    """
    screen.fill(BG_COLOR)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = CELL_COLOR
            if highlight == (x, y):
                color = HIGHLIGHT_COLOR
            rect = pygame.Rect(x * (CELL_SIZE + MARGIN), y * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, TEXT_COLOR, rect, 1)
    pygame.display.flip()

# Main game 
running = True
found = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not found:
            x, y = event.pos
            x //= CELL_SIZE + MARGIN
            y //= CELL_SIZE + MARGIN
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                if (x, y) == pet_position:
                    found = True
                    #only for console:
                    print("You found the pet!")
                else:
                    #only for console:
                    print("The pet is not here.")
                draw_grid((x, y))

    if found:
        screen.fill(BG_COLOR)
        text = font.render("You found the pet!", True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1500)
        pygame.quit()
        sys.exit()