import pygame
import random
import sys

# starting pygame
pygame.init()

# visualisation
CARD_SIZE = 80
GRID_SIZE_X, GRID_SIZE_Y = 3, 2  # 3x2 grid for 6 cards
MARGIN = 10
FPS = 30
WIDTH = GRID_SIZE_X * (CARD_SIZE + MARGIN) - MARGIN
HEIGHT = GRID_SIZE_Y * (CARD_SIZE + MARGIN) - MARGIN
BG_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)

CARD_COLORS = [
    (173, 216, 230),  # blue
    (144, 238, 144),  # green
    (216, 191, 216),  # purple
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory")
font = pygame.font.Font(None, 36)


def create_board():
    ''' creating a list of randomly distributed cards'''
    cards = CARD_COLORS * (GRID_SIZE_X * GRID_SIZE_Y // len(CARD_COLORS))
    random.shuffle(cards)
    return cards

def draw_board(board, revealed):
    ''' drawing the board of the game '''
    screen.fill((0, 0, 128))
    for y in range(GRID_SIZE_Y): # y is rows and x is column on game board, GRID_SIZE for Y and X are amount of rows and columns respectively
        for x in range(GRID_SIZE_X):
            color = board[y * GRID_SIZE_X + x] if revealed[y][x] else (0, 0, 0) # colors at certain x and y position on game board, gray color on back of card when card is hidden 
            pygame.draw.rect(screen, color, (x * (CARD_SIZE + MARGIN), y * (CARD_SIZE + MARGIN), CARD_SIZE, CARD_SIZE)) # cards are shown as rectangles 
    pygame.display.flip()

def memory_game():
    ''' running memory game'''
  
    board = create_board()
    revealed = [[False] * GRID_SIZE_X for _ in range(GRID_SIZE_Y)]
    first_selection, second_selection = None, None
    matches = 0
    total_pairs = GRID_SIZE_X * GRID_SIZE_Y // 2  # 3 * 2 = 6, number of pairs, needs to be even
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= CARD_SIZE + MARGIN
                y //= CARD_SIZE + MARGIN
                if 0 <= x < GRID_SIZE_X and 0 <= y < GRID_SIZE_Y and not revealed[y][x]:
                    revealed[y][x] = True
                    if first_selection is None:
                        first_selection = (x, y)
                    elif second_selection is None:
                        second_selection = (x, y)

        draw_board(board, revealed)

        if first_selection and second_selection: # checking two selected cards 
            pygame.display.flip()
            pygame.time.wait(500)  # time until cards will either be flipped around again or be marked as a pair (0.5 ms)
            fx, fy = first_selection # coordinates of first card
            sx, sy = second_selection # coordinates of second card
            if board[fy * GRID_SIZE_X + fx] == board[sy * GRID_SIZE_X + sx]: # cards are checked if they have the same color 
                matches += 1 # if match than match-count increases by 1
                if matches == total_pairs: # if all matches are found the game will be over 
                    

                    #put's "You won!" on Screen and closes window automatically after 1500 milliseconds    
                    screen.fill(BG_COLOR)
                    text = font.render("You won!", True, TEXT_COLOR)
                    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    #other way to close the window:
                    #pygame.quit() 
                    sys.exit()
            else:
                revealed[fy][fx] = revealed[sy][sx] = False # if selected cards are not matching they will be flipped again 
            first_selection, second_selection = None, None 

        clock.tick(FPS)

if __name__ == "__main__":
    memory_game()
