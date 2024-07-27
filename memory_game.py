import pygame
import random
import sys

# Pygame initialisieren
pygame.init()

# Konstanten
CARD_SIZE = 80
GRID_SIZE_X, GRID_SIZE_Y = 3, 2  # 3x2 Raster für 6 Karten
MARGIN = 10
FPS = 30
WIDTH = GRID_SIZE_X * (CARD_SIZE + MARGIN) - MARGIN
HEIGHT = GRID_SIZE_Y * (CARD_SIZE + MARGIN) - MARGIN

# Pastellfarben für die Karten
CARD_COLORS = [
    (173, 216, 230),  # Pastellblau
    (144, 238, 144),  # Pastellgrün
    (216, 191, 216),  # Pastelllila
]

# Bildschirm einrichten
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

def create_board():
    """Erstelle eine Liste von zufällig angeordneten Kartenfarben."""
    cards = CARD_COLORS * (GRID_SIZE_X * GRID_SIZE_Y // len(CARD_COLORS))
    random.shuffle(cards)
    return cards

def draw_board(board, revealed):
    """Zeichne das gesamte Spielfeld basierend auf der Board- und Offenheitsliste."""
    screen.fill((0, 0, 0))
    for y in range(GRID_SIZE_Y):
        for x in range(GRID_SIZE_X):
            color = board[y * GRID_SIZE_X + x] if revealed[y][x] else (128, 128, 128)
            pygame.draw.rect(screen, color, (x * (CARD_SIZE + MARGIN), y * (CARD_SIZE + MARGIN), CARD_SIZE, CARD_SIZE))
    pygame.display.flip()

def memory_game():
    """Führe das Memory-Spiel aus."""
    board = create_board()
    revealed = [[False] * GRID_SIZE_X for _ in range(GRID_SIZE_Y)]
    first_selection, second_selection = None, None
    matches = 0
    total_pairs = GRID_SIZE_X * GRID_SIZE_Y // 2  # Anzahl der Paare
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

        if first_selection and second_selection:
            pygame.display.flip()
            pygame.time.wait(500)  # Warten Sie, um das Paar zu zeigen
            fx, fy = first_selection
            sx, sy = second_selection
            if board[fy * GRID_SIZE_X + fx] == board[sy * GRID_SIZE_X + sx]:
                matches += 1
                if matches == total_pairs:
                    print("You won!")
                    pygame.quit()
                    sys.exit()
            else:
                revealed[fy][fx] = revealed[sy][sx] = False
            first_selection, second_selection = None, None

        clock.tick(FPS)

if __name__ == "__main__":
    memory_game()
